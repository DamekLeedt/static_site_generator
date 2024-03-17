from textnode import TextNode
from htmlnode import *
import re

def main():
    text_node = TextNode("This is a text node", "bold")
    node = TextNode("This is text with a `code block` word", "text")
    print(split_nodes_image([TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", "text")]))
                             
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
        if list(node.text).count(delimiter) % 2 != 0:
            return ValueError(f'"{node.text}" doesn\'t contain an even number of "{delimiter}"')
        block_list.extend([TextNode(string, text_type if node.text.index(string) % 2 == 1 else "text") for string in node.text.split(delimiter)])
    return block_list

def extract_markdown_images(text:str):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text:str):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes:list[TextNode]):
    for node in old_nodes:
        image = extract_markdown_images(node.text)
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
    return block_list

def split_nodes_link(old_nodes:list[TextNode]):
    for node in old_nodes:
        link = extract_markdown_links(node.text)
        text = list(filter(None, re.sub(r"\[(.*?)\]\((.*?)\)", "\n", node.text).split("\n")))
        block_list = ["" for _i in range(len(text) + len(link))]
        index = 0
        for i in range(0, len(text) + 1, 2):
            block_list[i] = TextNode(text[index], "text")
            index += 1
        index = 0
        for i in range(1, len(link) + 2, 2):
            block_list[i] = TextNode(link[index][0], "link", link[index][1])
            index += 1
    return block_list

def text_to_textnodes(text):
    pass

main()