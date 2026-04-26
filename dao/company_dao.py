from typing import Any

from utils.db_utils import create_mysql_connection

def fetch_company_by_id_in_db(company_id: int) -> dict[str, Any]:
    query = 'SELECT * FROM company WHERE companyID = %s'
    connection = create_mysql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (company_id,))
            return cursor.fetchone()
    finally:
        connection.close()
