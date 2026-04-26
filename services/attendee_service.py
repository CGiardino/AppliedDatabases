import pymysql

from dao.attendee_connection_dao import add_attendee_in_graph, add_attendee_relationship_in_graph, attendee_exists_in_graph, \
    fetch_connected_attendees_in_graph
from dao.attendee_dao import fetch_attendee_name_by_id_in_db, update_attendee_in_db, fetch_attendee_names_by_ids_in_db, \
    add_attendee_in_db, fetch_attendees_by_company_id_in_db
from dao.company_dao import fetch_company_by_id_in_db
import datetime

from exceptions.attendee_exceptions import AttendeesAlreadyConnectedError
from utils.constants import MENU_SEPARATOR, ERROR_PREFIX, DATE_FORMAT
from utils.gender_enum import Gender


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
    company = fetch_company_by_id_in_db(company_id_int)
    if not company:
        print(f'{ERROR_PREFIX} Company ID: {company_id_int} does not exist.\n')
        return
    try:
        add_attendee_in_db(attendee_id, attendee_name, attendee_dob, gender_enum.value, company_id_int)
        print('\nAttendee successfully added.\n')
    except pymysql.err.IntegrityError :
        print(f'{ERROR_PREFIX} Attendee ID: {attendee_id} already exists.\n')

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
            print(f"{attendee['attendeeName']} | {attendee['attendeeDOB']} | {attendee['sessionTitle']} | {attendee['speakerName']} | {attendee['roomName']}")
        print()
        break