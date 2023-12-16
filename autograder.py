import re


class AutoGrader:

    def __init__(self, filename: str):
        self.filename = filename
        self.student_code = ''
        self.code_lower = ''
        self.results: list[str] = []

    def get_student_code_from_file(self):
        with open(self.filename, 'r') as f:
            self.student_code: str = f.read()
            self.strip_comments()
            self.code_lower = self.student_code.lower()

    def get_student_code(self) -> str:
        return self.student_code

    def strip_comments(self):
        self.student_code = re.sub(r'(?m)^ *#.*\n?', '', self.student_code)

    def expect_def(self) -> int:
        idx_def = self.code_lower.find('def ')
        if idx_def == -1:
            self.results.append('FAIL: no def statement')
        else:
            self.results.append('SUCCESS: contains def')

        return idx_def

    def grade_student_code(self):
        self.expect_def()

    def print_results(self):
        for result in self.results:
            print(result)