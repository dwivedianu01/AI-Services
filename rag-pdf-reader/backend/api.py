import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.pdf_reader import extract_text_from_pdf
from utils.rag_utils import build_vector_store, rag_query

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load and index all PDFs in folder at startup
folder_path = "test-data"
all_text = ""
for file in os.listdir(folder_path):
    if file.endswith(".pdf"):
        file_path = os.path.join(folder_path, file)
        print(f"Indexing {file_path}...")
        all_text += extract_text_from_pdf(file_path) + "\n"

vector_store = build_vector_store(all_text)

# Request model
class QuestionRequest(BaseModel):
    question: str

@app.post("/chat")
def ask_question(req: QuestionRequest):
    answer = rag_query(vector_store, req.question)
    return {"question": req.question, "answer": answer}