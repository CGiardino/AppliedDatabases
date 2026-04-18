def _display_menu() -> None:
    print('Conference Management')
    print('---------------------')
    print()
    print('MENU')
    print('====')
    print('1 - View Speakers & Sessions')
    print('2 - View Attendees by Company')
    print('3 - Add New Attendee')
    print('4 - View Connected Attendees')
    print('5 - Add Attendee Connection')
    print('6 - View Rooms')
    print('x - Exit application')

def _run_menu() -> None:
    while True:
        _display_menu()
        choice = input('Choice: ').strip().lower()

        if choice == 'x':
            break

        print(f'Option "{choice}" selected. Not implemented yet.\n')

if __name__ == '__main__':
    _run_menu()
