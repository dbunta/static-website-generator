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

    def test_split_nodes_delimiter_code(self):
        text_node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([text_node], '`', TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)

    def test_split_nodes_delimiter_bold(self):
        text_node = TextNode("This is text with a **code block** word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([text_node], '**', TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)

    def test_split_nodes_delimiter_italic(self):
        text_node = TextNode("This is text with a *code block* word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([text_node], '*', TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKa0qIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertEqual(images[0][0], "rick roll")
        self.assertEqual(images[0][1], "https://i.imgur.com/aKa0qIh.gif")
        self.assertEqual(images[1][0], "obi wan")
        self.assertEqual(images[1][1], "https://i.imgur.com/fJRm4Vk.jpeg")

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        self.assertEqual(links[0][0], "to boot dev")
        self.assertEqual(links[0][1], "https://www.boot.dev")
        self.assertEqual(links[1][0], "to youtube")
        self.assertEqual(links[1][1], "https://www.youtube.com/@bootdotdev")

    def test_split_node_image(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKa0qIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[0].url, None)

        self.assertEqual(new_nodes[1].text, "rick roll")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGES)
        self.assertEqual(new_nodes[1].url, "https://i.imgur.com/aKa0qIh.gif")

        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[2].url, None)

        self.assertEqual(new_nodes[3].text, "obi wan")
        self.assertEqual(new_nodes[3].text_type, TextType.IMAGES)
        self.assertEqual(new_nodes[3].url, "https://i.imgur.com/fJRm4Vk.jpeg")

    def test_split_node_links(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes[0].text, "This is text with a link ")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[0].url, None)

        self.assertEqual(new_nodes[1].text, "to boot dev")
        self.assertEqual(new_nodes[1].text_type, TextType.LINKS)
        self.assertEqual(new_nodes[1].url, "https://www.boot.dev")

        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[2].url, None)

        self.assertEqual(new_nodes[3].text, "to youtube")
        self.assertEqual(new_nodes[3].text_type, TextType.LINKS)
        self.assertEqual(new_nodes[3].url, "https://www.youtube.com/@bootdotdev")


