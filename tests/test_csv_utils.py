import pytest
import os,sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from src.csv_utils import read_csv_rows

@pytest.mark.parametrize("s",["students1.csv","students2.csv"])
def test_read_csv_rows(s):
    try:
        assert read_csv_rows(s)
    except Exception as e:
        pytest.fail(f"Error reading file {s}: {str(e)}")


@pytest.mark.parametrize("s",["students13.csv","students22.csv"])
def test_not_read_csv_rows(s):
    with pytest.raises(FileNotFoundError):
        read_csv_rows(s)


def test_collect_grades():
    pass
