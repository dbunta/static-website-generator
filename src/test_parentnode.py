import unittest
from parentnode import *
from leafnode import *

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        children = [
            LeafNode("bold text", "b")
        ]
        node = ParentNode("div", children, {"prop1":"value1"})
        html = node.to_html()
        self.assertEqual(html, "<div prop1=\"value1\"><b>bold text</b></div>")

    def test_to_html_with_parent(self):
        children_inner = [
            LeafNode("bold text", "b")
        ]
        children = [
            ParentNode("div", children_inner, {"prop1":"value1"}),
            LeafNode("bold text", "b"),
            LeafNode("unordered list", "ul")
        ]
        node = ParentNode("div", children)
        html = node.to_html()
        self.assertEqual(html, "<div><div prop1=\"value1\"><b>bold text</b></div><b>bold text</b><ul>unordered list</ul></div>")

