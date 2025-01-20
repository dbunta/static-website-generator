import unittest
from leafnode import *

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("click here", "a", {"href":"https://google.com"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "click here")
        self.assertEqual(node.props, {"href":"https://google.com"})


    def test_to_html_value_only(self):
        node = LeafNode("click here")
        html = node.to_html()
        self.assertEqual(html, "click here")


    def test_to_html(self):
        node = LeafNode("click here", "a", {"href":"https://google.com"})
        html = node.to_html()
        self.assertEqual(html, "<a href=\"https://google.com\">click here</a>")

