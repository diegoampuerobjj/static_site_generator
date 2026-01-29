from enum import Enum
from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ORDERED_LIST = "ordered_list"
    UNORDERED_LIST = "unordered_list"

def markdown_to_blocks(text):
    raw_blocks = text.split("\n\n")
    filtered_blocks = []
    for block in raw_blocks:
        block = block.strip()
        if block == "":
            continue
        # NEW: if this block has multiple heading lines, split them
        lines = block.split("\n")
        current = []
        for line in lines:
            if line.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
                # if we already collected some lines, flush them as a block
                if current:
                    filtered_blocks.append("\n".join(current).strip())
                    current = []
                # this heading line becomes its own block
                filtered_blocks.append(line.strip())
            else:
                current.append(line)
        if current:
            filtered_blocks.append("\n".join(current).strip())
    return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
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
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    children = []
    splitted = markdown_to_blocks(markdown)

    for block in splitted:
        html_node = block_to_html_node(block)
        children.append(html_node)

    return ParentNode("div", children) 

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text: str): 
    nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in nodes]
    return html_nodes

def heading_to_html_node(block): 
    level = len(block) - len(block.lstrip("#")) 
    text_part = block[level:]
    cleaned = text_part.strip()
    children_nodes = text_to_children(cleaned)
    return ParentNode(f"h{level}", children_nodes)

def paragraph_to_html_node(block): 
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def code_to_html_node(block): 
    parts = block.split("```")
    inner = parts[1].lstrip("\n")

    text_node = TextNode(inner, TextType.TEXT)
    code_child = text_node_to_html_node(text_node)

    code_node = ParentNode("code", [code_child])
    pre_node = ParentNode("pre", [code_node])
    return pre_node

def quote_to_html_node(block): 
    lines = block.split("\n")
    stripped_lines = []
    
    for line in lines:
        line = line.strip()
        
        if line.startswith(">"):
            line = line[1:]
            line = line.lstrip()
        
        if line:
            stripped_lines.append(line)
    
    quote_text = " ".join(stripped_lines).strip()
    children_nodes = text_to_children(quote_text)
    
    quote_node = ParentNode(f"blockquote", children_nodes)
    return quote_node

def unordered_list_to_html_node(block): 
    li_nodes = []
    lines = block.split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue
        elif line.startswith("- "):
            item_text = line[2:]
        elif line.startswith("* "):
            item_text = line[2:]
        else:
            continue
        
        li_children = text_to_children(item_text)
        li_node = ParentNode("li", li_children)
        li_nodes.append(li_node)
    
    ul_node = ParentNode("ul", li_nodes)
    return ul_node

def ordered_list_to_html_node(block): 
    ol_nodes = []
    lines = block.split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue
        i = 0
        while i < len(line) and line[i].isdigit():
            i += 1
        if i == 0:
            continue
        if i + 2 >= len(line) or line[i] != "." or line[i + 1] != " ":
            continue

        item_text = line[i + 2:]
        
        ol_children = text_to_children(item_text)
        li_node = ParentNode("li", ol_children)
        ol_nodes.append(li_node)
    
    ol_node = ParentNode("ol", ol_nodes)
    return ol_node


            