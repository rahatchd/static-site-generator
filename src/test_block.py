import unittest

from block import BlockType, block_to_block_type, markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

        def test_leading_and_trailing_blank_lines(self):
            md = """


First block

Second block



    """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "First block",
                    "Second block",
                ],
            )

        def test_single_block_no_blank_lines(self):
            md = """Just a single line of text with **inline** stuff and _more_."""
            blocks = markdown_to_blocks(md)
            self.assertEqual(blocks, ["Just a single line of text with **inline** stuff and _more_."])

        def test_multiple_consecutive_blank_lines(self):
            md = """
First

Second


Third
    """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "First",
                    "Second",
                    "Third",
                ],
            )

        def test_heading_paragraph_and_list(self):
            md = """# Heading

Paragraph text that goes here.

- item one
- item two
- item three
    """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "# Heading",
                    "Paragraph text that goes here.",
                    "- item one\n- item two\n- item three",
                ],
            )

        def test_only_whitespace_blocks(self):
            md = "   \n\n\t\nReal content\n\n   "
            blocks = markdown_to_blocks(md)
            self.assertEqual(blocks, ["Real content"])


class TestBlock(unittest.TestCase):
    def test_heading_1(self):
        block = "# x"
        btype = block_to_block_type(block)
        self.assertIs(btype, BlockType.HEADING)

    def test_heading_2(self):
        block = "## x"
        btype = block_to_block_type(block)
        self.assertIs(btype, BlockType.HEADING)

    def test_heading_3(self):
        block = "### x"
        btype = block_to_block_type(block)
        self.assertIs(btype, BlockType.HEADING)

    def test_heading_4(self):
        block = "#### x"
        btype = block_to_block_type(block)
        self.assertIs(btype, BlockType.HEADING)

    def test_heading_5(self):
        block = "##### x"
        btype = block_to_block_type(block)
        self.assertIs(btype, BlockType.HEADING)

    def test_heading_6(self):
        block = "###### x"
        btype = block_to_block_type(block)
        self.assertIs(btype, BlockType.HEADING)

    def test_code(self):
        block = """```
def code():
    ...
```"""
        btype = block_to_block_type(block)
        self.assertIs(btype, BlockType.CODE)

    def test_code_empty(self):
        block = """```
```"""
        btype = block_to_block_type(block)
        self.assertIs(btype, BlockType.CODE)

    def test_quote(self):
        block = """>if i only could
> i'd make a deal with goood"""
        btype = block_to_block_type(block)
        self.assertIs(btype, BlockType.QUOTE)

    def test_unordered_list(self):
        block = """- a
- b
- c"""
        btype = block_to_block_type(block)
        self.assertIs(btype, BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = """1. a
2. b
3. c"""
        btype = block_to_block_type(block)
        self.assertIs(btype, BlockType.ORDERED_LIST)

    def test_paragraph(self):
        block = "some la la paragraph\nblah blah\nsmash mikoshi"
        btype = block_to_block_type(block)
        self.assertIs(btype, BlockType.PARAGRAPH)

    def test_paragraph_heading_gt_6(self):
        block = "####### x"
        btype = block_to_block_type(block)
        self.assertIs(btype, BlockType.PARAGRAPH)

        block = "###x"
        btype = block_to_block_type(block)
        self.assertIs(btype, BlockType.PARAGRAPH)

    def test_paragraph_incorrect_starting_backticks(self):
        block = """````
def code():
    ...
```"""
        btype = block_to_block_type(block)
        self.assertIs(btype, BlockType.PARAGRAPH)

    def test_paragraph_missing_trailing_backticks(self):
        block = """````
def code():
    ..."""
        btype = block_to_block_type(block)
        self.assertIs(btype, BlockType.PARAGRAPH)

    def test_paragraph_single_line_code(self):
        block = "`code`"
        btype = block_to_block_type(block)
        self.assertIs(btype, BlockType.PARAGRAPH)

    def test_paragraph_broken_quote(self):
        block = """>if i only could
i'd say this is a paragraph"""
        btype = block_to_block_type(block)
        self.assertIs(btype, BlockType.PARAGRAPH)

    def test_paragraph_broken_unordered_list(self):
        block = """- a
paragraph
- c"""
        btype = block_to_block_type(block)
        self.assertIs(btype, BlockType.PARAGRAPH)

    def test_paragraph_broken_ordered_list(self):
        block = """1. a
2 b
3. c"""
        btype = block_to_block_type(block)
        self.assertIs(btype, BlockType.PARAGRAPH)

    def test_paragraph_incorrect_order_ordered_list(self):
        block = """1. a
4. b
3. c"""
        btype = block_to_block_type(block)
        self.assertIs(btype, BlockType.PARAGRAPH)
