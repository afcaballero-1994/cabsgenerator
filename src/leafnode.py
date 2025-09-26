from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None,
                 value: str,
                 props: dict[str, str] | None = None):
        super().__init__(tag, value, None, props)


    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode should have a value")
        if self.tag == None:
            return f"{self.value}"

        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"
