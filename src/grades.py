from collections import defaultdict
from typing import Dict, List
from tabulate import tabulate

from csv_utils import read_csv_rows


def safe_float(s: str) -> float:
    """Попробовать преобразовать в float, иначе вернуть None через исключение."""
    try:
        return float(s)
    except (ValueError,TypeError):
        return None


def collect_grades(filenames: List[str]) -> Dict[str, List[tuple]]:
    """
    Собрать все оценки для каждого студента.

    """
    grades_by_student: Dict[str, List[tuple]] = defaultdict(list)

    for fn in filenames:

        rows = read_csv_rows(fn)
        if rows is None:
            continue
        for row in rows:
            name = row.get("student_name")
            grade_text = row.get("grade")
            subject = row.get("subject")
            if not name or not grade_text:
                # пропустить пустые записи
                continue

            try:
                grade = safe_float(grade_text)
            except ValueError:
                # если оценка не число — пропустить запись
                continue

            grades_by_student[name].append((subject, grade))

    return grades_by_student

def average(nums: List[float]) -> float:
    """Среднее; если список пуст — вернуть 0.0."""
    return 0.0 if not nums else sum(nums) / len(nums)


def _student_performance(all_grades: Dict[str, List[tuple]]):
    rows = []
    for student, grades_sub in all_grades.items():
        grade_only = []
        for subject, grade in grades_sub:
            grade_only.append(grade)
        if not grade_only:
            continue  # пропустить студентов без оценок
        avg = average(grade_only)

        rows.append([student, avg])

    # Сортируем по среднему баллу
    rows.sort(key=lambda r: r[1], reverse=True)

    return rows  # Возвращаем отсортированный список


def print_student(rows):
    numbered = []
    for idx, (name, avg) in enumerate(rows, start=1):
        numbered.append([idx, name, avg])

    print(tabulate(numbered, headers=["Студент", "Средний балл"], tablefmt="grid", numalign="right", stralign="left"))


# реестр команд
COMMANDS = {
    "student-performance": _student_performance,
}