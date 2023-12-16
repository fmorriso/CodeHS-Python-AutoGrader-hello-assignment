import re


class AutoGrader:

    def __init__(self, filename: str):
        self.filename = filename
        self.student_code = ''
        self.code_lower = ''
        self.code_index = -1
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

    def expect_def(self) -> bool:
        looking_for = 'def '
        idx_def = self.code_lower.find(looking_for)
        expectation = 'contains def'
        if idx_def == -1:
            self.results.append(f'FAIL: {expectation}')
            return False

        self.results.append(f'SUCCESS: {expectation}')
        self.code_index = len(looking_for)
        return True

    def expect_function_name(self) -> bool:
        expectation = 'contains function named hello (all lowercase)'
        looking_for = 'hello'
        # verify the function is named hello (case sensitive)
        idx_fn_name = self.code_lower[self.code_index:].find(looking_for)
        if idx_fn_name == -1:
            self.results.append(f'FAIL: {expectation}')
            return False
        self.results.append(f'SUCCESS: {expectation}')
        self.code_index += idx_fn_name + len(looking_for)
        return True

    def expect_function_parameter(self) -> bool:
        expectation = 'hello function expects a name parameter'
        looking_for = '('
        # find the required left paren after the function name
        idx_left_paren = self.code_lower[self.code_index:].find(looking_for)
        if idx_left_paren == -1:
            self.results.append(f'FAIL: {expectation}')
            return False
        self.code_index += idx_left_paren + len(looking_for)

        # find the name parameter immediately following the left paren
        looking_for = 'name'
        idx_param = self.code_lower[self.code_index:].find(looking_for)
        if idx_param == -1:
            self.results.append(f'FAIL: {expectation}')
            return False
        self.results.append(f'SUCCESS: {expectation}')
        self.code_index += idx_param + len(looking_for)
        return True

    def expect_return_statement(self) -> bool:
        expectation = 'hello function contains a return statement'
        looking_for = 'return '
        idx_return = self.code_lower[self.code_index:].find(looking_for)
        if idx_return == -1:
            self.results.append(f'FAIL: {expectation}')
            return False
        self.code_index += idx_return + len(looking_for)
        self.results.append(f'SUCCESS: {expectation}')
        return True

    def expect_return_expression(self) -> bool:
        expectation = 'hello function returns hello with comma in quotes'
        looking_for = 'hello, '
        # verify that return is followed by the literal string hello (case insensitive)
        idx_hello = self.code_lower[self.code_index:].find(looking_for)
        if idx_hello == -1:
            self.results.append(f'FAIL: {expectation}')
            return False
        self.results.append(f'SUCCESS: {expectation}')
        self.code_index += idx_hello + len(looking_for)

        # look for the plus concatenation operator
        looking_for = ' + '
        expectation = 'hello function return statement contains + operator'
        idx_plus_sign = self.code_lower[self.code_index:].find('+')
        if idx_plus_sign == -1:
            self.results.append(f'FAIL: {expectation}')
            return False
        self.results.append(f'SUCCESS: {expectation}')
        self.code_index += idx_plus_sign + len(looking_for)

        # look for name parameter without any quotes around it
        looking_for = 'name'
        expectation = 'hello function return statement includes name parameter'
        idx_name_param = self.code_lower[self.code_index:].find(looking_for)
        if idx_name_param == -1:
            self.results.append(f'FAIL: {expectation}')
            return False
        self.results.append(f'SUCCESS: {expectation}')
        # do NOT advance code_index just yet

        # verify name param is not surrounded by single or double quotes
        expectation = 'name parameter in return statement is NOT surrounded by quotes (single or double)'
        possible_quote_char = self.code_lower[self.code_index - 1]
        if possible_quote_char == '"' or possible_quote_char == "'":
            self.results.append(f'FAIL: {expectation}')
            return False
        self.results.append(f'SUCCESS: {expectation}')
        # note: need to advance beyond " + name"
        self.code_index += idx_plus_sign + len(looking_for)
        return True

    def grade_student_code(self):
        # expectations concerning the def statement
        if self.expect_def():
            if self.expect_function_name():
                self.expect_function_parameter()

        # expectations about the return statement within the function
        if self.expect_return_statement():
            if self.expect_return_expression():
                pass


    def print_results(self):
        for result in self.results:
            print(result)
