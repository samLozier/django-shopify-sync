.. role:: py(code)
   :language: python

.. default-role:: py

===================
Django Shopify Sync
===================

Readme will be added here.

WIP

How to use
==========

First we will get some of the products from shopify

.. code:: python

    from shopify_sync.models import Product
    products = Product.objects.sync_all(query="For bar")

`sync_all` passes all kwargs to the `shopify_resource.find` so we can
then sync only the items that shopify returns from that search. Now we have all
of the `products` stored locally. Now to update from Django

.. code:: python

    product = Product.objects.first()
    product.title = "New Bar Foo"
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

