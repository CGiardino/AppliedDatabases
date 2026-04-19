from dao.sessionDAO import fetch_sessions_by_speaker_name

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

def _show_sessions_for_speaker_letters() -> None:
    speaker_name = input('Enter speaker name: ')
    rows = fetch_sessions_by_speaker_name(speaker_name)

    if not rows:
        print('No sessions found for that search.\n')
        return

    print(f'\nSession Details For : {speaker_name}')
    for row in rows:
        print(f"{row['speakerName']} | {row['sessionTitle']} | {row['roomName']}")
    print()

def _run_menu() -> None:
    while True:
        _display_menu()
        choice = input('Choice: ').strip().lower()

        if choice == 'x':
            break

        if choice == '1':
            try:
                _show_sessions_for_speaker_letters()
            except Exception as exc:
                print(f'Could not load sessions: {exc}\n')
            continue

        print(f'Option "{choice}" selected. Not implemented yet.\n')

if __name__ == '__main__':
    _run_menu()
