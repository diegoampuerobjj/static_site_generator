import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []

    for old_node in old_nodes:

        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
        else:
            parts = old_node.text.split(delimiter)

            if len(parts) % 2 == 0:
                raise Exception("Invalid markdown syntax. Maybe close the delimiter?")
            
            for index, part in enumerate(parts):
                if part == "":
                    continue
                if index % 2 == 0:
                    new_node = TextNode(part, TextType.TEXT)
                    result.append(new_node)
                else:
                    new_node = TextNode(part, text_type)
                    result.append(new_node)

    return result

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        current_text = old_node.text
        images = extract_markdown_images(current_text)

        if len(images) == 0:
            if current_text != "":
                new_nodes.append(old_node)
            continue

        for alt, url in images:
            sections = current_text.split(f"![{alt}]({url})", 1)
            before = sections[0]
            after = sections[1]

            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            current_text = after

        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        link_extracted = extract_markdown_links(old_node.text)
        current_text = old_node.text

        if len(link_extracted) == 0:
            new_nodes.append(old_node)
            continue
        
        for a, url in link_extracted:
            sections = current_text.split(f"[{a}]({url})", 1)
            before = sections[0]
            after = sections[1]

            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))
            
            new_nodes.append(TextNode(a, TextType.LINK, url))

            current_text = after

        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

