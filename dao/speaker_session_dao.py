from typing import Any

from utils.db_utils import create_mysql_connection


def fetch_sessions_by_speaker_name(letters: str) -> list[dict[str, Any]]:
    search_text = letters.strip()
    if not search_text:
        return []

    query = (
        'SELECT s.speakerName, s.sessionTitle, r.roomName '
        'FROM session s '
        'JOIN room r ON r.roomID = s.roomID '
        'WHERE s.speakerName LIKE %s '
        'ORDER BY s.speakerName, s.sessionDate, s.sessionTitle'
    )

    connection = create_mysql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (f'%{search_text}%',))
            return cursor.fetchall()
    finally:
        connection.close()
