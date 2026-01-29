import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self) -> None:
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(node, node2)

        node3 = TextNode("This is anchor text", TextType.LINK, "https://boot.dev")

        self.assertNotEqual(node, node3)
        self.assertNotEqual(node2, node3)

        node4 = TextNode("This is b text node", TextType.BOLD)

        self.assertNotEqual(node, node4)


if __name__ == "__main__":
    unittest.main()
