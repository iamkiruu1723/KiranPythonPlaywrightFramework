import json
import csv
from pathlib import Path

import openpyxl


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _resolve_data_file(file_path: str) -> Path:
    path = Path(file_path)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def read_json_data(file_path: str):
    """
    Reads test data from a JSON file and returns a list of tuples.
    Example JSON structure:
    [
        {"email": "test1@example.com", "password": "abc123", "validity": "valid"},
        {"email": "test2@example.com", "password": "xyz123", "validity": "invalid"}
    ]
    """
    data = []
    resolved_path = _resolve_data_file(file_path)
    with resolved_path.open("r", encoding="utf-8") as file:
        json_data = json.load(file)

    for record in json_data:
        data.append((
            record["testName"],
            record["email"],
            record["password"],
            record["expected"],
        ))
    return data


def read_csv_data(file_path: str):
    """
    Reads test data from a CSV file and returns a list of tuples.
    CSV file should contain headers: email,password,validity
    """
    data = []
    try:
        with _resolve_data_file(file_path).open(newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                #data.append((row["email"], row["password"], row["validity"]))
                data.append(tuple(row.values()))
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return data


def read_excel_data(file_path: str, sheet_name: str = None):
    """
    Reads test data from an Excel file and returns a list of tuples.
    Assumes the first row contains headers (email, password, validity).
    """
    data = []
    try:
        workbook = openpyxl.load_workbook(_resolve_data_file(file_path))
        sheet = workbook[sheet_name] if sheet_name else workbook.active
        for row in sheet.iter_rows(min_row=2, values_only=True):
            data.append(row)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
    return data
