from services.attendee_service import update_attendee, add_attendee_connection, add_attendee, \
    show_attendees_by_company_id, fetch_connected_attendees, delete_attendee

from services.room_service import show_rooms
from services.session_service import show_sessions_for_speaker_letters
from utils.constants import MENU_SEPARATOR, ERROR_PREFIX

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
    print('8 - Delete Attendee')
    print('x - Exit application')

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
                show_sessions_for_speaker_letters()
            except Exception as exc:
                print(f'{ERROR_PREFIX} Could not load sessions: {exc}\n')
            continue
        if choice == '2':
            try:
                show_attendees_by_company_id()
            except Exception as exc:
                print(f'{ERROR_PREFIX} Could not load attendees: {exc}\n')
            continue
        if choice == '3':
            try:
                add_attendee()
            except Exception as exc:
                print(f'{ERROR_PREFIX} {exc}\n')
            continue
        if choice == '4':
            try:
                fetch_connected_attendees()
            except Exception as exc:
                print(f'{ERROR_PREFIX} Could not load attendee connections: {exc}\n')
            continue
        if choice == '5':
            try:
                add_attendee_connection()
            except Exception as exc:
                print(f'{ERROR_PREFIX} Could not connect attendees: {exc}\n')
            continue
        if choice == '6':
            try:
                show_rooms(rooms)
            except Exception as exc:
                print(f'{ERROR_PREFIX} Could not load rooms: {exc}\n')
            continue
        if choice == '7':
            try:
                update_attendee()
            except Exception as exc:
                print(f'{ERROR_PREFIX} Could not update attendee: {exc}\n')
            continue
        if choice == '8':
            try:
                delete_attendee()
            except Exception as exc:
                print(f'{ERROR_PREFIX} Could not delete attendee: {exc}\n')
            continue
                
if __name__ == '__main__':
    _run_menu()
