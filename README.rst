.. role:: py(code)
   :language: python

.. default-role:: py

===================
Django Shopify Sync
===================

I've been using this project for a few months and haven't been able to get in touch with the maintainers of
the origial repo: https://github.com/discolabs/django-shopify-sync 
or the more recently maintained fork: https://gitlab.com/thelabnyc/django-shopify-sync

This fork has been created with the goal of: 

0. Attracting contributors! 

1. Better documentation including type-hints, docstrings and "how to" / example templates. 

2. Adding tests using the pytest framework. 

3. Eventually incorporating the two originally created shopify-django apps to make an easy to use shopify-django app template. 


The two related apps are: 

1. https://github.com/discolabs/django-shopify-webhook

2. https://github.com/discolabs/django-shopify-auth


Installation
============

Pip install points to this repo: https://gitlab.com/thelabnyc/django-shopify-sync not the one you're reading now. 
1. Currently you'll need to copy the code into your own project to use it. 
2. Add `'shopify_sync',` to `INSTALLED_APPS`
3. Create a new `shopify_sync.Session` in Django admin or shell, enter your Shopify admin API token and site name.

Confused about where to find this session info? I was initially as well, there are two easy steps:
1. Use the shopify_python_api package (or any other method) to get a token https://github.com/Shopify/shopify_python_api#public-and-custom-apps
2. Save the "site" and "token" data for your sesson to the "Sesson" model that's defined in this app 


This package supports Python 3.X and Django>=1.11

How to use
==========

First we will get some of the products from shopify

.. code:: python

    from shopify_sync.models import Product, Session
    session = Session.objects.first()  # Assuming you have just one that you made previously
    products = Product.objects.sync_all(session) # everything
    products = Products.objects.sync_all(session, ids="111111111,") # just a subset, strangely "id" alone does not work

`sync_all` passes all kwargs to the `shopify_resource.find` which is part of the shpify_python_api package (which this is built on). 
We can then sync only the items that shopify returns from that search. Now we have all
of the `products` stored locally. shopify_python_api returns shopify.Product objects that get converted to instances of the 
shopify_django_sync Product model, then saved to our database. Though not relevant to this example, the app can also receive info in json (not object) form
which is relevant for processing webhooks. 

Now to update Shopify from Django

.. code:: python

    product = Product.objects.first() # get a product
    product.title = "New Bar Foo" # modify the title 
    product.save(push=True) 

The `save` method on the objects also accepts the optional argument `push`
which will push the updated model that is locally to Shopify. Now if a product
was edited on shopify through some means other than this Django app, we will
not have the current updated model. For this we need to sync

.. code:: python

    changed_product.sync()

the `changed_product` will get a local copy of the shopify_resource and then
do a `.reload()` on it so that we make a request to shopify. Then we sync
that back with our database.

 Note: Currently this app will keep an object in the database even if it's deleted from shopify directly. You can end up with orphan data in your database. 

