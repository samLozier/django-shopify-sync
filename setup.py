from setuptools import setup, find_packages

version = __import__('shopify_sync').__version__

setup(
    name = 'django-shopify-sync',
    version = version,
    description = 'A package for synchronising Django models with Shopify resources.',
    long_description = open('README.rst').read(),
    author = 'David Burke',
    author_email = 'dburke@thelabnyc.com',
    url = 'https://gitlab.com/thelabnyc/django-shopify-sync',
    license = 'MIT',

    packages = find_packages(),

    install_requires = [
        'django >=1.11',
        'django-shopify-webhook >=0.2.6',
        'ShopifyAPI >=5.0.0',
        'jsonfield >=0.9.22',
    ],

    tests_require = [
        'python-dateutil >=2.4.2',
        'model_mommy >=1.2.1',
    ],

    zip_safe=True,
    classifiers=[],
)
