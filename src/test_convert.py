import unittest

from convert import text_node_to_html_node, markdown_to_html_node
from htmlnode import LeafNode
from textnode import TextNode, TextType


class TestConvert(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, None)

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, None)

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, None)

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, None)

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.children, None)
        self.assertDictEqual(html_node.props, {"href": "https://boot.dev"})

    def test_image(self):
        node = TextNode("This is a image node", TextType.IMAGE, "boot.png")
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.children, None)
        self.assertDictEqual(html_node.props, {"src": "boot.png", "alt": "This is a image node"})

    def test_invalid_text_type_raises(self):
        class FakeType:
            pass

        node = TextNode("bad", FakeType())
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_headings(self):
        md = """
# heading 1

## heading 2

### heading 3

#### heading 4

##### heading 5

###### heading 6

    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>"
            "<h1>heading 1</h1>"
            "<h2>heading 2</h2>"
            "<h3>heading 3</h3>"
            "<h4>heading 4</h4>"
            "<h5>heading 5</h5>"
            "<h6>heading 6</h6>"
            "</div>"
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quote(self):
        md = """
> this is a quote
>so profound
> you don't know
> what you've found
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>this is a quote\nso profound\nyou don't know\nwhat you've found\n</blockquote></div>"
        )

    def test_unordered_list(self):
        md = """
- list of items
- there's no order
- they want no quarter
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul>"
            "<li>list of items</li>"
            "<li>there's no order</li>"
            "<li>they want no quarter</li>"
            "</ul></div>"
        )

    def test_ordered_list(self):
        md = """
1. list of items
2. there's an order
3. they want a quarter
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol>"
            "<li>list of items</li>"
            "<li>there's an order</li>"
            "<li>they want a quarter</li>"
            "</ol></div>"
        )

    def test_kitchen_sink(self):
        md = """
# Heading **one**

This is a _paragraph_ with **bold**, `code`, and a [link](https://boot.dev).

> quoted _text_ with **inline** stuff

- first **item**
- second _item_ with `code`
- third item

1. ordered **one**
2. ordered _two_
3. ordered `three`

```
code_block_line_1
code_block_line_2 with **markdown** that _should_ stay
```

Final paragraph with **bold** and _italic_.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>"
            "<h1>Heading <b>one</b></h1>"
            "<p>This is a <i>paragraph</i> with <b>bold</b>, "
            "<code>code</code>, and a "
            '<a href="https://boot.dev">link</a>.</p>'
            "<blockquote>quoted <i>text</i> with <b>inline</b> stuff\n</blockquote>"
            "<ul>"
            "<li>first <b>item</b></li>"
            "<li>second <i>item</i> with <code>code</code></li>"
            "<li>third item</li>"
            "</ul>"
            "<ol>"
            "<li>ordered <b>one</b></li>"
            "<li>ordered <i>two</i></li>"
            "<li>ordered <code>three</code></li>"
            "</ol>"
            "<pre><code>code_block_line_1\n"
            "code_block_line_2 with **markdown** that _should_ stay\n"
            "</code></pre>"
            "<p>Final paragraph with <b>bold</b> and <i>italic</i>.</p>"
            "</div>",
        )

    def test_mixed_blocks(self):
        md = """
> first quote line
> second **bold** line
>
>   third line with _italic_

- item one
- 
- item **three**

1.  first
2.badly formatted but still list?
3.   third with `code`
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>"
            "<blockquote>first quote line\n"
            "second <b>bold</b> line\n"
            "\n"
            "third line with <i>italic</i>\n</blockquote>"
            "<ul>"
            "<li>item one</li>"
            "<li></li>"
            "<li>item <b>three</b></li>"
            "</ul>"
            "<ol>"
            "<li>first</li>"
            "<li>badly formatted but still list?</li>"
            "<li>third with <code>code</code></li>"
            "</ol>"
            "</div>",
        )


if __name__ == "__main__":
    unittest.main()
