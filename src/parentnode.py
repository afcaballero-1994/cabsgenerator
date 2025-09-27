from htmlnode import HTMLNode

class ParentNode(HTMLNode):
	def __init__(
		self, tag: str, children: list[HTMLNode],
		props: dict[str, str] | None = None):
		super().__init__(tag, None, children, props)

	def to_html(self) -> str:
		if self.tag is None:
			raise ValueError("Tag value is mandatory")
		if self.children is None:
			raise ValueError("There is no children")
		
		def loop(cs: list[HTMLNode], result: str) -> str:
			if not cs:
				return result
			else:
				return loop(cs[1:], result + cs[0].to_html())
		result: str = loop(self.children, "")

		return f"<{self.tag}{self.props_to_html()}>{result}</{self.tag}>"