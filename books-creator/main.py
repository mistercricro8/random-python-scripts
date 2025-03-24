import os
import requests


def list_folders(directory):
    return [
        f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))
    ]


def select_folder(folders):
    for i, folder in enumerate(folders, 1):
        print(f"{i}. {folder}")

    while True:
        choice = input("n: ")
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(folders):
                return folders[choice - 1]


def upload_pdfs(folder_path):
    base_url = "http://localhost:8000/api"
    category_id = 56
    # requests.post(f"{base_url}/categories/create", data={"name": "cat_name"})
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        title = (
            os.path.splitext(file_name)[0]
            .replace("_", " ")
            .replace("-", " ")
            .replace(".", " ")
        )

        with open(file_path, "rb") as file:
            files = {"file": file}
            data = {"name": title, "category_id": category_id}

            response = requests.post(f"{base_url}/books/create", files=files, data=data)
            print(f"{file_name}: {response.status_code}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folders = list_folders(script_dir)

    if folders:
        selected_folder = select_folder(folders)
        upload_pdfs(os.path.join(script_dir, selected_folder))
