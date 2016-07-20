from unittest import TestCase
from ..models import Product


class ProductTagBaseCase(TestCase):
    def setUp(self):
        self.single_tag = "Car"
        self.multi_tag = ["Boat", "Duck"]
        self.multi_tag_str = ", ".join(self.multi_tag)
        self.prod_tags = "New, Old"
        self.prod_tag = "Green"
        self.product = Product()

    @staticmethod
    def assertContains(larger, smaller):
        for i in smaller.split(", "):
            assert i in larger, "'%s' is NOT in '%s'" % (i, larger)

    @staticmethod
    def assertNotContains(larger, smaller):
        for i in smaller.split(", "):
            assert i not in larger, "'%s' is in '%s'" % (i, larger)


class ProductSingleTagAddTestCase(ProductTagBaseCase):
    def test_add_single_tag_with_no_tags(self):
        self.assertEqual(self.product.tags, "")
        self.product.add_tag(self.single_tag)
        self.assertEqual(self.product.tags, self.single_tag)

    def test_add_single_tag_with_one_tag(self):
        self.product.tags = self.prod_tag
        self.product.add_tag(self.single_tag)
        self.assertContains(self.product.tags, self.single_tag)
        self.assertContains(self.product.tags, self.prod_tag)

    def test_add_single_tag_with_multi_tag(self):
        self.product.tags = self.prod_tags
        self.product.add_tag(self.single_tag)
        self.assertContains(self.product.tags, self.single_tag)
        self.assertContains(self.product.tags, self.prod_tags)


class ProductSingleTagRemoveTestCase(ProductTagBaseCase):
    def test_remove_single_tag_with_no_tags(self):
        self.assertEqual(self.product.tags, "")
        self.product.remove_tag(self.single_tag)
        self.assertEqual(self.product.tags, "")

    def test_remove_single_tag_with_one_tag(self):
        self.product.tags = self.prod_tag + ', ' + self.single_tag
        self.product.remove_tag(self.single_tag)
        self.assertNotContains(self.product.tags, self.single_tag)
        self.assertContains(self.product.tags, self.prod_tag)

    def test_remove_single_tag_with_multi_tag(self):
        self.product.tags = self.prod_tags + ', ' + self.single_tag
        self.product.remove_tag(self.single_tag)
        self.assertNotContains(self.product.tags, self.single_tag)
        self.assertContains(self.product.tags, self.prod_tags)


class ProductMultiTagAddTestCase(ProductTagBaseCase):
    def test_add_multi_tag_with_no_tags(self):
        self.assertEqual(self.product.tags, "")
        self.product.add_tag(self.multi_tag)
        self.assertEqual(self.product.tags, self.multi_tag_str)

    def test_add_multi_tag_with_one_tag(self):
        self.product.tags = self.prod_tag
        self.product.add_tag(self.multi_tag)
        self.assertContains(self.product.tags, self.multi_tag_str)
        self.assertContains(self.product.tags, self.prod_tag)

    def test_add_multi_tag_with_multi_tag(self):
        self.product.tags = self.prod_tags
        self.product.add_tag(self.multi_tag)
        self.assertContains(self.product.tags, self.multi_tag_str)
        self.assertContains(self.product.tags, self.prod_tags)


class ProductMultiTagRemoveTestCase(ProductTagBaseCase):
    def test_remove_multi_tag_with_no_tags(self):
        self.assertEqual(self.product.tags, "")
        self.product.remove_tag(self.multi_tag)
        self.assertEqual(self.product.tags, "")

    def test_remove_multi_tag_with_one_tag(self):
        self.product.tags = self.prod_tag + ', ' + self.multi_tag_str
        self.product.remove_tag(self.multi_tag)
        self.assertNotContains(self.product.tags, self.multi_tag_str)
        self.assertContains(self.prod_tag, self.product.tags)

    def test_remove_multi_tag_with_multi_tag(self):
        self.product.tags = self.prod_tags + ', ' + self.multi_tag_str
        self.product.remove_tag(self.multi_tag)
        self.assertNotContains(self.product.tags, self.multi_tag_str)
        self.assertContains(self.product.tags, self.prod_tags)
