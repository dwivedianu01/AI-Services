import mysql.connector
from mysql.connector import Error
from .config import settings


def get_connection():
    """
    Creates and returns a new MySQL database connection
    using credentials from config.ini.
    """
    try:
        conn = mysql.connector.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASS,
            database=settings.DB_NAME
        )
        return conn

    except Error as e:
        print(f"❌ Database connection error: {e}")
        return None


def execute_query(query, params=None, fetch=False):
    """
    Executes a SQL query safely.

    :param query: SQL query string
    :param params: optional tuple of parameters for prepared statements
    :param fetch: boolean → if True, returns results
    """
    conn = get_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())

        if fetch:
            result = cursor.fetchall()
            conn.close()
            return result

        conn.commit()
        conn.close()
        return True

    except Error as e:
        print(f"❌ SQL execution error: {e}")
        conn.close()
        return None
