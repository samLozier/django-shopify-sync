import logging

from .models import (CustomCollection, Customer, Order, Product, Shop,
                     SmartCollection)

log = logging.getLogger(__name__)


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
    log.info("Topic from webhook %s" % topic)
    return mapping.get(topic, None)


def get_topic_action(topic):
    return 'sync_one'


def webhook_received_handler(sender, domain, topic, data, **kwargs):
    """
    Signal handler to process a received webhook.
    """

    # Get the model related to the incoming topic and data.
    model = get_topic_model(topic, data)
    if model is None:
        assert "topic model does not exist"

    # Get the action related to the incoming topic.
    model_action = get_topic_action(topic)
    if model_action is None:
        assert "topic action does not exist"

    # Convert the incoming data to the relevant Shopify resource.
    shopify_resource = model.shopify_resource_from_json(data)
    log.warning("adsfadf %s" % str`(shopify_resource))

    # Execute the desired action.
    if model_action == 'sync_one':
        model.objects.sync_one(shopify_resource)
