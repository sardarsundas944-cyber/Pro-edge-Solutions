import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
STUDENTS_FILE = DATA_DIR / "students.json"


def ensure_data_file():
    DATA_DIR.mkdir(exist_ok=True)
    if not STUDENTS_FILE.exists():
        STUDENTS_FILE.write_text("[]", encoding="utf-8")
    return STUDENTS_FILE


def load_students():
    try:
        ensure_data_file()
        with STUDENTS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            return []
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return []


def save_students(students):
    try:
        ensure_data_file()
        with STUDENTS_FILE.open("w", encoding="utf-8") as file:
            json.dump(students, file, indent=4)
            file.write("\n")
        return True
    except OSError:
        return False
