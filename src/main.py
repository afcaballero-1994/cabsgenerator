from textnode import TextNode
from textnode import Text_type

def main() -> None:
    new = TextNode("This is some anchor text", Text_type.LINK, "boot.dev")
    print(new)

main()
