from fastapi import APIRouter
from ..rag.retriever import get_retriever
from ..rag.prompts import SQL_GENERATION_PROMPT
from ..sql.service import run_sql_query
from ..utils.config import settings

from openai import OpenAI

router = APIRouter()

# ✅ Initialize OpenAI client once
client = OpenAI(**settings.OPENAI_CLIENT_KWARGS)


@router.post("/chat")
async def ask_chatbot(payload: dict):
    """
    Main chatbot endpoint.
    Steps:
    1. Retrieve context using FAISS retriever
    2. Generate SQL using LLM + context
    3. Execute SQL
    4. Return results
    """

    question = payload.get("question", "")

    if question.strip() == "":
        return {"error": "No question provided."}

    # ✅ 1. Get RAG context
    retriever = get_retriever()
    context_docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in context_docs])

    # ✅ 2. Generate SQL using LLM
    prompt = SQL_GENERATION_PROMPT.format(
        context=context,
        question=question
    )

    try:
        response = client.chat.completions.create(
            model=settings.OPENAI_CHAT_MODEL,
            messages=[
                {"role": "system", "content": "You generate SQL queries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        sql_query = response.choices[0].message.content.strip()

        # remove accidental backticks or markdown
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    except Exception as e:
        return {"error": f"LLM SQL generation failed: {str(e)}"}

    # ✅ 3. Execute SQL safely
    results = run_sql_query(sql_query)

    # ✅ 4. Final output
    return {
        "question": question,
        "generated_sql": sql_query,
        "results": results
    }
