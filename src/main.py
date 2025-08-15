import os
from process_repos import execute
from unzip_all_json_gz import unzip_all_json_gz

unzip_all_json_gz()

folder_path = "data_unzipped"

for file_name in os.listdir(folder_path):
    if file_name.endswith(".json"):
        file_path = os.path.join(folder_path, file_name)
        execute(file_path, file_name)
