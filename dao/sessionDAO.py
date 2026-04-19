from typing import Any

from utils.db_utils import create_mysql_connection


class SessionDAO:
    def __init__(self, connection: Any) -> None:
        self._connection = connection

    def get_sessions_by_speakername(self, letters: str) -> list[dict[str, Any]]:
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

        cursor = self._connection.cursor()
        try:
            cursor.execute(query, (f'%{search_text}%',))
            return cursor.fetchall()
        finally:
            cursor.close()


def fetch_sessions_by_speaker_name(letters: str) -> list[dict[str, Any]]:
    connection = create_mysql_connection()
    try:
        dao = SessionDAO(connection)
        return dao.get_sessions_by_speakername(letters)
    finally:
        connection.close()
