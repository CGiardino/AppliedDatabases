from typing import Any

from config.db_config import DB_CONFIG
import pymysql 

def create_mysql_connection() -> Any:
    try:
        return pymysql.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            cursorclass=pymysql.cursors.DictCursor,
        )
    except RuntimeError as exc:
        if 'cryptography' in str(exc):
            raise RuntimeError(
                "'cryptography' is required for MySQL auth. Install with: pip install -r requirements.txt"
            ) from exc
        raise
