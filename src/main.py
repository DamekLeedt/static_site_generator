from textnode import TextNode
from htmlnode import *
from shutil import copytree, rmtree
import os
import re

def main():
    # generate_page("content", "template.html", "public")
    generate_page_recursive("content", "template.html", "public")
    
        
def text_node_to_html_node(text_node:TextNode):
    if text_node.text_type not in ["text", "bold", "italic", "code", "link", "image"]:
        raise Exception("Not a valid text type.")
    ttype = text_node.text_type
    text = text_node.text
    link = {"href": text_node.url} if text_node.url else None
    if ttype == "text":
        return LeafNode(None, text, link).to_html()
    if ttype == "bold":
        return LeafNode("b", text, link).to_html()
    if ttype == "italic":
        return LeafNode("i", text, link).to_html()
    if ttype == "code":
        return LeafNode("code", text, link).to_html()
    if ttype == "link":
        return LeafNode("a", text, {"href": text_node.url}).to_html()
    if ttype == "image":
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text}).to_html()

def split_nodes_delimiter(old_nodes:list[TextNode], delimiter:str, text_type):
    block_list = []
    for node in old_nodes:
        if node.text_type != "text":
            block_list.extend([node])
            continue
        if list(node.text).count(delimiter) % 2 != 0:
            return ValueError(f'"{node.text}" doesn\'t contain an even number of "{delimiter}"')
        index = 0
        for string in node.text.split(delimiter):
             block_list.extend([TextNode(string, text_type if index % 2 == 1 else "text")])
             index += 1
    return block_list

def extract_markdown_images(text:str):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text:str):
    return re.findall(r"[^!]\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes:list[TextNode]):
    return_list = []
    for node in old_nodes:
        image = extract_markdown_images(node.text)
        if not image:
            return_list.extend([node])
            continue
        text = list(filter(None, re.sub(r"!\[(.*?)\]\((.*?)\)", "\n", node.text).split("\n")))
        block_list = ["" for _i in range(len(text) + len(image))]
        index = 0
        for i in range(0, len(text) + 1, 2):
            block_list[i] = TextNode(text[index], "text")
            index += 1
        index = 0
        for i in range(1, len(image) + 2, 2):
            block_list[i] = TextNode(image[index][0], "image", image[index][1])
            index += 1
        return_list.extend(block_list)
    return return_list

def split_nodes_link(old_nodes:list[TextNode]):
    return_list = []
    for node in old_nodes:
        link = extract_markdown_links(node.text)
        if not link:
            return_list.extend([node])
            continue
        text = list(re.sub(r"[^!]\[(.*?)\]\((.*?)\)", " ", node.text).split("\n"))
        block_list = ["" for _i in range(len(text) + len(link))]
        index = 0
        for i in range(0, len(text) + 1, 2):
            block_list[i] = TextNode(text[index], "text")
            index += 1
        index = 0
        for i in range(1, len(link) + 2, 2):
            block_list[i] = TextNode(link[index][0], "link", link[index][1])
            index += 1
        return_list.extend(block_list)
    return return_list

def join_list(list:list):
    return "\n".join([str(string) for string in list])

def text_to_textnodes(text):
    old_nodes = split_nodes_link([TextNode(text, "text")])
    old_nodes = split_nodes_image(old_nodes)
    old_nodes = split_nodes_delimiter(old_nodes, "**", "bold")
    old_nodes = split_nodes_delimiter(old_nodes, "*", "italic")
    old_nodes = split_nodes_delimiter(old_nodes, "`", "code")
    return old_nodes

def markdown_to_blocks(markdown):
    if not markdown:
        raise ValueError("does not accept empty string")
    block_list = []
    temp = []
    for string in markdown.split("\n"):
        string = string.lstrip()
        #print("HI " + string)
        if string:
            #print(f"BUILDING... {temp} + {string} ({bool(string)})")
            temp.append(string.strip())
        else:
            #print(f"APPENDING... {temp}")
            block_list.append("\n".join(temp))
            temp = []
    if temp:
        block_list.append("\n".join(temp))
    #print(block_list)
    return block_list

def is_ordered_list(block):
    result = re.findall(r"(?m)^[1-9][0-9]*[.]", block)
    if not result:
        return False
    if len(result) == 0:
        if result[0] == "1.":
            return True
        return False
    results = [int(re.findall(r"[1-9][0-9]*", string)[0]) for string in result]
    prev = results[0]
    for num in results[1:]:
        # print(f"{prev} + 1 = {num} ? {prev + 1 == num}")
        if num != prev + 1:
            return False
        prev = num
    return True

def block_to_block_type(block:str):
    if re.findall(r"^#{1,6} \w", block):
        print("heading")
        return "heading"
    if re.findall(r"^```[\S\s]+\b```", block):
        print("code")
        return "code"
    if re.findall(r"^>", block):
        print("quote")
        return "quote"
    if re.findall(r"^[*|-]", block):
        print("unordered list")
        return "unordered list"
    if is_ordered_list(block):
        print("ordered list")
        return "ordered list"
    return "paragraph"

def heading_block_to_html(block:str):
    size = str(len(re.findall(r"#{1,6} ", block)[0].rstrip()))
    leafnode = LeafNode("h" + size, block.lstrip("# "))
    #print(leafnode.to_html())
    return leafnode

def code_block_to_html(block:str):
    parentnode = ParentNode("pre", LeafNode("code", block.strip("`")))
    #print(parentnode.to_html())
    return parentnode

def ordered_list_to_html(block:str):
    leafnode_list = []
    for line in block.split("\n"):
        leafnode_list.append(line.lstrip("1234567890. "))
    parentnode = ParentNode("ol", [LeafNode("li", leafnode) for leafnode in leafnode_list])
    #print(parentnode.to_html())
    return parentnode

def unordered_list_to_html(block:str):
    # print(block)
    leafnode_list = []
    for line in block.split("\n"):
        if line:
            leafnode_list.append(line.lstrip("*- "))
    parentnode = ParentNode("ul", [LeafNode("li", leafnode) for leafnode in leafnode_list])
    #print(parentnode.to_html())
    return parentnode

def quote_to_html(block:str):
    leafnode = LeafNode("blockquote", block)
    #print(leafnode.to_html())
    return leafnode

def paragraph_to_html(block:str):
    leafnode = LeafNode("p", block)
    #print(leafnode.to_html())
    return leafnode

def markdown_to_html_node(markdown:str):
    block_list = markdown_to_blocks(markdown)
    child_list = []
    for block in block_list:
        btype = block_to_block_type(block)
        if btype == "paragraph":
            child_list.append(paragraph_to_html(block))
        if btype == "ordered list":
            child_list.append(ordered_list_to_html(block))
        if btype == "unordered list":
            child_list.append(unordered_list_to_html(block))
        if btype == "code":
            child_list.append(code_block_to_html(block))
        if btype == "quote":
            child_list.append(quote_to_html(block))
        if btype == "heading":
            child_list.append(heading_block_to_html(block))
    parentnode = ParentNode("div", [node for node in child_list])
    # print(parentnode.to_html())
    return parentnode

def extract_title(markdown):
    header = re.findall(r"^[#] ", markdown)
    if not header:
        #print("shit")
        raise Exception("No title.")
    #print("piss :)")
    return markdown.split("\n")[0].lstrip("# ")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    text = open(from_path, encoding="utf-8").read()
    template = open(template_path).read()

    markdown = markdown_to_html_node(text).to_html()
    title = extract_title(text)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", markdown)

    path = "/".join(dest_path.split("/")[:-1])
    if len(path) > 1 and not os.path.exists(path):
        os.makedirs(path)
    open(dest_path, 'w').write(template)

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    current_path = dir_path_content.split("/")
    # print(current_path)
    for path in os.listdir(dir_path_content):
        current_path.append(path)
        path_str = "/".join(current_path)
        print(current_path)
        if os.path.isfile(path_str):
            print(path_str + " is a " + path_str.split(".")[1] + " file.")
            if path_str.split(".")[1] == "md":
                generate_page(path_str, template_path, dest_dir_path + f"/{"/".join(current_path[1:]).split(".")[0]}.html")
        else:
            print(path_str + " is a folder.")
            generate_page_recursive(path_str, template_path, dest_dir_path)
        current_path.pop()  

def crawl_path(dir, current_path:list=[]):
    current_path = [dir]
    for path in os.listdir(dir):
        current_path.append(path)
        path_str = "/".join(current_path)
        # print(current_path)
        if os.path.isfile(path_str):
            print(path_str + " is a file.")
        else:
            print(path_str + " is a folder.")
            crawl_path(path_str, current_path)
        current_path.pop()  
    
def copy_dir(path_to_copy, dir_to_paste):
    if os.path.exists(dir_to_paste):
        rmtree(dir_to_paste)
    copytree(path_to_copy, dir_to_paste)

main()