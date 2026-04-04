from openai import OpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import config

# Initialize OpenAI client with key from config
client = OpenAI(api_key=config.OPENAI_API_KEY)

def build_vector_store(text):
    # Use RecursiveCharacterTextSplitter (new API)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_text(text)

    embeddings = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)
    vector_store = FAISS.from_texts(chunks, embeddings)
    return vector_store

def rag_query(vector_store, query):
    docs = vector_store.similarity_search(query, k=3)
    context = "\n".join([d.page_content for d in docs])

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Answer based on context:\n{context}\n\nQuestion: {query}"}]
    )
    return response.choices[0].message.content