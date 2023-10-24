from datetime import datetime

from aiogoogle import Aiogoogle

from app.core import constants as const
from app.core.config import settings


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(const.DATE_FORMAT)
    service = await wrapper_service.discover(
        'sheets', settings.google_sheets_api_version)
    spreadsheet_body = {
        'properties': {
            'title': const.SPREADSHEET_TITLE.format(now_date_time),
            'locale': const.LOCALE
        },
        'sheets': [
            {'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': const.SHEET_TITLE,
                'gridProperties': {'rowCount': const.ROW_COUNT,
                                   'columnCount': const.COLUMN_COUNT}
            }
            }
        ]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']  # noqa
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_service.discover(
        'drive', settings.google_drive_api_version)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charity_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(const.DATE_FORMAT)
    service = await wrapper_service.discover(
        'sheets', settings.google_sheets_api_version)
    table_values = [
        [const.REPORT_DATE, now_date_time],
        [const.REPORT_NAME],
        [const.REPORT_NAME_HEADER, const.TIME_CHARITY_HEADER, const.DESCRIPTION_HEADER]
    ]
    for project in charity_projects:
        table_values.append([
            project.name,
            project.close_date - project.create_date,
            project.description,
        ])

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=const.RANGE,
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
