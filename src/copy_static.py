import os
import shutil

def delete_destination_contents(path):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                delete_destination_contents(item_path)
                if not os.listdir(item_path):
                    os.rmdir(item_path)
        except Exception as e:
            print(f"Error deleting {item_path}: {e}")

def copy_source_content_to_destination(path, destination):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        new_subdir = os.path.join(destination, item)
        print(f"DEBUG copying {item_path} -> {destination}")
        try:
            if os.path.isfile(item_path): 
                shutil.copy(item_path, destination)

            elif os.path.isdir(item_path):
                if not os.path.exists(new_subdir):
                    os.mkdir(new_subdir)

                copy_source_content_to_destination(item_path, new_subdir)

        except Exception as e:
            print(f"Error copying {item_path}: {e}")