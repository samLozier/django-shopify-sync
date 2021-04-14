VERSION = (2, 2, 9)
__version__ = ".".join(map(str, VERSION))
__author__ = "David Burke"


SHOPIFY_API_PAGE_LIMIT: int = 250


default_app_config: str = "shopify_sync.apps.ShopifySyncConfig"
