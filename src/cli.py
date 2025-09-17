import argparse
from grades import collect_grades, COMMANDS,print_student
from csv_utils import save_as_txt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Welcome')
    parser.add_argument(
        '--files',
        nargs='+',           # один или более значений
        help='List of input files',
        required=True
    )
    parser.add_argument(
        '--report',
        help='Func name',
        required=True
    )
    my_namespace = parser.parse_args()
    cmd = my_namespace.report
    file_list = my_namespace.files

    if cmd not in COMMANDS:
        parser.error(f"Неизвестная команда: {cmd}")

    all_grades = collect_grades(file_list)
    save_as_txt("parsed_grades.txt", all_grades)
    grades = COMMANDS[cmd](all_grades)
    print_student(grades)