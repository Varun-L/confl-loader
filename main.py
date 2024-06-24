from langchain_community.document_loaders import ConfluenceLoader
from dotenv import load_dotenv
import os

load_dotenv()

space_key = "SPACE_KEY"
loader = ConfluenceLoader(
    url=os.getenv("URL"), username=os.getenv("USERNAME"), api_key=os.getenv("API_KEY"),
    page_ids=["PI"], include_attachments=False, limit=100, max_pages=4000
)
# documents = loader.load(space_key="SPACE", include_attachments=False, limit=100)
documents = loader.load()

for document in documents:
    print(document.page_content)
    print(document.metadata["title"])
    print(document.metadata["id"])
    print(document.metadata["source"])
    print(document.metadata["when"])