import os
from dotenv import load_dotenv

load_dotenv()

# Configuración esencial
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SHEET_ID = os.getenv("SHEET_ID")

# Configuración de Google Sheets (usando nombres consistentes)
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS", "creds.json")  # Nombre unificado

# Validación
required_vars = {
    "TELEGRAM_TOKEN": TELEGRAM_TOKEN,
    "OPENAI_API_KEY": OPENAI_API_KEY,
    "SHEET_ID": SHEET_ID
}

missing_vars = [name for name, value in required_vars.items() if not value]
if missing_vars:
    raise ValueError(f"Faltan variables en .env: {', '.join(missing_vars)}")