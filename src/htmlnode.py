from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class HTMLNode(ABC):
    tag: str | None = None
    value: str | None = None
    children: list[HTMLNode] | None = None
    props: dict[str, str] | None = None

    @abstractmethod
    def to_html(self) -> str:
        ...

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        return " " + " ".join(key + '="' + value + '"' for key, value in self.props.items())


class LeafNode(HTMLNode):

    def __init__(self, tag: str | None, value: str | None, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Leaf node must have a value")
        if self.tag is None:
            return self.value
        return (
            "<" + self.tag + self.props_to_html() + ">"
            + self.value
            + "</" + self.tag + ">"
        )


class ParentNode(HTMLNode):

    def __init__(self, tag: str, children: list[str], props: dict[str, str] | None = None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("Parent node must have a tag")
        if not self.children:
            raise ValueError("Parent node must have children")
        if not all(isinstance(node, HTMLNode) for node in self.children):
            raise ValueError("Parent node's children must be HTMLNodes")
        return (
            "<" + self.tag + self.props_to_html() + ">"
            + "".join(child.to_html() for child in self.children)
            + "</" + self.tag + ">"
        )
