from typing import Any

from utils.db_utils import create_mysql_connection

def fetch_attendees_by_company_id_in_db(company_id: int) -> list[dict[str, Any]]:
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
        
def add_attendee_in_db(attendee_id: str, attendee_name: str, attendee_dob: str, attendee_gender:str, attendee_company_id: int) -> None:
    query = 'INSERT INTO attendee (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID) VALUES (%s, %s, %s, %s, %s)'
    connection = create_mysql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (attendee_id, attendee_name, attendee_dob, attendee_gender, attendee_company_id))
            connection.commit()
    finally:
        connection.close()


def fetch_attendee_name_by_id_in_db(attendee_id: int):
    query = 'SELECT attendeeName FROM attendee WHERE attendeeID = %s LIMIT 1'
    connection = create_mysql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (attendee_id,))
            return cursor.fetchone()
    finally:
        connection.close()


def fetch_attendee_names_by_ids_in_db(attendee_ids: list[int]) -> dict[int, str]:
    if not attendee_ids:
        return {}

    placeholders = ', '.join(['%s'] * len(attendee_ids))
    query = f'SELECT attendeeID, attendeeName FROM attendee WHERE attendeeID IN ({placeholders})'

    connection = create_mysql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, tuple(attendee_ids))
            rows = cursor.fetchall()
            return {row['attendeeID']: row['attendeeName'] for row in rows}
    finally:
        connection.close()

def update_attendee_in_db(attendee_id: int, attendee_name: str, attendee_dob: str, attendee_gender: str, attendee_company_id: int) -> None:
    """Update attendee details in the database."""
    query = (
        'UPDATE attendee SET attendeeName = %s, attendeeDOB = %s, attendeeGender = %s, attendeeCompanyID = %s '
        'WHERE attendeeID = %s'
    )
    connection = create_mysql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (attendee_name, attendee_dob, attendee_gender, attendee_company_id, attendee_id))
            connection.commit()
    finally:
        connection.close()
