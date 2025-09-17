import csv
from typing import Dict, List


def read_csv_rows(filename: str) -> List[dict]:
    """Прочитать все строки CSV и вернуть список словарей."""
    with open(filename, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def save_as_txt(path: str, data: Dict[str, List[float]]) -> None:
    # читаемый текст: имя -> [оценки], среднее
    with open(path, "w", encoding="utf-8") as f:
        for name, grades in data.items():
            
            f.write(f"{name} -> {grades}\n")