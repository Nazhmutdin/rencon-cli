import pathlib
from pathlib import Path
import os

from dotenv import load_dotenv


load_dotenv()


DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")
HOST = os.getenv("HOST")
USER = os.getenv("USER")
PORT = os.getenv("PORT")

BASE_DIR = Path.cwd()
STATIC_DIR = Path(f"{BASE_DIR}/static")

GROUPS_FOLDER = pathlib.Path(f"{STATIC_DIR}/groups")

WELDERS_DATA_JSON_PATH = pathlib.Path(f"{STATIC_DIR}/welders_certifications.json")
WELDER_REGISTRY_PATH = pathlib.Path(f"{STATIC_DIR}/welder_registry.xlsx")
NDT_REGISTRY_PATH = pathlib.Path(f"{STATIC_DIR}/ndt_registry.xlsx")
NDT_TABLES_FOLDER_PATH = pathlib.Path(f"{STATIC_DIR}/ndt_tables")

ENGINEERS_DATA_JSON_PATH = pathlib.Path(f"{STATIC_DIR}/engineers_certifications.json")
ENGINEER_REGISTRY_PATH = pathlib.Path(f"{STATIC_DIR}/engineer_registry.xlsx")

PDF_PARSER_SRC = pathlib.Path(f"{STATIC_DIR}/src")
PDF_PARSER_STORE = pathlib.Path(f"{STATIC_DIR}/processed")

CHROME_DRIVER_PATH = pathlib.Path(f"{STATIC_DIR}/chromedriver/chromedriver.exe")

PATH_TO_TESSERACT = pathlib.Path(f"{STATIC_DIR}/tesseract/tesseract.exe")
TESSERACT_CONFIG = f"--tessdata-dir '{STATIC_DIR}/tesseractOLD/tessdata' -l rus+eng --oem 2 --psm 12"

PATH_TO_POPPLER = pathlib.Path(f"{STATIC_DIR}/poppler/Library/bin")
PATH_TO_MASKS = pathlib.Path(f"{STATIC_DIR}/masks")
PATH_TO_PDF_PARSER_SETTINGS = pathlib.Path(f"{STATIC_DIR}/settings.json")

SEARCH_VALUES_FILE = pathlib.Path(f"{STATIC_DIR}/search_values.txt")
SKIPED_VALUES_FILE = pathlib.Path(f"{STATIC_DIR}/skiped_values.txt")

ACST_DATA_JSON_PATH = pathlib.Path(f"{STATIC_DIR}/acsts.json")
ACST_REGISTRY_PATH = pathlib.Path(f"{STATIC_DIR}/acst_registry.xlsx")