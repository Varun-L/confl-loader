import os
from pathlib import Path
from langchain_community.document_loaders import ConfluenceLoader
from dotenv import load_dotenv

load_dotenv()

def create_local_files(documents, output_folder):
    """
    Creates local files from Confluence documents and saves them in the specified output folder.
    """
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    for document in documents:
        file_name = f"{document.metadata['title']}.txt"
        file_path = output_path / file_name

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(document.page_content)
        except Exception as e:
            print(f"Error writing file {file_name}: {e}")

def main():
    space_key = "SPACE_KEY"
    output_folder = "SK_confluence_data" 

    loader = ConfluenceLoader(
        url=os.getenv("URL"),
        username=os.getenv("USERNAME"),
        api_key=os.getenv("API_KEY"),
        space_key=space_key,
        include_attachments=False,
        limit=100,
        max_pages=4000,
    )
    documents = loader.load()

    create_local_files(documents, output_folder)

if __name__ == "__main__":
    main()
