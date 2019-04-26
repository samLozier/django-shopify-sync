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
        shopify_session = ShopifySession(self.site, '2019-04', self.token)
        # pyactiveresource has a defined __setattr__
        shopify_session.__dict__['model'] = self
        shopify_session.__dict__['session'] = shopify_session
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

    elif isinstance(obj, ShopifyResource):
        shopify_resource = obj
        if session:
            # Use the session if we are given it and make sure it is a shopify
            # session we connect
            if isinstance(session, ShopifySession):
                shopify_resource.__dict__['session'] = session
            else:
                shopify_resource.__dict__['session'] = session.to_shopify()
        elif hasattr(shopify_resource, 'session'):
            # If there was no session provided, see if the resource has one
            # attached
            shopify_resource.activate_session(shopify_resource.session)
            try:
                yield shopify_resource
            except Exception as err:
                shopify_resource.clear_session()
                raise err
            else:
                shopify_resource.clear_session()
        else:
            # Otherwise we have to try find the session the session from the
            # resouce insides.
            print("Intorspection to find the session!", shopify_resource.__dict__)
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
        shopify_resource = obj
        shopify_resource.activate_session(obj.session)

    else:
        raise TypeError("Object needs to be a Model, ShopifyResource, or Session not '%s'." % type(obj))

    if not isinstance(shopify_resource, ShopifySession):
        # We now can activate the session if it isn't a ShopifySession
        shopify_resource.activate_session(shopify_resource.session)
    try:
        yield shopify_resource
    except Exception as err:
        shopify_resource.clear_session()
        raise err
    else:
        shopify_resource.clear_session()
