import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            new_line = line[2:]
            return new_line.strip()
    raise Exception("markdown has no valid title heading")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    with open(template_path, 'r', encoding="utf-8") as f:
        html_content = f.read()
    
    html_string = markdown_to_html_node(md_content).to_html()
    title_page = extract_title(md_content)

    new_content = html_content.replace("{{ Title }}", title_page)
    new_content = new_content.replace("{{ Content }}", html_string)
    new_content = new_content.replace('href="/', 'href="' + basepath)
    new_content = new_content.replace('src="/', 'src="' + basepath)

    dir_path = os.path.dirname(dest_path)
    os.makedirs(dir_path, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(new_content)

def generate_page_recursively(dir_path_content, template_path, dest_dir_path, basepath):
    
    contents = os.listdir(dir_path_content)
    
    for content in contents:
        content_path = os.path.join(dir_path_content, content)
        content_extension = os.path.splitext(content_path)[1]
        if os.path.isfile(content_path):
            if content_extension == ".md":
                rel_content_path = os.path.relpath(content_path, dir_path_content)
                dest_path = os.path.join(dest_dir_path, rel_content_path)
                dest_path = Path(dest_path).with_suffix(".html")
                generate_page(content_path, template_path, dest_path, basepath) 
               

        elif os.path.isdir(content_path):
            rel_content_path = os.path.relpath(content_path, dir_path_content)
            dest_path = os.path.join(dest_dir_path, rel_content_path)
            generate_page_recursively(content_path, template_path, dest_path, basepath)









    
