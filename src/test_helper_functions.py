import unittest
from textnode import *
from helper_functions import *

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_to_html(self):
        text_node = TextNode("this is normal", TextType.NORMAL)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(type(html_node), LeafNode)

    def test_text_to_html(self):
        value = "this is normal"
        text_node = TextNode(value, TextType.NORMAL)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, value)

    def test_text_to_html_bold(self):
        value = "this is normal"
        text_node = TextNode(value, TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, value)
        self.assertEqual(html_node.tag, "b")

    def test_text_to_html_italic(self):
        value = "this is normal"
        text_node = TextNode(value, TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, value)
        self.assertEqual(html_node.tag, "i")

    def test_text_to_html_code(self):
        value = "this is normal"
        text_node = TextNode(value, TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, value)
        self.assertEqual(html_node.tag, "code")

    def test_text_to_html_links(self):
        value = "this is normal"
        url = "https://google.com"
        text_node = TextNode(value, TextType.LINKS, url)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, value)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href":url})

    def test_text_to_html_images(self):
        value = "this is normal"
        url = "https://google.com"
        text_node = TextNode(value, TextType.IMAGES, url)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src":url, "alt":value})