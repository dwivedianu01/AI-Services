import os
from utils.pdf_reader import extract_text_from_pdf
from utils.rag_utils import build_vector_store, rag_query

# Step 1: Load all PDFs from a folder
folder_path = "test-data"   # create a folder named 'documents' and put your PDFs inside
all_text = ""

for file in os.listdir(folder_path):
    if file.endswith(".pdf"):
        file_path = os.path.join(folder_path, file)
        print(f"Loading {file_path}...")
        all_text += extract_text_from_pdf(file_path) + "\n"

# Step 2: Build Vector Store from all documents
vector_store = build_vector_store(all_text)

# Step 3: Ask Questions across all PDFs


question = input("Enter your question: ")
answer = rag_query(vector_store, question)

print("Q:", question)
print("A:", answer)