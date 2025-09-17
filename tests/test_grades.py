from unittest.mock import patch

import  pytest

from grades import safe_float,collect_grades,_student_performance

@pytest.mark.parametrize("s,expected", [
    ("12", 12.0),
    ("23", 23.0),
    ("3.14", 3.14),
])
def test_true_safe_float(s,expected):
    assert safe_float(s) == expected

@pytest.mark.parametrize("s", [
    "assda",
    "",
    None,
    "1,23",   # запятая не конвертируется в float
])
def test_false_safe_float(s):
    assert safe_float(s) is None





def make_row(student_name: str, grade: str, subject: str = "Math") -> dict:
    return {"student_name": student_name, "grade": grade, "subject": subject}


def fake_read(file1, file2, filename: str):
    if filename == "f1.csv":
        return file1
    elif filename == "f2.csv":
        return file2
    return []



def patch_safe_float():
    return patch("grades.safe_float", lambda s: float(s))


def test_collect_grades():
    file1 = [
        make_row("Alice", "5", "Math"),
        make_row("Bob", "4", "Physics"),
        make_row("Alice", "4.5", "Physics"),
    ]
    file2 = [
        make_row("Charlie", "3", "History"),
        make_row("Bob", "4.0", "Math"),
    ]

    with patch("grades.read_csv_rows", lambda filename: fake_read(file1, file2, filename)), patch_safe_float():
        result = collect_grades(["f1.csv", "f2.csv"])

    assert result["Alice"] == [("Math", 5.0), ("Physics", 4.5)]
    assert result["Bob"] == [("Physics", 4.0), ("Math", 4.0)]
    assert result["Charlie"] == [("History", 3.0)]


def test_collect_grades_skips_empty():
    file1 = [
        make_row("", "5", "Math"),  # пустое имя -> пропустить
        make_row("Dima", "", "Math"),  # пустая оценка -> пропустить
        make_row("Gina", "4", "Chemistry"),  # валидная
    ]
    file2 = [
        {"student_name": "Egor"},  # нет поля grade -> пропустить
        make_row("Fiona", "not-a-number", "Bio"),  # некорректная оценка -> пропустить
    ]

    with patch("grades.read_csv_rows", lambda filename: fake_read(file1, file2, filename)), patch_safe_float():
        result = collect_grades(["f1.csv", "f2.csv"])

    assert "Dima" not in result
    assert "Egor" not in result
    assert "Fiona" not in result
    assert result["Gina"] == [("Chemistry", 4.0)]

def test_student_performance():
    all_grades = {
        "Alice": [("Math", 5.0), ("Physics", 4.5)],
        "Bob": [("Math", 4.0), ("Physics", 3.5)],
        "Diana": [("Chemistry", 4.0)],
    }
    expected_output = [
        ["Alice", 4.75],
        ["Diana", 4.0],
        ['Bob', 3.75],

    ]

    assert _student_performance(all_grades) == expected_output