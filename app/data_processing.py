import os
import shutil
from git import Repo

def get_markdown_files(repo_url):
    temp_dir = "temp"
    data_dir = "data"

    # Clone the repository
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    Repo.clone_from(repo_url, temp_dir)

    # Extract markdown files
    markdown_files = []
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    for root, dirs, files in os.walk(temp_dir, topdown=False):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                destination = os.path.join(data_dir, file)
                base, ext = os.path.splitext(file)
                counter = 1
                while os.path.exists(destination):
                    destination = os.path.join(data_dir, f"{base}_{counter}{ext}")
                    counter += 1
                shutil.move(full_path, destination)
                markdown_files.append(destination)

    return markdown_files
