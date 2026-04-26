from typing import Any

from utils.db_utils import create_mysql_connection

def fetch_rooms_in_db()-> list[dict[str, Any]]:
    query = 'SELECT * FROM room'
    connection = create_mysql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    finally:
        connection.close()