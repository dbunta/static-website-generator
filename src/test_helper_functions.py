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

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_nodes = text_to_textnodes(text)
        self.assertEqual(text_nodes[0].text, "This is ")
        self.assertEqual(text_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(text_nodes[0].url, None)

        self.assertEqual(text_nodes[1].text, "text")
        self.assertEqual(text_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(text_nodes[1].url, None)

        self.assertEqual(text_nodes[2].text, " with an ")
        self.assertEqual(text_nodes[2].text_type, TextType.NORMAL)
        self.assertEqual(text_nodes[2].url, None)

        self.assertEqual(text_nodes[3].text, "italic")
        self.assertEqual(text_nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(text_nodes[3].url, None)

        self.assertEqual(text_nodes[4].text, " word and a ")
        self.assertEqual(text_nodes[4].text_type, TextType.NORMAL)
        self.assertEqual(text_nodes[4].url, None)

        self.assertEqual(text_nodes[5].text, "code block")
        self.assertEqual(text_nodes[5].text_type, TextType.CODE)
        self.assertEqual(text_nodes[5].url, None)

        self.assertEqual(text_nodes[6].text, " and an ")
        self.assertEqual(text_nodes[6].text_type, TextType.NORMAL)
        self.assertEqual(text_nodes[6].url, None)

        self.assertEqual(text_nodes[7].text, "obi wan image")
        self.assertEqual(text_nodes[7].text_type, TextType.IMAGES)
        self.assertEqual(text_nodes[7].url, "https://i.imgur.com/fJRm4Vk.jpeg")

        self.assertEqual(text_nodes[8].text, " and a ")
        self.assertEqual(text_nodes[8].text_type, TextType.NORMAL)
        self.assertEqual(text_nodes[8].url, None)

        self.assertEqual(text_nodes[9].text, "link")
        self.assertEqual(text_nodes[9].text_type, TextType.LINKS)
        self.assertEqual(text_nodes[9].url, "https://boot.dev")

    def test_markdown_to_blocks(self):
        markdown = """# This is a heading

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.

            * This is the first list item in a list block
            * This is a list item
            * This is another list item"""

        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks[0], "# This is a heading")
        self.assertEqual(blocks[1], "This is a paragraph of text. It has some **bold** and *italic* words inside of it.")
        self.assertEqual(blocks[2], """* This is the first list item in a list block
            * This is a list item
            * This is another list item""")
    
    def test_block_to_blocktype_heading(self):
        self.assertEqual(block_to_blocktype("# this is a heading"), "heading")

    def test_block_to_blocktype_code(self):
        self.assertEqual(block_to_blocktype("``` this is code ```"), "code")

    def test_block_to_blocktype_quote(self):
        block = """> this is quote line 1
        > this is quote line 2
        """
        self.assertEqual(block_to_blocktype(block), "quote")

    def test_block_to_blocktype_unordered_list(self):
        block = """* this is quote line 1
        - this is quote line 2
        """
        self.assertEqual(block_to_blocktype(block), "unordered_list")

    def test_block_to_blocktype_ordered_list(self):
        block = """1. this is quote line 1
        2. this is quote line 2
        """
        self.assertEqual(block_to_blocktype(block), "ordered_list")

    def test_block_to_blocktype_paragraph(self):
        self.assertEqual(block_to_blocktype("this is a paragraph"), "paragraph")


    def test_text_to_children_unordered_list(self):
        block = "* test\n*test2\n* test3"
        actual = text_to_children_unordered_list(block)
        self.assertEqual(len(actual), 3)
        self.assertEqual(actual[0].tag, "li")
        self.assertEqual(actual[0].value, None)
        self.assertEqual(actual[0].props, None)
        self.assertEqual(actual[0].children[0].value, "test")
        self.assertEqual(actual[0].children[0].tag, None)
        self.assertEqual(actual[0].children[0].props, None)
        self.assertEqual(actual[0].children[0].children, None)
        self.assertEqual(actual[1].tag, "li")
        self.assertEqual(actual[1].value, None)
        self.assertEqual(actual[1].props, None)
        self.assertEqual(actual[1].children[0].value, "test2")
        self.assertEqual(actual[1].children[0].tag, None)
        self.assertEqual(actual[1].children[0].props, None)
        self.assertEqual(actual[1].children[0].children, None)
        self.assertEqual(actual[2].value, None)
        self.assertEqual(actual[2].props, None)
        self.assertEqual(actual[2].children[0].value, "test3")
        self.assertEqual(actual[2].children[0].tag, None)
        self.assertEqual(actual[2].children[0].props, None)
        self.assertEqual(actual[2].children[0].children, None)

    def test_text_to_children_unordered_list_alt(self):
        block = "- test\n-test2\n- test3"
        actual = text_to_children_unordered_list(block)
        self.assertEqual(len(actual), 3)
        self.assertEqual(actual[0].tag, "li")
        self.assertEqual(actual[0].value, None)
        self.assertEqual(actual[0].props, None)
        self.assertEqual(actual[0].children[0].value, "test")
        self.assertEqual(actual[0].children[0].tag, None)
        self.assertEqual(actual[0].children[0].props, None)
        self.assertEqual(actual[0].children[0].children, None)
        self.assertEqual(actual[1].tag, "li")
        self.assertEqual(actual[1].value, None)
        self.assertEqual(actual[1].props, None)
        self.assertEqual(actual[1].children[0].value, "test2")
        self.assertEqual(actual[1].children[0].tag, None)
        self.assertEqual(actual[1].children[0].props, None)
        self.assertEqual(actual[1].children[0].children, None)
        self.assertEqual(actual[2].value, None)
        self.assertEqual(actual[2].props, None)
        self.assertEqual(actual[2].children[0].value, "test3")
        self.assertEqual(actual[2].children[0].tag, None)
        self.assertEqual(actual[2].children[0].props, None)
        self.assertEqual(actual[2].children[0].children, None)

    def test_text_to_children_ordered_list(self):
        block = "1. test\n2. test2\n3. test3"
        actual = text_to_children_ordered_list(block)
        self.assertEqual(actual[0].tag, "li")
        self.assertEqual(actual[0].value, None)
        self.assertEqual(actual[0].props, None)
        self.assertEqual(actual[0].children[0].value, "test")
        self.assertEqual(actual[0].children[0].tag, None)
        self.assertEqual(actual[0].children[0].props, None)
        self.assertEqual(actual[0].children[0].children, None)
        self.assertEqual(actual[1].tag, "li")
        self.assertEqual(actual[1].value, None)
        self.assertEqual(actual[1].props, None)
        self.assertEqual(actual[1].children[0].value, "test2")
        self.assertEqual(actual[1].children[0].tag, None)
        self.assertEqual(actual[1].children[0].props, None)
        self.assertEqual(actual[1].children[0].children, None)
        self.assertEqual(actual[2].value, None)
        self.assertEqual(actual[2].props, None)
        self.assertEqual(actual[2].children[0].value, "test3")
        self.assertEqual(actual[2].children[0].tag, None)
        self.assertEqual(actual[2].children[0].props, None)
        self.assertEqual(actual[2].children[0].children, None)
        
    def test_text_to_children_paragraph(self):
        block = "this is a paragraph"
        actual = text_to_children_paragraph(block)
        self.assertEqual(actual.tag, "p")
        self.assertEqual(actual.value, None)
        self.assertEqual(actual.props, None)
        self.assertEqual(actual.children[0].tag, None)
        self.assertEqual(actual.children[0].value, "this is a paragraph")

    def test_markdown_to_html_nodes_ul(self):
        markdown = "* test\n*test2\n* test3"
        actual = markdown_to_html_node(markdown)
        self.assertEqual(actual.tag, "ul")
        self.assertEqual(actual.value, None)
        self.assertEqual(actual.props, None)
        self.assertEqual(actual.children[0].tag, "li")
        self.assertEqual(actual.children[0].children[0].tag, None)
        self.assertEqual(actual.children[0].children[0].value, "test")
        self.assertEqual(actual.children[1].children[0].value, "test2")
        self.assertEqual(actual.children[2].children[0].value, "test3")

    def test_markdown_to_html_nodes_ol(self):
        markdown = "1. test\n2. test2\n3. test3"
        actual = markdown_to_html_node(markdown)
        self.assertEqual(actual.tag, "ol")
        self.assertEqual(actual.value, None)
        self.assertEqual(actual.props, None)
        self.assertEqual(actual.children[0].tag, "li")
        self.assertEqual(actual.children[0].children[0].tag, None)
        self.assertEqual(actual.children[0].children[0].value, "test")
        self.assertEqual(actual.children[1].children[0].value, "test2")
        self.assertEqual(actual.children[2].children[0].value, "test3")

    def test_markdown_to_html_nodes_p(self):
        markdown = "this is a paragraph"
        actual = markdown_to_html_node(markdown)
        self.assertEqual(actual.tag, "div")
        self.assertEqual(actual.value, None)
        self.assertEqual(actual.props, None)
        self.assertEqual(actual.children[0].tag, "p")
        self.assertEqual(actual.children[0].value, None)
        self.assertEqual(actual.children[0].children[0].tag, None)
        self.assertEqual(actual.children[0].children[0].value, "this is a paragraph")

    def test_markdown_to_html_nodes_code(self):
        markdown = "```this is code```"
        actual = markdown_to_html_node(markdown)
        self.assertEqual(actual.tag, "code")
        self.assertEqual(actual.value, "this is code")
        self.assertEqual(actual.props, None)
        self.assertEqual(actual.children, None)

    def test_markdown_to_html_nodes_quote(self):
        markdown = "> this is a quote\n> and more quoting"
        actual = markdown_to_html_node(markdown)
        self.assertEqual(actual.tag, "blockquote")
        self.assertEqual(actual.value, "this is a quote\n and more quoting")
        self.assertEqual(actual.props, None)
        self.assertEqual(actual.children, None)

    def test_markdown_to_html_nodes_heading(self):
        markdown = "# this is h1"
        actual = markdown_to_html_node(markdown)
        self.assertEqual(actual.tag, "h1")
        self.assertEqual(actual.value, "this is h1")
        self.assertEqual(actual.props, None)
        self.assertEqual(actual.children, None)
        markdown = "## this is h2"
        actual = markdown_to_html_node(markdown)
        self.assertEqual(actual.tag, "h2")
        self.assertEqual(actual.value, "this is h2")
        markdown = "### this is h3"
        actual = markdown_to_html_node(markdown)
        self.assertEqual(actual.tag, "h3")
        self.assertEqual(actual.value, "this is h3")

    def test_markdown_to_html_nodes_bold(self):
        markdown = "these are **bold** and *italic*"
        actual = markdown_to_html_node(markdown)
        self.assertEqual(actual.tag, "div")
        self.assertEqual(actual.value, None)
        self.assertEqual(actual.props, None)
        self.assertEqual(actual.children[0].tag, "p")
        self.assertEqual(actual.children[0].value, None)
        self.assertEqual(actual.children[0].children[0].tag, None)
        self.assertEqual(actual.children[0].children[0].value, "these are ")
        self.assertEqual(actual.children[0].children[1].tag, "b")
        self.assertEqual(actual.children[0].children[1].value, "bold")
        self.assertEqual(actual.children[0].children[2].tag, None)
        self.assertEqual(actual.children[0].children[2].value, " and ")
        self.assertEqual(actual.children[0].children[3].tag, "i")
        self.assertEqual(actual.children[0].children[3].value, "italic")