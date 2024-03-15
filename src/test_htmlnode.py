import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = str(HTMLNode("This is an HTML node", None, None, {"href": "https://www.google.com", "target": "_blank"}))
        node2 = 'HTMLNode(This is an HTML node, None, None, href="https://www.google.com" target="_blank")'
        self.assertEqual(node, node2)

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "This is a paragraph of text.").to_html()
        node2 = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node, node2)

        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()
        node2 = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node, node2)

        node = LeafNode(None, "This line has no tag.").to_html()
        node2 = "This line has no tag."
        self.assertEqual(node, node2)

        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        ).to_html()
        node2 = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node, node2)



if __name__ == "__main__":
    unittest.main()
