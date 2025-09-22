from textnode import TextNode
from textnode import TextType

def main() -> None:
    new = TextNode("This is some anchor text", TextType.LINK, "boot.dev")
    print(new)

main()
