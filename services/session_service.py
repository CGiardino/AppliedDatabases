from dao.speaker_session_dao import fetch_sessions_by_speaker_name_in_db
from utils.constants import MENU_SEPARATOR


def show_sessions_for_speaker_letters() -> None:
    speaker_name = input('Enter speaker name: ')
    rows = fetch_sessions_by_speaker_name_in_db(speaker_name)

    print(f'Session Details For : {speaker_name}')
    print(f"{MENU_SEPARATOR}")
    if not rows:
        print('No speakers found of that name.\n')
        return

    for row in rows:
        print(f"{row['speakerName']} | {row['sessionTitle']} | {row['roomName']}")
    print()
