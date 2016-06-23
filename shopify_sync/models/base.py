from __future__ import unicode_literals

import logging
import math

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from .. import SHOPIFY_API_PAGE_LIMIT

from .session import Session
from shopify import Session as ShopifySession

log = logging.getLogger(__name__)


def get_shopify_pagination(total_count):
    """
    Get the appropriate pagination to use with Shopify's API
    given the total number of records.
    """
    last_page = (int(math.ceil(float(total_count) /
                 float(SHOPIFY_API_PAGE_LIMIT))))
    return (1, last_page, SHOPIFY_API_PAGE_LIMIT,)


class ShopifyResourceManager(models.Manager):
    """
    Base class for managing Shopify resource models.
    """

    def sync_one(self, shopify_resource, caller=None, session=None):
        """
        Given a Shopify resource object, synchronise it locally
        so that we have an up-to-date version in the local
        database. Returns the created or updated local model.
        """
        # Synchronise any related model field.
        msg = "Syncing shopify resource '%s'" % str(shopify_resource)
        if caller:
            msg += " - called by parent resource '%s'" % str(caller)
            # this means that we can pull the session from the parent
            session = session
        else:
            # get the session info from the header of the resource
            token = shopify_resource.__class__.headers['X-Shopify-Access-Token']
            site = shopify_resource.__class__.site
            # This will clean the url of the prefix and return a tuple
            site = shopify_resource.__class__.connection._parse_site(site)
            site = site[0].replace('https://', '')
            session, _ = Session.objects.update_or_create(site=site,
                                                          defaults={'token': token})
            if _:
                log.info("Created new session '%s'" % session)
        log.debug(msg)
        for related_field_name in self.model.get_related_field_names():
            try:
                related_shopify_resource = getattr(shopify_resource,
                                                   related_field_name)
            except NotImplementedError as err:
                log.warning("Shopify object '%s' is missing '%s' related_field" % (str(shopify_resource), err))
            else:
                related_model = getattr(self.model, related_field_name).field.rel.to
                related_model.objects.sync_one(related_shopify_resource,
                                               caller=shopify_resource,
                                               session=session)

        defaults = self.model.get_defaults(shopify_resource)

        # Synchronise instance.
        instance, created = self.update_or_create(
            id=shopify_resource.id,
            defaults=defaults,
        )

        # Synchronise any child fields.
        for child_field, child_model in self.model.get_child_fields().items():
            if hasattr(shopify_resource, child_field):
                child_shopify_resources = getattr(shopify_resource, child_field)
                child_model.objects.sync_many(child_shopify_resources,
                                              parent_shopify_resource=shopify_resource)
        _new = "Created" if created else "Updated"
        log.debug("%s <%s>" % (_new, instance))

        return instance

    def sync_many(self, shopify_resources, parent_shopify_resource=None):
        """
        Given an array of Shopify resource objects, synchronise all of them locally so that we have up-to-date versions
        in the local database, Returns an array of the created or updated local models.
        """
        instances = []
        for shopify_resource in shopify_resources:
            # If needed, ensure the parent ID is stored on the resource before synchronising it.
            if self.model.parent_field is not None and parent_shopify_resource is not None:
                setattr(shopify_resource, self.model.parent_field, getattr(parent_shopify_resource, 'id'))
            try:
                instance = self.sync_one(shopify_resource, caller=parent_shopify_resource)
            except NotImplementedError as exc:
                log.warning("shopify resource '%s' failed to sync for reason '%s'" % (str(shopify_resource), exc))
            else:
                instances.append(instance)
        return instances

    def sync_all(self, **kwargs):
        """
        Synchronised all Shopify resources matched by the given **kwargs filter to our local database.
        Returns the synchronised local model instances.
        """
        shopify_resources = self.fetch_all(**kwargs)
        return self.sync_many(shopify_resources)

    def fetch_all(self, session_id=None, **kwargs):
        """
        Generator function, which fetches all Shopify resources matched by the given **kwargs filter.
        """
        import shopify
        # need to make sure that we get a session to use
        if not session_id:
            session = Session.objects.first()
        else:
            session = Session.objects.get(id=session_id)
        # Get the class and make sure we have a session that we can use
        shopify_resource_class = self.model.shopify_resource_class
        shopify_session = shopify.Session(session.site, session.token)
        # And now we activate the session on the class
        shopify_resource_class.activate_session(shopify_session)
        # And we can continue as normal now that we have a session
        total_count = shopify_resource_class.count(**kwargs)
        current_page, total_pages, kwargs['limit'] = get_shopify_pagination(total_count)

        while current_page <= total_pages:
            kwargs['page'] = current_page
            shopify_resources = shopify_resource_class.find(**kwargs)
            for shopify_resource in shopify_resources:
                yield shopify_resource
            current_page += 1

    def push_one(self, instance):
        """
        Push a local model instance to Shopify, creating or updating in the process.

        The instance parameter can be either a ShopifyResourceModel, or an already-prepared ShopifyResource.

        Returns the locally synchronised model on success.
        """
        # Ensure we have a ShopifyResource prepared.
        if hasattr(instance, 'to_shopify_resource'):
            shopify_resource = instance.to_shopify_resource()
        else:
            shopify_resource = instance

        # Save the Shopify resource.
        if not shopify_resource.save():
            message = '[Shopify API Errors]: {0}'.format(
                ', '.join(shopify_resource.errors.full_messages())
            )
            log.error(message)
            raise Exception(message)
        return self.sync_one(shopify_resource)

    def push_many(self, instances):
        """
        Push a list of local model instances to Shopify,
        creating or updating in the process.

        Returns the list of locally synchronised models on success.
        """
        synchronised_instances = []
        for instance in instances:
            synchronised_instance = self.push_one(instance)
            synchronised_instances.append(synchronised_instance)
        return synchronised_instances

    class Meta:
        abstract = True


class ShopifyResourceModelBase(models.Model):
    """
    Base class for local Model objects that are to be synchronised with Shopify.
    """

    shopify_resource_class = None
    parent_field = None
    related_fields = []
    child_fields = {}

    objects = ShopifyResourceManager()

    json_encoder = DjangoJSONEncoder()

    @property
    def klass(self):
        return self.__class__

    @property
    def manager(self):
        return self.klass.objects

    @classmethod
    def get_defaults(cls, shopify_resource):
        """
        Get a hash of attribute: values that can be used to update or create a local instance of the given Shopify
        resource.
        """
        defaults = {}

        # Set simple attributes that we simply need to copy across.
        for field in cls.get_default_fields():
            if hasattr(shopify_resource, field):
                defaults[field] = getattr(shopify_resource, field)

        # Set ID values for foreign key references.
        for related_field in cls.get_related_field_names():
            if hasattr(shopify_resource, related_field):
                defaults[related_field + '_id'] = getattr(getattr(shopify_resource, related_field), 'id')
        return defaults

    @classmethod
    def get_default_fields(cls):
        """
        Get a list of field names that should be copied directly from a Shopify resource model when building the
        defaults hash.
        """
        default_fields_excluded = cls.get_default_fields_excluded() + ['session']
        fields = cls.get_parent_field_names()
        fields += [field.name for field in cls._meta.concrete_fields if field.name not in default_fields_excluded]
        return fields

    @classmethod
    def get_default_fields_excluded(cls):
        """
        Get a list of field names to be excluded when copying directly from a Shopify resource model and building
        a defaults hash.
        """
        return (cls.get_related_field_names() +
                list(cls.get_child_fields().keys()))  # python 3

    @classmethod
    def get_parent_field_names(cls):
        """
        Get a list of the names of parent fields for the current model.
        """
        if cls.parent_field is None:
            return []
        return [cls.parent_field]

    @classmethod
    def get_related_field_names(cls):
        """
        Get a list of the names of related fields for the current model.
        """
        return cls.related_fields

    @classmethod
    def get_child_fields(cls):
        """
        Get a list of child fields for the current model, in a "hash" format with the name of the field as the key
        and the related child model as the value.
        """
        return cls.child_fields

    @classmethod
    def get_r_fields(cls):
        return cls.r_fields

    @classmethod
    def shopify_resource_from_json(cls, json):
        """
        Return an instance of the Shopify Resource model for this model,
        built recursively using the given JSON object.
        """
        instance = cls.shopify_resource_class()
        log.info("Creating shopify reasource '%s'" % str(instance))
        log.debug("Using the following json: %s" % json)

        # Recursively instantiate any child attributes.
        for child_field, child_model in cls.get_child_fields().items():
            if child_field in json:
                json[child_field] = [child_model.shopify_resource_from_json(child_field_json)
                                     for child_field_json
                                     in json[child_field]]

        # Recursively instantiate any related attributes.
        if hasattr(cls, 'r_fields'):
            for r_field, r_model in cls.get_r_fields().items():
                if r_field in json:
                    json[r_field] = r_model.shopify_resource_from_json(json[r_field])

        instance.attributes = json
        return instance

    def to_shopify_resource(self):
        """
        Convert this ShopifyResource model instance to its equivalent ShopifyResource.
        """
        instance = self.shopify_resource_class()
        instance.activate_session(self.shopify_session)

        # Copy across attributes.
        for default_field in self.get_default_fields():
            if hasattr(self, default_field):
                attribute = getattr(self, default_field)
                # If the attribute is itself a ShopifyResourceModel, ignore it.
                # The relevant resource will be linked through a '_id' parameter.
                if not isinstance(attribute, ShopifyResourceModel):
                    try:
                        attribute_encoded = self.json_encoder.default(attribute)
                    except TypeError:
                        attribute_encoded = attribute
                    finally:
                        setattr(instance, default_field, attribute_encoded)

        # Recursively instantiate any child attributes.
        for child_field, child_model in self.get_child_fields().items():
            if hasattr(self, child_field):
                setattr(instance, child_field, [child.to_shopify_resource() for child in getattr(self, child_field)])

        return instance

    def to_json(self):
        """
        Convert this ShopifyResource model instance to a "JSON" (simple Python) object.
        """
        return self.to_shopify_resource().attributes

    def _shopify_session(self):
        shopify_session = ShopifySession(shop_url=self.session.site,
                                         token=self.session.token)
        return shopify_session
    shopify_session = property(_shopify_session)

    def sync(self):
        shopify_resource = self.to_shopify_resource()
        shopify_resource.reload()
        self.manager.sync_one(shopify_resource)

    def save(self, push=False, *args, **kwargs):
        if push:
            log.info("Pushing %s to store" % self)
            self = self.manager.push_one(self)
            # have to save so that we can get the id if it is new
            super(ShopifyResourceModelBase, self).save(*args, **kwargs)
        super(ShopifyResourceModelBase, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class ShopifyResourceModel(ShopifyResourceModelBase):
    id = models.BigIntegerField(primary_key=True)  # The numbers that shopify uses are too large
    session = models.ForeignKey(Session)

    class Meta:
        abstract = True


class ShopifyDatedResourceModel(ShopifyResourceModel):
    """
    Extends ShopifyResourceModel by adding two common fields for Shopify
    resources - `created_at` and `updated_at`.
    """

    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True
