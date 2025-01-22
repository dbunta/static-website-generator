import re
from textnode import *
from leafnode import *

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
            return LeafNode("", tag="img", props={"src":text_node.url, "alt":text_node.text})
        case _:
            raise Exception("invalid text type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        arr = node.text.split(delimiter)
        for i in range(0, len(arr)): 
            if i % 2 == 0:
                new_nodes.append(TextNode(arr[i], TextType.NORMAL))
            else:
                new_nodes.append(TextNode(arr[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    # returns tuple: alt text, url of any markdown image
    # text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    #print(extract_markdown_images(text))
    # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
    retval = []
    r_search = r"!\[.*?\]\(.*?://.*?\..*?\..*?\)"
    matches = re.findall(r_search, text)
    descriptions = list(map(lambda x: re.findall(r"\[.*?\]", x)[0], matches))
    links = list(map(lambda x: re.findall(r"\(.*?\)", x)[0], matches))
    for i in range(0, len(descriptions)):
        description = descriptions[i][1:-1]
        link = links[i][1:-1]
        retval.append((description, link))
    return retval

def extract_markdown_links(text):
    # returns tuple: anchor text, url of any markdown image
    # text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    # print(extract_markdown_links(text))
    # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
    retval = []
    r_search = r"\[.*?\]\(.*?://.*?\..*?\..*?\)"
    matches = re.findall(r_search, text)
    descriptions = list(map(lambda x: re.findall(r"\[.*?\]", x)[0], matches))
    links = list(map(lambda x: re.findall(r"\(.*?\)", x)[0], matches))
    for i in range(0, len(descriptions)):
        description = descriptions[i][1:-1]
        link = links[i][1:-1]
        retval.append((description, link))
    return retval

def split_nodes_image(old_nodes):
    # text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    new_nodes = []
    r_search = r"!\[.*?\]\(.*?://.*?\..*?\..*?\)"
    for node in old_nodes:
        matches = re.findall(r_search, node.text)
        arr = re.split(r_search, node.text)
        i = 0
        for j in range(0, len(arr)):
            new_nodes.append(TextNode(arr[j], TextType.NORMAL))
            if j < len(arr)-1:
                alt_text = re.findall(r"\[.*?\]", matches[i])
                url = re.findall(r"\(.*?\)", matches[i])
                new_nodes.append(TextNode(alt_text[0][1:-1], TextType.IMAGES, url[0][1:-1]))
                i += 1
    return new_nodes

def split_nodes_link(old_nodes):
    # text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    new_nodes = []
    r_search = r"\[.*?\]\(.*?://.*?\..*?\..*?\)"
    for node in old_nodes:
        matches = re.findall(r_search, node.text)
        arr = re.split(r_search, node.text)
        i = 0
        for j in range(0, len(arr)):
            new_nodes.append(TextNode(arr[j], TextType.NORMAL))
            if j < len(arr)-1:
                alt_text = re.findall(r"\[.*?\]", matches[i])
                url = re.findall(r"\(.*?\)", matches[i])
                new_nodes.append(TextNode(alt_text[0][1:-1], TextType.LINKS, url[0][1:-1]))
                i += 1
    return new_nodes
