from controllers.attendee_controller import update_attendee
from dao.speaker_session_dao import fetch_sessions_by_speaker_name
from dao.company_dao import fetch_company_by_id
from dao.attendee_dao import fetch_attendees_by_company_id, add_attendee, fetch_attendee_name_by_id, fetch_attendee_names_by_ids
from dao.attendee_connection_dao import fetch_connected_attendees, attendee_exists_in_graph, add_attendee_relationship, add_attendee_in_graph
import pymysql.err
from exceptions.attendee_exceptions import AttendeesAlreadyConnectedError
from dao.room_dao import fetch_rooms
import datetime

from utils.constants import MENU_SEPARATOR, ERROR_PREFIX, DATE_FORMAT
from utils.gender_enum import Gender

rooms = {'is_loaded': False, 'rooms': []}

def _display_menu() -> None:
    print('MENU')
    print('====')
    print('1 - View Speakers & Sessions')
    print('2 - View Attendees by Company')
    print('3 - Add New Attendee')
    print('4 - View Connected Attendees')
    print('5 - Add Attendee Connection')
    print('6 - View Rooms')
    print('7 - Update Attendee Details')
    print('x - Exit application')

def _show_sessions_for_speaker_letters() -> None:
    speaker_name = input('Enter speaker name: ')
    rows = fetch_sessions_by_speaker_name(speaker_name)

    if not rows:
        print('No speakers found of that name.\n')
        return

    print(f'\nSession Details For : {speaker_name}')
    for row in rows:
        print(f"{row['speakerName']} | {row['sessionTitle']} | {row['roomName']}")
    print()

def _show_attendees_by_company_id() -> None:
    while True:
        try:
            company_id = int(input('Enter company ID : '))
            if company_id <= 0:
                raise ValueError
        except ValueError:
            continue
        company = fetch_company_by_id(company_id)
        if not company:
            print(f'Company with ID {company_id} doesn\'t exist\n')
            break
        print(f'{company["companyName"]} Attendees')
        attendees = fetch_attendees_by_company_id(company_id)
        if not attendees:
            print(f'No attendees found for {company["companyName"]}\n')
            break
        for attendee in attendees:
            print(f"{attendee['attendeeName']} | {attendee['attendeeDOB']} | {attendee['sessionTitle']} | {attendee['speakerName']} | {attendee['roomName']}")
        print()
        break
        
def _show_rooms(rooms: dict) -> None:
    if not rooms['is_loaded']:
        rooms['rooms'] = fetch_rooms()
        rooms['is_loaded'] = True
    print('Room ID | Room Name | Capacity')
    for room in rooms['rooms']:
        print(f"{room['roomID']} | {room['roomName']} | {room['capacity']}")
    print()

def _add_attendee() -> None:
    print('Add New Attendee')
    print(MENU_SEPARATOR)
    attendee_id = input('Attendee ID : ')
    attendee_name = input('Name : ')
    attendee_dob = input('DOB (YYYY-MM-DD) : ')
    try:
        datetime.datetime.strptime(attendee_dob, DATE_FORMAT)
    except ValueError:
        print(f'{ERROR_PREFIX} DOB must be in YYYY-MM-DD format.')
        return
    attendee_gender = input('Gender : ')
    try:
        gender_enum = Gender(attendee_gender)
    except ValueError:
        print(f'{ERROR_PREFIX} Gender must be Male/Female.')
        return
    company_id = input('Company ID : ')
    try:
        company_id_int = int(company_id)
    except ValueError:
        print(f'{ERROR_PREFIX} Company ID: {company_id} does not exist.\n')
        return
    company = fetch_company_by_id(company_id_int)
    if not company:
        print(f'{ERROR_PREFIX} Company ID: {company_id_int} does not exist.\n')
        return
    try:
        add_attendee(attendee_id, attendee_name, attendee_dob, gender_enum.value, company_id_int)
        print('\nAttendee successfully added.\n')
    except pymysql.err.IntegrityError :
        print(f'{ERROR_PREFIX} Attendee ID: {attendee_id} already exists.\n')


def _fetch_connected_attendees() -> None:
    attendee_id_text = input('Enter attendee ID : ')
    try:
        attendee_id = int(attendee_id_text)
    except ValueError:
        print(f'{ERROR_PREFIX} Invalid attendee ID\n')
        return
    
    attendee = fetch_attendee_name_by_id(attendee_id)
    exists_in_neo4j = attendee_exists_in_graph(attendee_id)
    if not attendee and not exists_in_neo4j:
        print(f'{ERROR_PREFIX} Attendee does not exist\n')
        return

    rows = fetch_connected_attendees(attendee_id)
    if not rows:
        print(f'Attendee Name: {attendee["attendeeName"]}')
        print(f'{MENU_SEPARATOR}')
        print(f'No connections\n')
        return

    connected_attendee_ids = [row['attendeeID'] for row in rows]
    attendee_names = fetch_attendee_names_by_ids(connected_attendee_ids)

    print('These attendees are connected:')
    for row in rows:
        connected_attendee_id = row['attendeeID']
        attendee_name = attendee_names.get(connected_attendee_id, 'Unknown attendee in MySQL')
        print(f'{connected_attendee_id} | {attendee_name}')
    print()

def _add_attendee_connection() -> None:
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
        if fetch_attendee_name_by_id(attendee_1_int) is None or fetch_attendee_name_by_id(attendee_2_int) is None:
            print(f'{ERROR_PREFIX} One or both attendee IDs do not exist\n')
            continue
        if not attendee_exists_in_graph(attendee_1_int):
            add_attendee_in_graph(attendee_1_int)
        if not attendee_exists_in_graph(attendee_2_int):
            add_attendee_in_graph(attendee_2_int)
        try:
            add_attendee_relationship(attendee_1_int, attendee_2_int)
            print(f'Attendee {attendee_1_int} is now connected to Attendee {attendee_2_int}\n')
        except AttendeesAlreadyConnectedError:
            print(f'{ERROR_PREFIX} These attendees are already connected\n')
            continue
        break

def _run_menu() -> None:
    print('Conference Management')
    print(f'{MENU_SEPARATOR}\n')
    while True:
        _display_menu()
        choice = input('Choice: ').strip().lower()
        print()
        if choice == 'x':
            break
        if choice == '1':
            try:
                _show_sessions_for_speaker_letters()
            except Exception as exc:
                print(f'{ERROR_PREFIX} Could not load sessions: {exc}\n')
            continue
        if choice == '2':
            try:
                _show_attendees_by_company_id()
            except Exception as exc:
                print(f'{ERROR_PREFIX} Could not load attendees: {exc}\n')
            continue
        if choice == '3':
            try:
                _add_attendee()
            except Exception as exc:
                print(f'{ERROR_PREFIX} {exc}\n')
            continue
        if choice == '4':
            try:
                _fetch_connected_attendees()
            except Exception as exc:
                print(f'{ERROR_PREFIX} Could not load attendee connections: {exc}\n')
            continue
        if choice == '5':
            try:
                _add_attendee_connection()
            except Exception as exc:
                print(f'{ERROR_PREFIX} Could not connect attendees: {exc}\n')
            continue
        if choice == '6':
            try:
                _show_rooms(rooms)
            except Exception as exc:
                print(f'{ERROR_PREFIX} Could not load rooms: {exc}\n')
            continue
        if choice == '7':
            try:
                update_attendee()
            except Exception as exc:
                print(f'{ERROR_PREFIX} Could not update attendee: {exc}\n')
            continue
                
if __name__ == '__main__':
    _run_menu()
