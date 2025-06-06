import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import GOOGLE_CREDENTIALS, SHEET_ID
import logging

# Configuración básica de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def connect_to_sheet():
    """Conecta a Google Sheets y devuelve la hoja"""
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            GOOGLE_CREDENTIALS, scope)
        client = gspread.authorize(creds)
        return client.open_by_key(SHEET_ID)
    except Exception as e:
        logging.error(f"Error al conectar con Google Sheets: {e}")
        return None

def get_products_list():
    """Obtiene la lista de productos desde la hoja 'productos'"""
    try:
        sheet = connect_to_sheet()
        if not sheet:
            return []
            
        worksheet = sheet.worksheet("productos")
        return worksheet.get_all_values()[1:]  # Excluye el encabezado
    except Exception as e:
        logging.error(f"Error obteniendo productos: {e}")
        return []

def save_order(user_id, username, products, total):
    """Guarda el pedido en la hoja 'PedidosConfirmados'"""
    try:
        sheet = connect_to_sheet()
        if not sheet:
            return False
            
        worksheet = sheet.worksheet("PedidosConfirmados")
        worksheet.append_row([
            username,
            str(user_id),
            products,
            f"${float(total):.2f}",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])
        return True
    except Exception as e:
        logging.error(f"Error guardando pedido: {e}")
        return False