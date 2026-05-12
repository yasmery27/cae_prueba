from pathlib import Path

APP_TITLE = "QueHacerSD"
APP_SUBTITLE = "Descubre y organiza planes en Santo Domingo"

DATABASE_PATH = Path("/tmp/quehacersd.db")

VALID_BUDGETS = ["Todos", "RD$500", "RD$800", "RD$1500"]
VALID_ZONES = ["Todas", "Zona Colonial", "Piantini", "Villa Mella"]
VALID_SCHEDULES = ["Todos", "Diurno", "Nocturno"]

SUCCESS_MESSAGE = "Plan guardado correctamente."
ERROR_MESSAGE = "Ocurrió un error inesperado."
