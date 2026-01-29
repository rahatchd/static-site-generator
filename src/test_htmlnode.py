import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    class _MockHTMLNode(HTMLNode):
        def to_html(self) -> str:
            return ""

    def test_html_node_to_props(self):
        node = self._MockHTMLNode(props={"href": "https://google.com", "target": "_blank"})
        self.assertEqual(' href="https://google.com" target="_blank"', node.props_to_html())


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        self.assertEqual(
            LeafNode("p", "This is a paragraph of text.").to_html(),
            "<p>This is a paragraph of text.</p>"
        )

    def test_leaf_to_html_a(self):
        self.assertEqual(
            LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html(),
            '<a href="https://www.google.com">Click me!</a>'
        )

    def test_no_value_to_html_raises(self):
        self.assertRaises(ValueError, LeafNode("x", None).to_html)

    def test_no_tag_to_html_raw(self):
        self.assertEqual("raw", LeafNode(None, "raw").to_html())


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_raw_children(self):
        parent_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_parent_children(self):
        inner1 = ParentNode("span", [LeafNode(None, "one")])
        inner2 = ParentNode("span", [LeafNode(None, "two")])
        outer = ParentNode("div", [inner1, inner2])
        self.assertEqual(
            outer.to_html(),
            "<div><span>one</span><span>two</span></div>",
        )

    def test_to_html_parent_with_props(self):
        child = LeafNode(None, "content")
        parent = ParentNode("section", [child], {"class": "main", "id": "top"})
        self.assertEqual(
            parent.to_html(),
            '<section class="main" id="top">content</section>',
        )

    def test_to_html_with_mixed_children(self):
        bold = LeafNode("b", "bold")
        inner = ParentNode("span", [LeafNode(None, "inside")])
        text = LeafNode(None, "end")
        parent = ParentNode("p", [bold, inner, text])
        self.assertEqual(
            parent.to_html(),
            "<p><b>bold</b><span>inside</span>end</p>",
        )

    def test_to_html_deep_nesting(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [
                        ParentNode(
                            "p",
                            [LeafNode(None, "deep")],
                        )
                    ],
                )
            ],
        )
        self.assertEqual(node.to_html(), "<div><section><p>deep</p></section></div>")

    def test_to_html_with_invalid_child_raises(self):
        node = ParentNode("div", ["not a node"])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_child_with_empty_string(self):
        child = LeafNode(None, "")
        parent = ParentNode("p", [child])
        self.assertEqual(parent.to_html(), "<p></p>")

    def test_to_html_with_missing_tag_raises(self):
        child = LeafNode(None, "text")
        parent_node = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_empty_children_list_raises(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()
