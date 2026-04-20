from typing import Any

from utils.db_utils import create_mysql_connection

def fetch_attendees_by_company_id(company_id: int) -> list[dict[str, Any]]:
    query = ('SELECT a.attendeeName, a.attendeeDOB, s.sessionTitle, s.speakerName, rm.roomName FROM attendee a '
             'join registration r on (a.attendeeID = r.attendeeID)'
             'join session s on (r.sessionID = s.sessionID)'
             'join room rm on (s.roomID = rm.roomID)'
             'WHERE a.attendeeCompanyID = %s '
             'ORDER BY a.attendeeName, a.attendeeDOB')
    connection = create_mysql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (company_id,))
            return cursor.fetchall()
    finally:
        connection.close()