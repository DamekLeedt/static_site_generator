from textnode import TextNode
from htmlnode import *

def main():
    text_node = TextNode("This is a text node", "bold")
    print(text_node_to_html_node(text_node))

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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    block_list = []
    pass

main()