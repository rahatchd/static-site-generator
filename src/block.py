import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def _is_heading(txt: str) -> bool:
    return re.match(r"^[#]{1,6} .*", txt)


def _is_code(txt: str) -> bool:
    lines = txt.split("\n")
    match lines:
        case ["```", *_, "```"]:
            return True
        case _:
            return False


def _is_quote(txt: str) -> bool:
    return all(line.startswith(">") for line in txt.split("\n"))


def _is_unordered_list(txt: str) -> bool:
    return all(line.startswith("- ") for line in txt.split("\n"))


def _is_ordered_list(txt: str) -> bool:
    line_starts = [re.findall(r"^([0-9]+)\.", line) for line in txt.split("\n")]
    numbers = list(map(lambda x: int(x[0]) if x and len(x) == 1 else -1, line_starts))
    return numbers == list(range(1, len(line_starts) + 1))


def block_to_block_type(block: str) -> BlockType:
    if _is_heading(block):
        return BlockType.HEADING
    if _is_code(block):
        return BlockType.CODE
    if _is_quote(block):
        return BlockType.QUOTE
    if _is_unordered_list(block):
        return BlockType.UNORDERED_LIST
    if _is_ordered_list(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown: str) -> list[str]:
    return [split.strip() for split in markdown.split("\n\n") if split.strip()]
