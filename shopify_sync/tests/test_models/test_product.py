import pytest
from mixer.backend.django import mixer

from shopify_sync.models import Product


class TestProduct:
    pytestmark = pytest.mark.django_db

    @pytest.fixture()
    def mixed_product(self):
        return mixer.blend(Product, handle="test-product")

    def test_json_create(self):
        pass

    def test_update_product(self):
        mp = mixer.blend(Product, handle="test-product")
        p = Product.objects.get(handle="test-product")
        p.body_html = "New HTML"
        p.save()
        p.refresh_from_db()
        assert p.body_html == "New HTML", "Check if product was saved."

    def test_update_child_element(self):
        """
        Need to check that an update to variant triggers a
        webhook and that the webhook is handled
        :return:
        :rtype:
        """
        pass


    def test_product_meta_save(self, mp):
        p = Product.objects.get(id=mp.id)
        p.save(sync_meta=True)


        assert True

    def test_product_update(self):
        assert True

    def test_prdouct_delete(self):
        assert True

    def test_product_images_property(self):
        assert True

    def test_collects_property(self):
        assert True

    def test_variants_property(self):
        assert True

    def test_options_property(self):
        assert True

    def test_price_property(self):
        assert True

    def test_weight_property(self):
        assert True

    def test__get_tag_list(self):
        assert True

    def test__set_tag_list(self):
        assert True

    def test_add_tag(self):
        assert True

    def test_remove_tag(self):
        assert True



