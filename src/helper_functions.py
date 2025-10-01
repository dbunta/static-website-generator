import re
from textnode import *
from leafnode import *
from parentnode import *
from os import makedirs, listdir
from os.path import exists, join, isfile


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
    # r_search = r"!\[.*?\]\(.*?://.*?\..*?\..*?\)"
    r_search = r"!\[.*?\]\(.*?\)"
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
    # r_search = r"\[.*?\]\(.*?://.*?\..*?\..*?\)"
    r_search = r"\[.*?\]\(.*?\)"
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
    # r_search = r"!\[.*?\]\(.*?://.*?\..*?\..*?\)"
    r_search = r"!\[.*?\]\(.*?\)"
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
    # r_search = r"\[.*?\]\(.*?://.*?\..*?\)"
    r_search = r"\[.*?\]\(.*?\)"
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
    child_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        blocktype = block_to_blocktype(block)
        node = {}
        match blocktype:
            case "heading":
                headings = re.search(r"^#{1,6}", block).group(0)
                tag = f"h{len(headings)}" 
                text = re.sub("^#{1,6}", "", block).strip()
                children = None
                child_nodes.append(LeafNode(text, tag, None))
            case "quote":
                tag = "blockquote"
                text = block.replace(">", "").strip()
                children = None
                child_nodes.append(LeafNode(text, tag, None))
            case "code":
                tag = "code"
                text = block.strip("```")
                props = None
                children = None
                child_nodes.append(LeafNode(text, tag, None))
            case "unordered_list":
                tag = "ul"
                text = None
                children = text_to_children_unordered_list(block)
                child_nodes.append(ParentNode(tag, children, None))
            case "ordered_list":
                tag = "ol"
                text = None
                children = text_to_children_ordered_list(block)
                child_nodes.append(ParentNode(tag, children, None))
            case "paragraph":
                tag = "div"
                text = None
                children = [text_to_children_paragraph(block)]
                child_nodes.append(ParentNode(tag, children, None))
    return ParentNode("div", child_nodes)

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
        textnodes = text_to_textnodes(line.lstrip("- ").lstrip("* "))
        children = list(map(text_node_to_html_node, textnodes))
        parent = ParentNode("li", children)
        newlines.append(parent)
    return newlines

def text_to_children_ordered_list(text):
    lines = text.split('\n')
    newlines = []
    for line in lines:
        textnodes = text_to_textnodes(re.sub(r"^\d. ", "", line))
        children = list(map(text_node_to_html_node, textnodes))
        parent = ParentNode("li", children)
        newlines.append(parent)
    return newlines

def text_to_children_paragraph(text):
    textnodes = text_to_textnodes(text)
    htmlnodes = map(text_node_to_html_node, textnodes)
    return ParentNode("p", list(htmlnodes))

def extract_title(markdown):
    heading = re.search(r"^#.*", markdown).group(0)
    text = re.sub("^#", "", heading).strip()
    return text
    
def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    file = open(from_path)
    file_content = file.read()
    file.close()
    template = open(template_path)
    template_content = template.read()
    template.close()
    html = markdown_to_html_node(file_content).to_html()
    title = extract_title(file_content)
    template_content = template_content.replace("{{ Content }}", html).replace("{{ Title }}", title).replace("href=\"/", f"href=\"base_path").replace("src=\"/", f"src=\"base_path")

    
    destlist = dest_path.split("/")
    # dest = "/".join(dest_path.split("/")[0:-1])
    dest = "/".join(destlist[0:-1])
    destfile = dest[-1]

    if not exists(dest):
        makedirs(dest)

    newfile = open(dest_path, "x")
    newfile.write(template_content)
    newfile.close()
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    dirs = listdir(dir_path_content)
    print(dirs)
    for dir in dirs:
        dirpath = join(dir_path_content, dir)
        if not isfile(dirpath):
            generate_pages_recursive(dirpath, template_path, dest_dir_path, base_path)
        else:
            filename = dir.split(".")[0] + ".html"
            filepath = join(dest_dir_path, "/".join(dir_path_content.split("/")[2:]), filename)
            generate_page(dirpath, template_path, filepath, base_path)

