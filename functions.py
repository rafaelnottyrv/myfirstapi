from google.oauth2 import service_account
from googleapiclient.discovery import build

def generate_ini_google_doc(sheet_id1, sheet_id2):
    """Actualiza el contenido de Google Sheets"""
    # Credenciales de autenticación y autorización
    creds = service_account.Credentials.from_service_account_file('credentials.json')

    # Inicializar la API de Sheets
    service = build('sheets', 'v4', credentials=creds)

    # Leer los datos de la hoja 'Hoja1'
    range_name = 'Hoja1!A1:J'
    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id1,
        range=range_name
    ).execute()
    values = result.get('values', [])

    # Escribir los datos en la hoja 'Hoja2'
    if values:
        range_name_dest = 'Hoja2!A1'
        request_body = {
            'values': values
        }
        result_dest = service.spreadsheets().values().update(
            spreadsheetId=sheet_id1,
            range=range_name_dest,
            valueInputOption='RAW',
            body=request_body
        ).execute()
        return result_dest
    else:
        return "No se encontraron datos en la hoja 'Hoja1'"

