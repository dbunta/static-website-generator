import re
from textnode import *
from leafnode import *
from parentnode import *

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
                new_nodes.append(TextNode(arr[i], node.text_type))
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
            new_nodes.append(TextNode(arr[j], node.text_type, node.url))
            if j < len(arr)-1:
                alt_text = re.findall(r"\[.*?\]", matches[i])
                url = re.findall(r"\(.*?\)", matches[i])
                new_nodes.append(TextNode(alt_text[0][1:-1], TextType.IMAGES, url[0][1:-1]))
                i += 1
    return new_nodes

def split_nodes_link(old_nodes):
    # text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    new_nodes = []
    r_search = r"\[.*?\]\(.*?://.*?\..*?\)"
    for node in old_nodes:
        matches = re.findall(r_search, node.text)
        arr = re.split(r_search, node.text)
        i = 0
        for j in range(0, len(arr)):
            new_nodes.append(TextNode(arr[j], node.text_type, node.url))
            if j < len(arr)-1:
                alt_text = re.findall(r"\[.*?\]", matches[i])
                url = re.findall(r"\(.*?\)", matches[i])
                new_nodes.append(TextNode(alt_text[0][1:-1], TextType.LINKS, url[0][1:-1]))
                i += 1
    return new_nodes

def text_to_textnodes(text):
    # This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)
    text_nodes = [TextNode(text, TextType.NORMAL)]
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "*", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes

def markdown_to_blocks(markdown):
    lines = markdown.split('\n\n')
    blocks = list(map(lambda x: x.strip(), lines)) 
    return blocks

def block_to_blocktype(block):
    if re.findall(r"^#{1,6}.*", block):
        return "heading"
    if re.findall(r"^`{3}.*`{3}$", block):
        return "code"

    lines = block.split('\r')
    number_quotes = 0
    number_ul = 0
    number_ol = 0
    for line in lines:
        if line.startswith(">"):
            number_quotes += 1
        if line.startswith("* ") or line.startswith("- "):
            number_ul += 1
        if line.startswith(f"{number_ol+1}. "):
            number_ol += 1
    
    if len(lines) == number_quotes:
        return "quote"
    if len(lines) == number_ul:
        return "unordered_list"
    if len(lines) == number_ol:
        return "ordered_list"

    return "paragraph"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        blocktype = block_to_blocktype(block)
        match blocktype:
            case "heading":
                headings = re.search(r"^#{1,6}", block).group(0)
                tag = f"h{len(headings)}" 
                text = re.sub("^#{1,6}", "", block).strip()
                children = None
            case "quote":
                tag = "blockquote"
                text = block.replace(">", "").strip()
                children = None
            case "code":
                tag = "code"
                text = block.strip("```")
                props = None
                children = None
            case "unordered_list":
                tag = "ul"
                text = None
                children = text_to_children_unordered_list(block)
            case "ordered_list":
                tag = "ol"
                text = None
                children = text_to_children_ordered_list(block)
            case "paragraph":
                tag = "div"
                text = None
                children = [text_to_children_paragraph(block)]
    return HtmlNode(tag, text, children, None)

    # split markdown into blocks with existing function
    # loop over each block
    # determine type of block with existing function
    # based on type of block, createa a new htmlnode with proper data
    # assign the proper child htmlnode objects to the block node. 
    # text_to_children(text)
    # takes a string of text and returns a list of htmlnodes that represent 
    # the inline markdown using existing functions (textnode > htmlnode)
    # make all block nodes children under a single parent html node (div) and return it

def text_to_children_unordered_list(text):
    lines = text.split('\n')
    newlines = []
    for line in lines:
        textnode = text_to_textnodes(line.lstrip("- ").lstrip("* "))[0]
        child = text_node_to_html_node(textnode)
        parent = HtmlNode("li", None, [child], None)
        newlines.append(parent)
    return newlines

def text_to_children_ordered_list(text):
    lines = text.split('\n')
    newlines = []
    for line in lines:
        textnode = text_to_textnodes(re.sub(r"^\d. ", "", line))[0]
        child = text_node_to_html_node(textnode)
        parent = HtmlNode("li", None, [child], None)
        newlines.append(parent)
    return newlines

def text_to_children_paragraph(text):
    textnodes = text_to_textnodes(text)
    htmlnodes = map(text_node_to_html_node, textnodes)
    # print(list(htmlnodes))
    # textnode = text_to_textnodes(text)[0]
    # htmlnode = text_node_to_html_node(textnode)
    return HtmlNode(tag="p", children=list(htmlnodes))



    