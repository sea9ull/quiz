from oauth2client.service_account import ServiceAccountCredentials as SA
import gspread

DOCUMENT_ID = "XXXXXX"

credential_file = 'credential.json'
scopes = ['https://spreadsheets.google.com/feeds']

credentials = SA.from_json_keyfile_name(credential_file, scopes=scopes)
gs_client = gspread.authorize(credentials)
gfile = gs_client.open_by_key(DOCUMENT_ID)


def insert_record(data):
    worksheet = gfile.sheet1
    worksheet.append_row(data)


def update_record(data):
    worksheet = gfile.sheet1
    c = worksheet.find(data[0])
    if c:
        N = len(data)
        cells = worksheet.range(c.row, 1, c.row, N)

        for i in range(N):
            cells[i].value = data[i]

        worksheet.update_cells(cells)
    else:
        insert_record(data)
