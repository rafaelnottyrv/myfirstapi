from google.oauth2 import service_account
from googleapiclient.discovery import build

def generate_ini_google_doc(sheet_id, sheet_name):
    """Actualiza el contenido de google sheets"""
    # Credenciales de autenticación y autorización
    creds = service_account.Credentials.from_service_account_file('credentials.json')
    
    # Inicializar la API de Sheets
    service = build('sheets', 'v4', credentials=creds)

    # Definir la hoja y el rango donde se escribirán los datos
    sheet = service.spreadsheets()
    range_name = sheet_name + '!A1'
    values = [
        ["KPI5", 'Iniciativa', 'Nombre App', 'Tiempo', 'Tiempo Custom', 'Request', 'Promedio', 'Promedio custom', 'Nota', 'Nota Custom']
    ]

    # Escribir los datos en la hoja de cálculo
    request_body = {
        'values': values
    }
    result = sheet.values().update(
        spreadsheetId=sheet_id,
        range=range_name,
        valueInputOption='RAW',
        body=request_body
    ).execute()
    return result

def prueba():    
    """Retorna Hola"""
    print("Hola_Mundo")