import re
from mysql.connector import Error
from ..utils.db_connection import get_connection


# -------------------------------
# ✅ SQL Safety Checker
# -------------------------------
def is_sql_safe(query: str) -> bool:
    """
    Ensures the generated SQL is safe to execute.
    Only SELECT queries are allowed.
    Dangerous operations like DROP/DELETE/UPDATE without WHERE are blocked.
    """

    unsafe_patterns = [
        r"\bDROP\b",
        r"\bTRUNCATE\b",
        r"\bALTER\b",
        r"\bDELETE\b(?!.*WHERE)",   # DELETE without WHERE → dangerous
        r"\bUPDATE\b(?!.*WHERE)",   # UPDATE without WHERE → dangerous
        r"\bINSERT\b(?!.*INTO)",    # malformed or unsafe INSERT
    ]

    upper_query = query.upper().strip()

    # ✅ Only allow SELECT queries
    if not upper_query.startswith("SELECT"):
        print("❌ Blocked non-SELECT query:", query)
        return False

    # ✅ Check for dangerous operations
    for pattern in unsafe_patterns:
        if re.search(pattern, upper_query):
            print("❌ Unsafe SQL blocked:", query)
            return False

    return True


# -------------------------------
# ✅ SQL Executor (Safe)
# -------------------------------
def run_sql_query(sql: str):
    """
    Executes safe SELECT SQL queries.
    Returns list of dict rows OR an error dictionary.
    """

    # ✅ Step 1: Safety validation
    if not is_sql_safe(sql):
        return {
            "error": "Unsafe or restricted SQL query detected. Only safe SELECT queries are allowed."
        }

    # ✅ Step 2: Connect to database
    conn = get_connection()
    if conn is None:
        return {"error": "Unable to connect to database."}

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results

    except Error as e:
        print(f"❌ SQL execution error: {e}")
        return {"error": str(e)}
