import sys

from autograder import AutoGrader


def get_python_version() -> str:
    return f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'


if __name__ == '__main__':
    print(f'Python version {get_python_version()}')
    ag = AutoGrader('student_code_exact.txt')
    ag.get_student_code_from_file()
    ag.grade_student_code()
    ag.print_results()



