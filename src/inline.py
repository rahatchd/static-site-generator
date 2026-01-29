import re
from functools import partial
from typing import Pattern, Callable

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        splits = node.text.split(delimiter)
        if len(splits) % 2 != 1:
            raise ValueError("Invalid markdown. Unclosed delimiter.")

        for idx, txt in enumerate(splits):
            txt_type = TextType.TEXT if idx % 2 == 0 else text_type
            new_nodes.append(TextNode(txt, txt_type))
    return new_nodes


_IMAGE_REGEX = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(_IMAGE_REGEX, text)


_LINK_REGEX = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(_LINK_REGEX, text)


def _split_nodes_regex(
    old_nodes: list[TextNode],
    pattern: Pattern,
    text_type: TextType,
) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        splits = re.split(pattern, node.text)

        display_txt = ""
        for idx, txt in enumerate(splits):
            match idx % 3:
                case 1:
                    display_txt = txt
                case 2:
                    url = txt
                    new_nodes.append(TextNode(display_txt, text_type, url))
                case _:
                    if txt:
                        new_nodes.append(TextNode(txt, TextType.TEXT))
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_regex(old_nodes, _IMAGE_REGEX, TextType.IMAGE)


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_regex(old_nodes, _LINK_REGEX, TextType.LINK)


def text_to_textnodes(text: str) -> list[TextNode]:
    if not text:
        return [TextNode(text, TextType.TEXT)]
    nodes = [TextNode(text, TextType.TEXT)]
    for split_fn in (
        partial(split_nodes_delimiter, delimiter="**", text_type=TextType.BOLD),
        partial(split_nodes_delimiter, delimiter="_", text_type=TextType.ITALIC),
        partial(split_nodes_delimiter, delimiter="`", text_type=TextType.CODE),
        split_nodes_image,
        split_nodes_link,
    ):
        nodes = split_fn(nodes)
    return nodes
