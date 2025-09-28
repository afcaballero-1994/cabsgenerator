from enum import Enum
from htmlnode import HTMLNode
from parentnode import ParentNode
from spllit_nodes import *
from textnode import *
from leafnode import LeafNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    result: list[str] = markdown.split("\n\n")
    result = list(map(lambda x: x.strip("\n "), result))
    result = list(filter(lambda x: x != "", result))

    return result

def block_to_block_type(block: str) -> BlockType:
    lines: list[str] = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1:
        if lines[0].startswith("```") and lines[-1].endswith("```"):
            return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
            return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
            return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            return BlockType.OLIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks: list[str] = markdown_to_blocks(markdown)
    parent: HTMLNode = ParentNode("div", [])

    for block in blocks:
        bltype: BlockType = block_to_block_type(block)
        match bltype:
            case BlockType.PARAGRAPH:
                pblock: ParentNode = ParentNode("p", [])

                nodes: list[TextNode] = text_to_text_nodes(block.replace("\n", " "))
                for node in nodes:
                    pblock.children.append(text_node_to_html_node(node))
                parent.children.append(pblock)
            case BlockType.CODE:
                pblock: ParentNode = ParentNode("pre", [])

                node = TextNode(block.lstrip("`\n").rstrip("`"), TextType.CODE)
                hnode = text_node_to_html_node(node)
                pblock.children.append(hnode)
                parent.children.append(pblock)

    return parent