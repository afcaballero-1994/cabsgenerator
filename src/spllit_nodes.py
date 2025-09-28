from textnode import TextNode, TextType

def split_node_delimiter(old_nodes: list[TextNode],
                         delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        st: list[str] = node.text.split(delimiter)
        if len(st) % 2 == 0:
            raise ValueError("Invalid Markdown syntax")
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
    new_nodes: list[TextNode] = []

    for node in old_nodes:
    	if node.text_type != TextType.TEXT:
    		new_nodes.append(node)
    		continue
    	og_text: str = node.text

    	links: list[tuple[str, str]] = extract_markdown_links(og_text)

    	if not links:
    		node.append(new_nodes)
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
    		node.append(new_nodes)
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
    
