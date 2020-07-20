from __future__ import unicode_literals

import logging
from copy import copy
import math

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models, utils
from django.db.models.fields.related import ForeignObjectRel
from pyactiveresource.connection import ResourceNotFound

from .. import SHOPIFY_API_PAGE_LIMIT

from .session import Session, ShopifyResource, ShopifySession, activate_session

log = logging.getLogger(__name__)


class ChangedFields(object):
    """
    Keeps track of fields that have changed since model instantiation, and on
    save updates only those fields.

    If save is called with update_fields, the passed kwarg is given precedence.

    A caveat: This can't do anything to help you with ManyToManyFields nor
    reverse relationships, which is par for the course: they aren't handled by
    save(), but are pushed to the db immediately on change.
    https://djangosnippets.org/snippets/2985/
    """
    related_classes = (models.ManyToManyField, ForeignObjectRel)

    def __init__(self, *args, **kwargs):
        super(ChangedFields, self).__init__(*args, **kwargs)

        self._changed_fields = {
            'id': self.id,
        }

    def __setattr__(self, name, value):
        if hasattr(self, '_changed_fields'):
            if name in self.__dict__ and self.__dict__[name].__class__ not in self.related_classes:
                old = getattr(self, name)
                super(ChangedFields, self).__setattr__(name, value)  # A parent's __setattr__ may change value.
                new = getattr(self, name)

                if old != new:
                    changed_fields = self._changed_fields

                    if name in changed_fields:
                        if changed_fields[name] == new:
                            # We've changed this field back to its value in the db. No need to push it back up.
                            changed_fields.pop(name)

                    else:
                        changed_fields[name] = copy(str(new))

            else:
                super(ChangedFields, self).__setattr__(name, value)

        else:
            super(ChangedFields, self).__setattr__(name, value)


class ShopifyResourceManager(models.Manager):
    """
    Base class for managing Shopify resource models.
    """

    def sync_one(self, obj, caller=None, # noqa C901
                 sync_children=True, sync_meta=False, *args, **kwargs):
        """
        Given a Shopify resource object, synchronise it locally
        so that we have an up-to-date version in the local
        database. Returns the created or updated local model.

        :param obj:
        :param caller:
        :param sync_children:
        :param sync_meta: should sync Metafields
        :param args:
        :param kwargs:
        :return:
        """
        if isinstance(obj, ShopifyResource):
            shopify_resource = obj
        elif hasattr(obj, 'to_shopify_resource'):
            shopify_resource = obj.to_shopify_resource()
        elif hasattr(obj, 'shopify_resource'):
            shopify_resource = obj.shopify_resource
        else:
            raise AttributeError("Object must have a shopify_resouce attr or "
                                 "be a ShopifyResource")
        # Synchronise any related model field.
        msg = "Syncing shopify resource '%s'" % str(shopify_resource)
        if caller:
            # We need to take the session form the parent
            shopify_resource.session = caller.session
            msg += " - called by parent resource '%s'" % str(caller)
        else:
            shopify_resource.session = Session.objects.first()

        log.debug(msg + ", site '%s'" % shopify_resource.session.site)

        # Not sync the related fields if we are not doing the children
        if sync_children:
            related_field_names = self.model.get_related_field_names()
        else:
            related_field_names = []
        for related_field_name in related_field_names:
            try:
                related_shopify_resource = getattr(shopify_resource,
                                                   related_field_name)
            except AttributeError:
                # this means we are getting a shopify resource not a django model
                related_shopify_resource = shopify_resource.attributes.get(related_field_name)
            if related_shopify_resource:
                field = getattr(self.model, related_field_name).field
                # handle deprecated `rel`
                if hasattr(field, 'rel') and hasattr(field.rel, 'to'):
                    related_model = field.rel.to
                else:
                    related_model = field.remote_field.model
                with activate_session(related_shopify_resource, session=shopify_resource.session) as related_shopify_resource:
                    related_model.objects.sync_one(related_shopify_resource,
                                                   caller=shopify_resource,
                                                   sync_meta=sync_meta,
                                                   *args, **kwargs)

        defaults = self.model.get_defaults(shopify_resource)

        # Synchronise instance.
        try:
            instance, created = self.update_or_create(id=shopify_resource.id,
                                                      defaults=defaults)
        except (utils.IntegrityError, Session.DoesNotExist):
            # This means that there needs to be the session in the defaults
            if isinstance(shopify_resource.session, ShopifySession):
                defaults.update({'session': shopify_resource.session.model})
            else:
                defaults.update({'session': shopify_resource.session})
            instance, created = self.update_or_create(
                id=shopify_resource.id,
                defaults=defaults,
            )
        except Exception as e:
            log.error(f'Sync failed for resource: {shopify_resource} and defaults: {defaults} exception: {e}')
            print('x', end='')
            raise e

        # don't sync children if set to False
        if not sync_children:
            _new = "Created" if created else "Updated"
            log.debug("%s <%s> (alone)" % (_new, instance))
            return instance

        # Synchronise any child fields.
        for child_field, child_model in self.model.get_child_fields().items():
            if hasattr(shopify_resource, child_field):
                child_shopify_resources = getattr(shopify_resource, child_field)
                if child_field == 'metafields':
                    if sync_meta:
                        with activate_session(shopify_resource,
                                              session=shopify_resource.session) as shopify_resource:
                            child_shopify_resources = shopify_resource.metafields()
                    else:
                        # skip metafields child_field
                        continue
                child_model.objects.sync_many(child_shopify_resources,
                                              parent_shopify_resource=shopify_resource,
                                              sync_meta=sync_meta)

        # Synchronise all related models for this model, like all addresses for a customer
        if hasattr(self.model, 'related_models'):
            # kwargs might contain a session object, and it might conflict with the session argument to sync_all
            if 'session' in kwargs:
                kwargs.pop('session')
            related_models = self.model.related_models()
            for related_model in related_models:
                related_model.objects.sync_all(shopify_resource.session,
                                               caller=shopify_resource,
                                               sync_meta=sync_meta,
                                               *args, **kwargs)

        _new = "Created" if created else "Updated"
        log.debug("%s <%s>" % (_new, instance))

        # show sync progress
        print('.', end='')

        return instance

    def sync_many(self, shopify_resources, parent_shopify_resource=None, sync_meta=False):
        """
        Given an array of Shopify resource objects, synchronise all of them locally so that we have up-to-date versions
        in the local database, Returns an array of the created or updated local models.

        :param shopify_resources:
        :param parent_shopify_resource:
        :param sync_meta: should sync Metafields
        :return:
        """
        instances = []
        for shopify_resource in shopify_resources:
            try:
                # If needed, ensure the parent ID is stored on the resource before synchronising it.
                if self.model.parent_field is not None and parent_shopify_resource is not None:
                    setattr(shopify_resource, self.model.parent_field, getattr(parent_shopify_resource, 'id'))
                instance = self.sync_one(shopify_resource,
                                         caller=parent_shopify_resource,
                                         sync_meta=sync_meta)
                instances.append(instance)
            except Exception as e:
                log.error(f'Exception during sync_many of {shopify_resource}: {e}')

        return instances

    def sync_all(self, session, sync_meta=False, **kwargs):
        """
        Synchronised all Shopify resources matched by the given **kwargs filter to our local database.
        Returns the synchronised local model instances.

        :param session:
        :param sync_meta: should sync Metafields
        :param kwargs:
        :return:
        """
        # need to make sure that we get a session to use

        shopify_resources = self.fetch_all(session=session, **kwargs)
        instances = self.sync_many(shopify_resources, sync_meta=sync_meta)

        # final newline after sync progress
        if 'caller' not in kwargs:
            print('')

        return instances

    def fetch_all(self, session, **kwargs):
        """
        Generator function, which fetches all Shopify resources matched by the given **kwargs filter.

        :param session:
        :param kwargs:
        :return:
        """
        # Get the class and make sure we have a session that we can use
        shopify_class = self.model.shopify_resource_class()
        
        # add caller id, like customer_id, to create properly prefixed urls
        if 'caller' in kwargs:
            caller = kwargs['caller']
            kwargs[caller._singular + '_id'] = caller.id
        
        limit = kwargs.pop('limit', SHOPIFY_API_PAGE_LIMIT)
        
        page = None
        # Before we've fetched the first page, it fetches the first page.
        # After that it keeps fetching until there is no next page
        while page is None or page.has_next_page():
            # The session does need to be activated before EVERY call
            # or else page.next_page() will error
            with activate_session(shopify_class, session=session) as fetcher:
                if page:
                    page = page.next_page()
                else:
                    page = fetcher.find(limit=limit, **kwargs)

                for shopify_resource in page:
                    shopify_resource.session = session
                    yield shopify_resource

    def push_one(self, instance, force=False, create=False, *args, **kwargs):
        """
        Push a local model instance to Shopify, creating or updating in the process.
        We ensure that we only send data that has been cnaged as well.

        The instance parameter needs to be a ShopifyResourceModel.

        Returns the locally synchronised model on success.

        :param instance:
        :param force:
        :param create:
        :param args:
        :param kwargs:
        :return:
        """
        if create and not force:
            raise AttributeError("Cannot have 'create' kwarg be True without"
                                 "having 'force' also be True.")
        session = instance.session
        # We don't need to push to shopify if there is nothing that has
        # changed. We still do a sync with shopify. If we do have a create flag
        # we will want to make sure that we don't just do a sync
        if len(instance._changed_fields) == 1 and not (force or create):
            log.info("No fields have changed, skipping push for '%s'" % instance)
            with activate_session(instance, session=session) as instance:
                return self.sync_one(instance, *args, **kwargs)
        # We don't want to push everything we have to shopify. We really only
        # want to push the data that has changed. This prevents us pushing data
        # that is stale. The method we use is to take the attributes that the
        # resource has and edit them to have only the changed fields and the
        # id. The method calls sync_one so we can update the db with any
        # changes that have been made, including our own changes
        with activate_session(instance, session=session) as shopify_resource:
            if not force:
                # This needs to be in the with loop as activate_session calls
                # to_shopify_resource and that ignores the _changed_fields, so
                # we need to re set them
                shopify_resource.attributes = instance._changed_fields
                log.info("Using only changed fields to push '%s': %s" % (shopify_resource, shopify_resource.attributes))
            # Save the Shopify resource.
            try:
                successful = shopify_resource.save()
            except ResourceNotFound as e:
                # When this fails, that means that there is no resource in shopify,
                # then if we have a create kwarg, then we will create the resource,
                # other wise we will just throw the error
                if create:
                    log.info("Matthew 10:26, the 'create' kwarg was passed, "
                             "the resource doesn't exist, time to create!")
                    with activate_session(instance, session=session) as shopify_resource:
                        shopify_resource = instance.clean_for_post(shopify_resource)
                        successful = shopify_resource.save()
                else:
                    log.warning("Resource '%s' could not be found!"
                                "Use the kwarg 'create=True' to create." % shopify_resource)
                    raise e

        if not successful:
            message = '[Shopify API Errors]: {0}'.format(
                ',\n'.join(shopify_resource.errors.full_messages())
            )
            log.error(message)
            raise Exception(message)

        with activate_session(shopify_resource, session=session) as shopify_resource:
            return self.sync_one(shopify_resource, *args, **kwargs)

    def push_many(self, instances, *args, **kwargs):
        """
        Push a list of local model instances to Shopify,
        creating or updating in the process.

        Returns the list of locally synchronised models on success.


        :param instances:
        :param args:
        :param kwargs:
        :return:
        """
        synchronised_instances = []
        for instance in instances:
            synchronised_instance = self.push_one(instance, *args, **kwargs)
            synchronised_instances.append(synchronised_instance)
        return synchronised_instances

    class Meta:
        abstract = True


class ShopifyResourceModelBase(ChangedFields, models.Model):
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
            # sometimes related fields have an _id suffix, as in the case of `customer_id`
            related_field = related_field + '_id'
            if hasattr(shopify_resource, related_field):
                # in this case, we have an id, so no need to get the `id` attribute as above
                defaults[related_field] = getattr(shopify_resource, related_field)

        return defaults

    @classmethod
    def get_default_fields(cls):
        """
        Get a list of field names that should be copied directly from a Shopify resource model when building the
        defaults hash.
        """
        default_fields_excluded = cls.get_default_fields_excluded()
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
                list(cls.get_child_fields().keys()) +  # python 3
                ['session', 'model'])

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

    @staticmethod
    def clean_for_post(shopify_resource):
        """
        When we use POST, we cannot have a 'id' present or else we get this error:

            [Shopify API Errors]: Source name cannot be set to a protected
            value by an untrusted API client.

        Our solution is to return the object with the id removed. We use a static method
        as we want to pass the object and it could be a ShopifyResource or model
        """
        clean_these_lists = ['shipping_lines', 'line_items']
        clean_these_keys = ['id', 'tax_lines', 'order_number', 'number', 'source_name']

        shopify_resource.id = None

        for key in clean_these_keys:
            shopify_resource.attributes.pop(key, None)

        for key in clean_these_lists:
            lines = shopify_resource.attributes.pop(key, None)
            if lines:
                for line in lines:
                    if isinstance(line, ShopifyResource):
                        line.attributes.pop('id', None)
                        line.attributes.pop('order_id', None)
                    else:
                        line.pop('id', None)
                shopify_resource.attributes[key] = lines

        if 'billing_address' in shopify_resource.attributes:
            # the billing zip can be blank, but when we push we need to have it
            # for some stupid reason. Like there database doesn't require a
            # zip, why should we have to provide it then. This is the shit that
            # makes me get all made at shopify and such...
            if not shopify_resource.attributes['billing_address']:
                # appreently the billing address can be blank
                shopify_resource.attributes['billing_address'] = {
                    'last_name': 'Empty',
                    'first_name': 'Billing addr',
                    'zip': None,
                    'city': None,
                    'address1': None,
                    'country': None,
                }
            if not shopify_resource.attributes['billing_address']['zip']:
                # yeah this will also happen:
                # 'billing_address Zip is not valid for Canada'
                shopify_resource.attributes['billing_address']['zip'] = 'K0L 2W0'
            if not shopify_resource.attributes['billing_address']['city']:
                # apparently PO boxes in Singapore don't need a city
                shopify_resource.attributes['billing_address']['city'] = 'Shopify Sux Eggs'
            if not shopify_resource.attributes['billing_address']['address1']:
                # Apprently you only really need the zip.
                shopify_resource.attributes['billing_address']['address1'] = ("a';DROP TABLE customers; SELECT"
                                                                              "* FROM customers WHERE 't' = 't'")
            if not shopify_resource.attributes['billing_address']['country']:
                # Sadly this has to be a county shopify knows
                shopify_resource.attributes['billing_address']['country'] = 'Azerbaijan'

        return shopify_resource

    def to_shopify_resource(self):
        """
        Convert this ShopifyResource model instance to its equivalent ShopifyResource.
        """
        instance = self.shopify_resource_class()
        # pyactiveresource changes __setattr__ to add attr to the attributes
        # dictionary and that is super annoying in so many ways so this is the
        # hack to undo that shit.
        instance.__dict__['session'] = self.session
        instance.__dict__['model'] = self

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

        # Get parent models for this model, like customer for an address, and add them to prefix options
        # so we can get a POST url like /customers/1319263371346/addresses/2195309133906.json
        if hasattr(self, '_prefix_options'):
            instance._prefix_options = self._prefix_options

        return instance

    def to_json(self):
        """
        Convert this ShopifyResource model instance to a "JSON" (simple Python) object.
        """
        return self.to_shopify_resource().attributes

    def sync(self, sync_meta=False):
        shopify_resource = self.to_shopify_resource()
        shopify_resource.reload()
        self.manager.sync_one(shopify_resource, sync_meta=sync_meta)
        self.refresh_from_db()

    def save(self, push=False, *args, **kwargs):
        if push:
            session = kwargs.pop('session', None)
            session = session if session else self.session
            log.info("Pushing '%s' (%s) to %s" % (self, self.id,
                                                  session.site))
            self = self.manager.push_one(self, session=session, *args, **kwargs)
            # have to save so that we can get the id if it is new
            kwargs.pop('sync_children', None)  # remove option field
            super(ShopifyResourceModelBase, self).save(*args, **kwargs)
        super(ShopifyResourceModelBase, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class ShopifyResourceModel(ShopifyResourceModelBase):
    id = models.BigIntegerField(primary_key=True)  # The numbers that shopify uses are too large
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    admin_graphql_api_id = models.CharField(max_length=80)

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
