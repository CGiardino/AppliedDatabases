from dao.room_dao import fetch_rooms_in_db

def show_rooms(rooms: dict) -> None:
    if not rooms['is_loaded']:
        rooms['rooms'] = fetch_rooms_in_db()
        rooms['is_loaded'] = True
    print('Room ID | Room Name | Capacity')
    for room in rooms['rooms']:
        print(f"{room['roomID']} | {room['roomName']} | {room['capacity']}")
    print()