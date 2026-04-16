from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import os

from ..utils.config import settings

def get_retriever():
    """
    Loads FAISS vectorstore and returns a retriever.
    """
    embeddings = OpenAIEmbeddings(**settings.OPENAI_EMBEDDING_KWARGS)

    if not os.path.exists("vectorstore"):
        raise Exception("❌ Vectorstore not found! Build it before requesting queries.")

    db = FAISS.load_local(
        "vectorstore",
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = db.as_retriever(
        search_kwargs={"k": 4}  # You can tune retrieval depth
    )

    return retriever
