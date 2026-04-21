from dao.sessionDAO import fetch_sessions_by_speaker_name
from dao.companyDAO import fetch_company_by_id
from dao.attendeeDAO import fetch_attendees_by_company_id, add_attendee
import pymysql.err

ERROR_PREFIX = '*** ERROR ***'
MENU_SEPARATOR = '---------------------'

def _display_menu() -> None:
    print('MENU')
    print('====')
    print('1 - View Speakers & Sessions')
    print('2 - View Attendees by Company')
    print('3 - Add New Attendee')
    print('4 - View Connected Attendees')
    print('5 - Add Attendee Connection')
    print('6 - View Rooms')
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

def _add_attendee() -> None:
    print('Add New Attendee')
    print(MENU_SEPARATOR)
    attendee_id = input('Attendee ID : ')
    attendee_name = input('Name : ')
    attendee_dob = input('DOB : ')
    attendee_gender = input('Gender : ')
    if attendee_gender != 'Male' and attendee_gender != 'Female':
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
        add_attendee(attendee_id, attendee_name, attendee_dob, attendee_gender, company_id_int)
        print('\nAttendee successfully added.\n')
    except pymysql.err.IntegrityError :
        print(f'{ERROR_PREFIX} Attendee ID: {attendee_id} already exists.\n')
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
                print(f'Could not load sessions: {exc}\n')
            continue
        if choice == '2':
            try:
                _show_attendees_by_company_id()
            except Exception as exc:
                print(f'Could not load attendees: {exc}\n')
            continue
        if choice == '3':
            try:
                _add_attendee()
            except Exception as exc:
                print(f'{ERROR_PREFIX} {exc}\n')
            continue

        print(f'Option "{choice}" selected. Not implemented yet.\n')

if __name__ == '__main__':
    _run_menu()
