class HTMLNode:
    pass
class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None,
                 children: list[HTMLNode] | None = None,
                 props: dict[str, str] | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        result: str = ""
        if self.props is not None:
            for k, v in self.props.items():
                result += f" {k}=\"{v}\""
            return result
        else:
            return ""
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
        
