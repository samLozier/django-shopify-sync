import shopify
from django.conf import settings

from .models import (CustomCollection, Customer, Order, Product, Shop,
                     SmartCollection)


def get_topic_model(topic, data):
    """
    Return the model related to the given topic, if it's a valid topic
    permitted by theme settings. If the topic isn't permitted, or there's
    no rule mapping the given topic to a model, None is returned.
    """
    topic = topic.split('/')[0]
    mapping = {
        'collections': SmartCollection if 'rules' in data else CustomCollection,
        'products': Product,
        'customers': Customer,
        'orders': Order,
        'shop': Shop,
    }

    return mapping.get(topic, None)


def get_topic_action(topic):
    return 'sync_one'


def webhook_received_handler(sender, domain, topic, data, **kwargs):
    """
    Signal handler to process a received webhook.
    """
    session = shopify.ShopifyResource.set_site(settings.SHOPIFY_URL)

    # Get the model related to the incoming topic and data.
    model = get_topic_model(topic, data)
    if model is None:
        return

    # Get the action related to the incoming topic.
    model_action = get_topic_action(topic)
    if model_action is None:
        return

    # Convert the incoming data to the relevant Shopify resource.
    shopify_resource = model.shopify_resource_from_json(data)

    # Execute the desired action.
    if model_action == 'sync_one':
        model.objects.sync_one(session, shopify_resource)
