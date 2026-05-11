from dao.attendee_dao import (
    fetch_attendee_name_by_id_in_db,
    update_attendee_in_db,
    add_attendee_in_db,
    fetch_attendees_by_company_id_in_db,
    delete_attendee_in_db,
    fetch_session_ids_by_attendee_id_in_db,
    fetch_attendee_names_by_ids_in_db,
    fetch_session_details_by_ids_in_db
)
from dao.attendee_connection_dao import delete_attendee_in_graph, add_attendee_in_graph, add_attendee_relationship_in_graph, attendee_exists_in_graph, \
    fetch_connected_attendees_in_graph
from dao.company_dao import fetch_company_by_id_in_db
from exceptions.attendee_exceptions import AttendeesAlreadyConnectedError
from utils.constants import MENU_SEPARATOR, ERROR_PREFIX, DATE_FORMAT
from utils.gender_enum import Gender
import datetime
import pymysql


# Show all connected attendees who go to the same session as the given attendee
def show_connected_attendees_same_session() -> None:
    print('Show Connected Attendees in Same Session')
    print(MENU_SEPARATOR)
    attendee_id_text = input('Enter attendee ID: ')
    try:
        attendee_id = int(attendee_id_text)
    except ValueError:
        print(f'{ERROR_PREFIX} Invalid attendee ID\n')
        return
    attendee = fetch_attendee_name_by_id_in_db(attendee_id)
    if not attendee:
        print(f'{ERROR_PREFIX} Attendee does not exist\n')
        return
    connected_rows = fetch_connected_attendees_in_graph(attendee_id)
    if not connected_rows:
        print('No connected attendees found.\n')
        return
    connected_ids = [row['attendeeID'] for row in connected_rows]
    attendee_sessions = set(fetch_session_ids_by_attendee_id_in_db(attendee_id))
    if not attendee_sessions:
        print('This attendee is not registered for any sessions.\n')
        return
    attendee_names = fetch_attendee_names_by_ids_in_db(connected_ids)
    # Gather all session IDs to fetch details in one query
    all_shared_session_ids = set()
    sessions_by_connected = {}
    for cid in connected_ids:
        sessions = set(fetch_session_ids_by_attendee_id_in_db(cid))
        shared_sessions = attendee_sessions & sessions
        if shared_sessions:
            sessions_by_connected[cid] = shared_sessions
            all_shared_session_ids.update(shared_sessions)

    if not sessions_by_connected:
        print('No connected attendees share sessions with the selected attendee.\n')
        return

    # Fetch session details
    session_details = fetch_session_details_by_ids_in_db(list(all_shared_session_ids))

    for cid, shared_sessions in sessions_by_connected.items():
        print(f"{MENU_SEPARATOR}")
        print(f"Connected to {attendee_names.get(cid, 'Unknown')}, attendee ID: {cid}\n")
        print("Session ID | Title | Date | Speaker | Room Name")
        for sid in shared_sessions:
            sid_int = int(sid)
            details = session_details.get(sid_int)
            if details:
                print(f"{sid_int} | {details['sessionTitle']} | {details['speakerName']} | {details['sessionDate']} | {details['roomName']}")
            else:
                print(f"{sid_int} | details unavailable")
    print(f"{MENU_SEPARATOR}\n")

def update_attendee() -> None:
    print('Update Attendee Details')
    print(MENU_SEPARATOR)
    attendee_id = input('Attendee ID to update: ')
    try:
        attendee_id_int = int(attendee_id)
    except ValueError:
        print(f'{ERROR_PREFIX} Attendee ID must be an integer.\n')
        return
    attendee = fetch_attendee_name_by_id_in_db(attendee_id_int)
    if not attendee:
        print(f'{ERROR_PREFIX} Attendee ID: {attendee_id_int} does not exist.\n')
        return
    attendee_name = input('New Name: ')
    attendee_dob = input('New DOB (YYYY-MM-DD): ')
    try:
        datetime.datetime.strptime(attendee_dob, '%Y-%m-%d')
    except ValueError:
        print(f'{ERROR_PREFIX} DOB must be in YYYY-MM-DD format.')
        return
    attendee_gender = input('New Gender (Male/Female): ')
    try:
        gender_enum = Gender(attendee_gender)
    except ValueError:
        print(f'{ERROR_PREFIX} Gender must be Male/Female.')
        return
    company_id = input('New Company ID: ')
    try:
        company_id_int = int(company_id)
    except ValueError:
        print(f'{ERROR_PREFIX} Company ID must be an integer.\n')
        return
    company = fetch_company_by_id_in_db(company_id_int)
    if not company:
        print(f'{ERROR_PREFIX} Company ID: {company_id_int} does not exist.\n')
        return
    try:
        update_attendee_in_db(attendee_id_int, attendee_name, attendee_dob, gender_enum.value, company_id_int)
        print('Attendee details updated successfully.\n')
    except Exception as exc:
        print(f'{ERROR_PREFIX} Could not update attendee: {exc}')

def add_attendee_connection() -> None:
    print('Add Attendee Connection')
    print(MENU_SEPARATOR)
    while True:
        attendee_1 = input('Enter Attendee 1 ID : ')
        attendee_2 = input('Enter Attendee 2 ID : ')
        try:
            attendee_1_int = int(attendee_1)
            attendee_2_int = int(attendee_2)
        except ValueError:
            print(f'{ERROR_PREFIX} Attendee IDs must be numbers\n')
            continue
        if attendee_1_int == attendee_2_int:
            print(f'{ERROR_PREFIX} An attendee cannot connect to himself/herself\n')
            continue
        if fetch_attendee_name_by_id_in_db(attendee_1_int) is None or fetch_attendee_name_by_id_in_db(attendee_2_int) is None:
            print(f'{ERROR_PREFIX} One or both attendee IDs do not exist\n')
            continue
        if not attendee_exists_in_graph(attendee_1_int):
            add_attendee_in_graph(attendee_1_int)
        if not attendee_exists_in_graph(attendee_2_int):
            add_attendee_in_graph(attendee_2_int)
        try:
            add_attendee_relationship_in_graph(attendee_1_int, attendee_2_int)
            print(f'Attendee {attendee_1_int} is now connected to Attendee {attendee_2_int}\n')
        except AttendeesAlreadyConnectedError:
            print(f'{ERROR_PREFIX} These attendees are already connected\n')
            continue
        break


def fetch_connected_attendees() -> None:
    attendee_id_text = input('Enter attendee ID : ')
    try:
        attendee_id = int(attendee_id_text)
    except ValueError:
        print(f'{ERROR_PREFIX} Invalid attendee ID\n')
        return

    attendee = fetch_attendee_name_by_id_in_db(attendee_id)
    exists_in_neo4j = attendee_exists_in_graph(attendee_id)
    if not attendee and not exists_in_neo4j:
        print(f'{ERROR_PREFIX} Attendee does not exist\n')
        return

    rows = fetch_connected_attendees_in_graph(attendee_id)
    if not rows:
        print(f'Attendee Name: {attendee["attendeeName"]}')
        print(f'{MENU_SEPARATOR}')
        print(f'No connections\n')
        return

    connected_attendee_ids = [row['attendeeID'] for row in rows]
    attendee_names = fetch_attendee_names_by_ids_in_db(connected_attendee_ids)

    print('These attendees are connected:')
    for row in rows:
        connected_attendee_id = row['attendeeID']
        attendee_name = attendee_names.get(connected_attendee_id, 'Unknown attendee in MySQL')
        print(f'{connected_attendee_id} | {attendee_name}')
    print()

def add_attendee() -> None:
    print('Add New Attendee')
    print(MENU_SEPARATOR)
    attendee_id_text = input('Attendee ID : ')
    attendee_name = input('Name : ')
    attendee_dob = input('DOB (YYYY-MM-DD) : ')
    attendee_gender = input('Gender : ')
    company_id_text = input('Company ID : ')

    try:
        gender_enum = Gender(attendee_gender)
    except ValueError:
        print(f'{ERROR_PREFIX} Gender must be Male/Female.\n')
        return

    try:
        company_id_int = int(company_id_text)
    except ValueError:
        print(f'{ERROR_PREFIX} Company ID: {company_id_text} does not exist.\n')
        return
    company = fetch_company_by_id_in_db(company_id_int)
    if not company:
        print(f'{ERROR_PREFIX} Company ID: {company_id_int} does not exist.\n')
        return
    try:
        add_attendee_in_db(attendee_id_text, attendee_name, attendee_dob, gender_enum.value, company_id_int)
        print('\nAttendee successfully added.\n')
    except pymysql.err.IntegrityError:
        print(f'{ERROR_PREFIX} Attendee ID: {attendee_id_text} already exists.\n')

def show_attendees_by_company_id() -> None:
    while True:
        try:
            company_id = int(input('Enter company ID : '))
            if company_id <= 0:
                raise ValueError
        except ValueError:
            continue
        company = fetch_company_by_id_in_db(company_id)
        if not company:
            print(f'Company with ID {company_id} doesn\'t exist\n')
            break
        print(f'{company["companyName"]} Attendees')
        attendees = fetch_attendees_by_company_id_in_db(company_id)
        if not attendees:
            print(f'No attendees found for {company["companyName"]}\n')
            break
        for attendee in attendees:
            print(f"{attendee['attendeeName']} | {attendee['attendeeDOB']} | {attendee['sessionTitle']} | {attendee['speakerName']} | {attendee['sessionDate']} | {attendee['roomName']}")
        print()
        break

# Delete attendee from both MySQL and Neo4j
def delete_attendee() -> None:
    print('Delete Attendee')
    print(MENU_SEPARATOR)
    attendee_id = input('Attendee ID to delete: ')
    try:
        attendee_id_int = int(attendee_id)
    except ValueError:
        print(f'{ERROR_PREFIX} Attendee ID must be an integer.\n')
        return
    attendee = fetch_attendee_name_by_id_in_db(attendee_id_int)
    if not attendee:
        print(f'{ERROR_PREFIX} Attendee ID: {attendee_id_int} does not exist.\n')
        return
    confirm = input(f'Are you sure you want to delete attendee {attendee["attendeeName"]} (ID: {attendee_id_int})? (y/n): ').strip().lower()
    if confirm != 'y':
        print('Deletion cancelled.\n')
        return
    try:
        delete_attendee_in_db(attendee_id_int)
        delete_attendee_in_graph(attendee_id_int)
        print('Attendee ID ',attendee_id ,' deleted successfully.\n')
    except Exception as exc:
        print(f'{ERROR_PREFIX} Could not delete attendee: {exc}')
