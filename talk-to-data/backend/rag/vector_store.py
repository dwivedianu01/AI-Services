import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from .generate_schema_md import generate_schema_markdown
from ..utils.config import settings


def build_vectorstore():
    """
    Auto-generates database documentation and builds vectorstore from it.
    Runs automatically at FastAPI startup.
    """

    # ✅ Step 1: Generate schema docs
    schema_path = generate_schema_markdown()

    # ✅ Step 2: Load all .md files in knowledge_base folder
    docs = []
    for file in os.listdir("knowledge_base"):
        if file.endswith(".md"):
            with open(f"knowledge_base/{file}", "r", encoding="utf-8") as f:
                docs.append(f.read())

    if not docs:
        raise Exception("❌ No documentation found in knowledge_base folder.")

    # ✅ Step 3: Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    documents = splitter.create_documents(docs)

    # ✅ Step 4: Create vector embeddings
    embeddings = OpenAIEmbeddings(**settings.OPENAI_EMBEDDING_KWARGS)

    # ✅ Step 5: Build FAISS vectorstore
    db = FAISS.from_documents(documents, embeddings)

    # ✅ Ensure vectorstore directory exists
    os.makedirs("vectorstore", exist_ok=True)

    db.save_local("vectorstore")

    print("✅ Vectorstore successfully built and saved to: vectorstore/")


if __name__ == "__main__":
    build_vectorstore()
