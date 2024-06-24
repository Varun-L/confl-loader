import os
from pathlib import Path
from langchain_community.document_loaders import ConfluenceLoader
from dotenv import load_dotenv
import concurrent.futures

load_dotenv()

 
def write_file(document, output_path):
    file_name = f"{document.metadata['title'].replace('/','_')}.txt"
    file_path = output_path / file_name

    # If a file with the same name already exists, append the ID to the filename
    if file_path.exists():
        file_name = f"{document.metadata['title']}_{document.metadata['id']}.txt"
        file_path = output_path / file_name

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(document.metadata['title'] + "\n")
            file.write(document.page_content)
            file.write("\nSource: "+document.metadata['source'])
    except Exception as e:
        print(f"Error writing file {file_name}: {e}")

def create_local_files(documents, output_folder):
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(write_file, documents, [output_path]*len(documents))

def main():
    space_key = "SPACE_KEY"
    output_folder = "sk_confluence_data_1" 

    loader = ConfluenceLoader(
        url=os.getenv("URL"),
        username=os.getenv("USERNAME"),
        api_key=os.getenv("API_KEY"),
        space_key=space_key,
        # page_ids=["690489589"],
        include_attachments=False,
        limit=100,
        max_pages=4000,
    )
    documents = loader.load()

    create_local_files(documents, output_folder)

if __name__ == "__main__":
    main()
