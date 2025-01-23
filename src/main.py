from textnode import *
from htmlnode import *
from helper_functions import *

def main():
    text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    test = text_to_textnodes(text)
    # print(test)

    # tn = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    # hn = HtmlNode(props={"prop1":"chester", "prop2":3})
    # print(hn.props_to_html())

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(text_node.text)
        case TextType.BOLD:
            return LeafNode(text_node.text, "b")
        case TextType.ITALIC:
            # return HtmlNode("i", text_node.text)
            return LeafNode(text_node.text, "i")
        case TextType.CODE:
            # return HtmlNode("code", text_node.text)
            return LeafNode(text_node.text, "code")
        case TextType.LINKS:
            # return HtmlNode("a", text_node.text, props={"href":text_node.url})
            return LeafNode(text_node.text, "a", props={"href":text_node.url})
        case TextType.IMAGES:
            # return HtmlNode("img", props={"src":text_node.url, "alt":text_node.text})
            return LeafNode(tag="img", props={"src":text_node.url, "alt":text_node.text})
        case _:
            raise Exception("invalid text type")
    return ""


main()

