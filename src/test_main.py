import unittest

from main import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):

        """link1 = split_nodes_link([TextNode("This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)", "text")])
        link2 = [
            TextNode("This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a ", "text"),
            TextNode("link", "link", "https://boot.dev")
        ]
        self.assertEqual(link1, link2)"""

        list1 = text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)")
        list2 = [
            TextNode("This is ", "text"),
            TextNode("text", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and an ", "text"),
            TextNode("image", "image", "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev")
        ]
        self.assertEqual(list1, list2)


if __name__ == "__main__":
    unittest.main()
