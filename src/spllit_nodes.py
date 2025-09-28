from textnode import TextNode, TextType

def split_node_delimiter(old_nodes: list[TextNode],
                         delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        st: list[str] = node.text.split(delimiter)
        #if len(st) % 2 == 0:
        #    raise ValueError("Invalid Markdown syntax")
        new_text: list[str] = list(filter(lambda x: x != "", st))
        to_be_added: list[TextNode] = []

        for text in new_text:
            if text.startswith(" ") or text.endswith(" ") or node.text_type != TextType.TEXT:
                to_be_added.append(TextNode(text, node.text_type))
            else:
                to_be_added.append(TextNode(text, text_type))
        new_nodes.extend(to_be_added)
    return new_nodes

def extract_markdown_images(txt: str) -> list[tuple[str, str]]:
	alt_text: str = ""
	link: str = ""
	result: list[tuple[str, str]] = []
	i = 0
	for i in range(len(txt)):
		if txt[i] == "!" and txt[i + 1] == "[":
			j = i
			while txt[j] != "]":
				j += 1
			i += 2

			alt_text = txt[i:j]
			i = j
		elif txt[i] == "(":
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
	i = 0
	for i in range(len(txt)):
		if txt[i] == "[":
			j = i
			while txt[j] != "]":
				j += 1
			i += 1

			alt_text = txt[i:j]
			i = j
		elif txt[i] == "(":
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
    nodes_to_use: list[TextNode] = []
    alt: str = []
    lin: str = []
    result = []
    val = []

    for old_node in old_nodes:
        val.extend(extract_markdown_links(old_node.text))

    print(result)


node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
)

split_nodes_link([node])
    
