import mysql.connector
from ..utils.config import settings
import os

def generate_schema_markdown():
    """
    Reads the live MySQL database schema & generates a schema markdown file.
    This runs automatically at server startup.
    """

    conn = mysql.connector.connect(
        host=settings.DB_HOST,
        user=settings.DB_USER,
        password=settings.DB_PASS,
        database=settings.DB_NAME
    )

    cursor = conn.cursor()

    markdown_output = "# 📘 Auto‑Generated Database Schema\n\n"
    markdown_output += "This file is generated automatically every time the server starts.\n\n"

    # Fetch all tables
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    for (table_name,) in tables:
        markdown_output += f"## Table: `{table_name}`\n\n"

        # Get column definitions
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()

        markdown_output += "### Columns:\n"
        for col in columns:
            col_name, col_type = col[0], col[1]
            markdown_output += f"- **{col_name}**: {col_type}\n"

        markdown_output += "\n---\n\n"

    cursor.close()
    conn.close()

    # Create knowledge_base folder if not exists
    os.makedirs("knowledge_base", exist_ok=True)

    file_path = "knowledge_base/schema_generated.md"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown_output)

    print("✅ Auto‑generated schema file created:", file_path)
    return file_path
