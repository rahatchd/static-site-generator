from htmlnode import LeafNode, HTMLNode, ParentNode
from textnode import TextNode, TextType
from inline import text_to_textnodes
from block import markdown_to_blocks, block_to_block_type, BlockType


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unknown text type: {text_node.text_type}")


def _md_inline(md: str, preserve_newline: bool = False) -> list[LeafNode]:
    return [
        text_node_to_html_node(tn)
        for tn in text_to_textnodes(
            md.replace("\n", " ")
            if not preserve_newline
            else md
        )
    ]


def _md_paragraph(md: str) -> ParentNode:
    nodes = _md_inline(md)
    return ParentNode("p", nodes)


def _md_heading(md: str) -> ParentNode:
    hashes, txt = md.split(" ", maxsplit=1)
    assert all(h == "#" for h in hashes), "not a heading"
    num = len(hashes)
    return ParentNode(f"h{num}", _md_inline(txt))


def _md_code(md: str) -> ParentNode:
    code_block = "\n".join(md.split("\n")[1:-1]) + "\n"
    return ParentNode(
        "pre",
        [LeafNode("code", code_block)],
    )


def _md_quote(md: str) -> ParentNode:
    quote = "\n".join(line.lstrip(">").strip() for line in md.split("\n")) + "\n"
    return ParentNode("blockquote", _md_inline(quote, preserve_newline=True))


def _md_ul(md: str) -> ParentNode:
    items = [line.lstrip("- ").strip() for line in md.split("\n")]
    return ParentNode(
        "ul",
        [ParentNode("li", _md_inline(item)) for item in items],
    )


def _md_ol(md: str) -> ParentNode:
    items = [line.split(".", maxsplit=1)[-1].strip() for line in md.split("\n")]
    return ParentNode(
        "ol",
        [ParentNode("li", _md_inline(item)) for item in items],
    )


def markdown_to_html_node(markdown: str) -> HTMLNode:
    root = ParentNode("div", [])
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        btype = block_to_block_type(block)
        match btype:
            case BlockType.PARAGRAPH:
                node = _md_paragraph(block)
            case BlockType.HEADING:
                node = _md_heading(block)
            case BlockType.CODE:
                node = _md_code(block)
            case BlockType.QUOTE:
                node = _md_quote(block)
            case BlockType.UNORDERED_LIST:
                node = _md_ul(block)
            case BlockType.ORDERED_LIST:
                node = _md_ol(block)
            case _:
                raise ValueError(f"unknown block type: {btype}")
        root.children.append(node)
    return root
