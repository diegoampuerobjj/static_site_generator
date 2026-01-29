from copy_static import delete_destination_contents, copy_source_content_to_destination
from content_generation import generate_page_recursively
import sys

dir_path_static = "./static"
dir_path_docs = "./docs"
dir_path_content = "./content"
template_path = "./template.html"
default_basepath = "/"

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else default_basepath
    print("Deleting docs directory...")
    delete_destination_contents(dir_path_docs)

    print("Copying static files to docs directory...")
    copy_source_content_to_destination(dir_path_static, dir_path_docs)

    print("Generating page...")
    generate_page_recursively(
        dir_path_content,
        template_path,
        dir_path_docs,
        basepath
    )


if __name__ == '__main__':
    main()

