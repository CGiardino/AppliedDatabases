from typing import Any

import pymysql
from neo4j import GraphDatabase

from config.db_config import DB_CONFIG, NEO4J_CONFIG

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


def create_neo4j_driver() -> Any:
    return GraphDatabase.driver(
        NEO4J_CONFIG['uri'],
        auth=(NEO4J_CONFIG['user'], NEO4J_CONFIG['password']),
    )

