import unittest
from htmlnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = HtmlNode("h1", "test", props={"prop1":"test", "prop2":"test2"})
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "test")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"prop1":"test", "prop2":"test2"})

    def test_not_eq(self):
        node = HtmlNode("h1", "test", props={"prop1":"test", "prop2":"test2"})
        node2 = HtmlNode("h1", "test", props={"prop1":"test", "prop2":"test2"})
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        node = HtmlNode("h1", "test", props={"prop1":"test", "prop2":"test2"})
        self.assertEqual(node.props_to_html(), " prop1=\"test\" prop2=\"test2\"")



if __name__ == "__main__":
    unittest.main()