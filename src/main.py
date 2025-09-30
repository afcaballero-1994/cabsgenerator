from textnode import TextNode
from textnode import TextType
from markdown_to_blocks import markdown_to_html_node

import os, shutil

def extrac_title(markdown: str) -> str:

    sp = markdown.split("\n")

    if sp[0].startswith("# "):
        return sp[0][2:]
    else:
        raise ValueError("Not valid header file")

def generate_page(from_path: str, template_path: str, dst_path: str):
    print(f"generating from: {from_path} using: {template_path} to: {dst_path}")

    with open(from_path) as mark, open(template_path) as templ, open(dst_path, "w") as ds:
        markdown = mark.read()
        templ_html = templ.read()
        html_node = markdown_to_html_node(markdown)

        title = extrac_title(markdown)
        print(2, title)

        htmtow = templ_html.replace("{{ Content }}", html_node.to_html()).replace("{{ Title }}", title)
        ds.write(htmtow)

def generate_pages_recursive(dir_path_content: str, template_path: str, dst_dir_path: str):

    def loop(dirs: [str], c: str):
        cd = list(map(lambda x: os.path.join(c,x), dirs))

        for d in cd:
            if os.path.isfile(d):
                print(f"about to generate: {d}")
                cpath = d.replace(dir_path_content, dst_dir_path).replace(".md", ".html")
                generate_page(d, template_path, cpath)
            else:
                dsc = dst_dir_path + d[len(dir_path_content):]

                if not os.path.exists(dsc):
                    print(f"creating dir: {dsc}")
                    os.mkdir(dsc)
                loop(os.listdir(d), d)
    loop(os.listdir(dir_path_content), dir_path_content)

def copy_pub():
    src: str = "./static"
    dst: str = "./public"
    if os.path.exists(dst):
        print(f"deleting: {dst}")
        shutil.rmtree(dst)

    print(f"creating dir: {dst}")
    os.mkdir(dst)

    def loop(dirs: list[str], c: str):
        cd = list(map(lambda x: os.path.join(c, x), dirs))
        
        for d in cd:
            if os.path.isfile(d):
                print(f"about to copy: {d}")
                cpath = d.replace(src, dst)
                shutil.copy(d, cpath)
            else:
                dsc = dst + d[len(src):]
                if not os.path.exists(dsc):
                    print(f"creating: {dsc}")
                    os.mkdir(dsc)
                loop(os.listdir(d), d)


    loop(os.listdir(src), src)

def main() -> None:
    copy_pub()
    generate_pages_recursive("./content", "./template.html", "./public")

main()
