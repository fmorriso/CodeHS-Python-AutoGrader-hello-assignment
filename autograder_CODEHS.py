class Suite(PythonTestSuite):
    # Any values that should be passed to any call to `input`
    inputs = ["Mark"]

    def expect_def(self) -> bool:
        looking_for = 'def '
        retval = False

        idx_def = self.code_lower.find(looking_for)
        if idx_def >= 0:
            self.code_index = len(looking_for)
            retval = True
        expect(idx_def).to_be_greater_than_or_equal_to(0) \
            .with_options(test_name="contains def")
        return retval

    def expect_function_name(self) -> bool:
        looking_for = 'hello'
        retval = False
        # verify the function is named hello (case sensitive)
        idx_fn_name = self.code_lower[self.code_index:].find(looking_for)
        if idx_fn_name >= 0:
            self.code_index += idx_fn_name + len(looking_for)
            retval = True

        expect(idx_fn_name).to_be_greater_than(0) \
            .with_options(test_name='contains function named hello (all lower case)')

        return retval

    def expect_function_parameter(self) -> bool:
        looking_for = '('
        retval = False
        # find the required left paren after the function name
        idx_left_paren = self.code_lower[self.code_index:].find(looking_for)
        if idx_left_paren >= 0:
            self.code_index += idx_left_paren + len(looking_for)

        expect(idx_left_paren).to_be_greater_than_or_equal_to(0) \
            .with_options(test_name='hello function expects name parameter in parens')

        # skip rest of function if we never found the left paren
        if idx_left_paren == -1:
            return retval

        # find the name parameter immediately following the left paren
        looking_for = 'name'
        idx_param = self.code_lower[self.code_index:].find(looking_for)
        if idx_param >= 0:
            self.code_index += idx_param + len(looking_for)
            retval = True

        expect(idx_param).to_be_greater_than_or_equal_to(0) \
            .with_options(test_name='hello function expects a name parameter')

        return retval

    # Write any tests that should run before the code is evaluated
    def before_run(self, student_code, solution_code):

        self.code_index = 0
        code_lower = strip_comments(student_code).lower()
        # make lower case code available to instance functions
        self.code_lower = code_lower

        # start checking first line of code where def is supposed to be located
        if self.expect_def():
            if self.expect_function_name():
                if self.expect_function_parameter():
                    pass

    # Write any tests that should run after the code is evaluated
    def after_run(self, student_code, solution_code, student_output, solution_output):

        student_lower = student_output.lower()
        solution_lower = solution_output.lower()

        idx_hello = student_lower.find('hello,')
        expect(idx_hello).to_be_greater_than_or_equal_to(0) \
            .with_options(test_name='output contains hello, or Hello, ')


Suite()
