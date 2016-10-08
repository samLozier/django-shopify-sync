from __future__ import unicode_literals

from django.db import models
from shopify import Session as ShopifySession, ShopifyResource
from contextlib import contextmanager


class Session(models.Model):
    token = models.CharField(max_length=255)
    site = models.CharField(max_length=511)

    class Meta:
        app_label = 'shopify_sync'

    def to_shopify(self):
        shopify_session = ShopifySession(self.site, self.token)
        shopify_session.model = self
        return shopify_session

    def __str__(self):
        return "Session: %s" % self.site


@contextmanager
def activate_session(obj, session=None):
    """
    We want to make sure that we do not just use 'activate_session' and
    then not close the session, this is our solution.

    For this we take a Session, ShopifyResource, or model and return a
    ShopifyResource with the addition attrs of model and session.
    """

    if isinstance(obj, Session):
        shopify_resource = obj.to_shopify()
        shopify_resource.session = shopify_resource
        shopify_resource.model = obj

    elif isinstance(obj, ShopifyResource):
        shopify_resource = obj
        shopify_resource.model = None
        # If it is a ShopifyResource, look to se if it is active
        if session:
            # Use the session if we are given it
            if isinstance(session, ShopifySession):
                shopify_resource.session = session
            else:
                shopify_resource.session = session.to_shopify()
        elif hasattr(shopify_resource, 'session'):
            shopify_resource.activate_session(shopify_resource.session)
            try:
                yield shopify_resource
            except Exception as err:
                shopify_resource.clear_session()
                raise err
            else:
                shopify_resource.clear_session()
        else:
            # we have to try find the session then
            print(shopify_resource.__dict__)
            site = shopify_resource.connection._parse_site(obj.__class__.site)
            if site:
                # We can't do anything as there is no site given
                raise AttributeError("Object does not have a site attached. Please pass session")
            else:
                site = site[0].replace('https://', '')
                try:
                    session = Session.objects.get(site=site)
                except models.DoesNotExist:
                    raise models.DoesNotExist("The session for site '%s' does not exist. "
                                              "You must create a session first by having the "
                                              "site login first" % site)
                else:
                    shopify_resource.session = session.to_shopify()

    elif isinstance(obj, models.Model):
        shopify_resource = obj.to_shopify_resource()
        shopify_resource.session = obj.session.to_shopify()
        shopify_resource.model = obj

    elif hasattr(obj, 'session'):
        yield obj

    else:
        raise TypeError("Object needs to be a Model, ShopifyResource, or Session not '%s'." % type(obj))

    if not isinstance(shopify_resource, ShopifySession):
        # We now can activate the session if it isn't a ShopifySession
        shopify_resource.activate_session(shopify_resource.session)
    # TODO: They *really* should not be there, like there are not in
    # get_default_fields()!!!
    shopify_resource.attributes.pop('session', None)
    shopify_resource.attributes.pop('model', None)
    try:
        yield shopify_resource
    except Exception as err:
        shopify_resource.clear_session()
        raise err
    else:
        shopify_resource.clear_session()
