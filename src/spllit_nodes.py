from textnode import TextNode, TextType

def split_node_delimiter(old_nodes: list[TextNode],
                         delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(txt: str) -> list[tuple[str, str]]:
    alt_text: str = ""
    link: str = ""
    result: list[tuple[str, str]] = []
    i = 0
    for i in range(len(txt)):
        if i + 1 >= len(txt):
            continue
        if txt[i] == "!" and txt[i + 1] == "[":
            j = i
            while txt[j] != "]":
                j += 1
            i += 2

            alt_text = txt[i:j]
            i = j + 1
            if txt[i] == "(":

                j = i
                while txt[j] != ")":
                    j += 1
                i += 1
                link = txt[i:j]
                i = j
                i += 1

            result.append((alt_text, link))
    
    return result

def extract_markdown_links(txt: str) -> list[tuple[str, str]]:
    alt_text: str = ""
    link: str = ""
    result: list[tuple[str, str]] = []
    for i in range(len(txt)):
        if txt[i] == "[" and txt[i - 1] != "!":
            j = i
            while txt[j] != "]":
                j += 1
            i += 1

            alt_text = txt[i:j]
            i = j + 1
            if txt[i] == "(":
                j = i
                while txt[j] != ")":
                    j += 1
                i += 1
                link = txt[i:j]
                i = j
                i += 1

            result.append((alt_text, link))
    
    return result

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    if old_nodes is None:
        return

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        og_text: str = node.text

        links: list[tuple[str, str]] = extract_markdown_links(og_text)

        if not links:
            new_nodes.append(node)
            continue
        for link in links:
            splitted = og_text.split(f"[{link[0]}]({link[1]})")

            if len(splitted) != 2:
                raise ValueError("Not valid Markdown for links")
            
            if splitted[0] != "":
                new_nodes.append(TextNode(splitted[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

            og_text = splitted[1]
        if og_text != "":
            new_nodes.append(TextNode(og_text, TextType.TEXT))

    return new_nodes
    
def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        og_text: str = node.text

        images: list[tuple[str, str]] = extract_markdown_images(og_text)

        if not images:
            new_nodes.append(node)
            continue
        for image in images:
            splitted = og_text.split(f"![{image[0]}]({image[1]})")

            if len(splitted) != 2:
                raise ValueError("Not valid Markdown for images")
            
            if splitted[0] != "":
                new_nodes.append(TextNode(splitted[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

            og_text = splitted[1]
        if og_text != "":
            new_nodes.append(TextNode(og_text, TextType.TEXT))

    return new_nodes
    
def text_to_text_nodes(txt: str) -> list[TextNode]:
    result = [TextNode(txt, TextType.TEXT)]
    
    result = split_node_delimiter(result, "**", TextType.BOLD)
    result = split_node_delimiter(result, "_", TextType.ITALIC)
    result = split_node_delimiter(result, "`", TextType.CODE)
    result = split_nodes_image(result)
    result = split_nodes_link(result)

    return result