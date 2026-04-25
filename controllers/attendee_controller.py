from dao.attendee_dao import fetch_attendee_name_by_id, update_attendee_in_db
from dao.company_dao import fetch_company_by_id
import datetime

from utils.constants import MENU_SEPARATOR, ERROR_PREFIX
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
    attendee = fetch_attendee_name_by_id(attendee_id_int)
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
    company = fetch_company_by_id(company_id_int)
    if not company:
        print(f'{ERROR_PREFIX} Company ID: {company_id_int} does not exist.\n')
        return
    try:
        update_attendee_in_db(attendee_id_int, attendee_name, attendee_dob, gender_enum.value, company_id_int)
        print('Attendee details updated successfully.\n')
    except Exception as exc:
        print(f'{ERROR_PREFIX} Could not update attendee: {exc}')

