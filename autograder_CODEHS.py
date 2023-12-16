class Suite(PythonTestSuite):
    # Any values that should be passed to any call to `input`
    inputs = ["Mark"]

    def expect_def(self) -> bool:
        expectation = 'contains def'
        looking_for = 'def '
        retval = False

        idx_def = self.code_lower.find(looking_for)
        if idx_def >= 0:
            self.code_index = len(looking_for)
            retval = True
        expect(idx_def).to_be_greater_than_or_equal_to(0) \
            .with_options(test_name=expectation)
        return retval

    def expect_function_name(self) -> bool:
        expectation = 'contains function named hello (all lower case)'
        looking_for = 'hello'
        retval = False
        # verify the function is named hello (case sensitive)
        idx_fn_name = self.code_lower[self.code_index:].find(looking_for)
        if idx_fn_name >= 0:
            self.code_index += idx_fn_name + len(looking_for)
            retval = True

        expect(idx_fn_name).to_be_greater_than(0) \
            .with_options(test_name=expectation)

        return retval

    def expect_return_statement(self) -> bool:
        expectation = 'hello function contains a return statement'
        looking_for = 'return '
        retval = False
        idx_return = self.code_lower[self.code_index:].find(looking_for)
        if idx_return >= 0:
            self.code_index += idx_return + len(looking_for)
            retval = True

        expect(idx_return).to_be_greater_than_or_equal_to(0) \
            .with_options(test_name=expectation)

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
        expectation = 'hello function expects a name parameter'
        looking_for = 'name'
        idx_param = self.code_lower[self.code_index:].find(looking_for)
        if idx_param >= 0:
            self.code_index += idx_param + len(looking_for)
            retval = True

        expect(idx_param).to_be_greater_than_or_equal_to(0) \
            .with_options(test_name=expectation)

        return retval

    def expect_return_expression(self) -> bool:
        expectation = 'hello function returns hello with comma in quotes'
        looking_for = 'hello, '
        retval = False
        # verify that return is followed by the literal string hello (case insensitive)
        idx_hello = self.code_lower[self.code_index:].find(looking_for)
        if idx_hello >= 0:
            self.code_index += idx_hello + len(looking_for)

        expect(idx_hello).to_be_greater_than_or_equal_to(0) \
            .with_options(test_name=expectation)

        # skip rest of function if the hello, is completely missing in action
        if idx_hello == -1:
            return retval

        # look for the plus concatenation operator
        looking_for = ' + '
        expectation = 'hello function return statement contains + operator'
        idx_plus_sign = self.code_lower[self.code_index:].find('+')
        if idx_plus_sign >= 0:
            self.code_index += idx_plus_sign + len(looking_for)

        expect(idx_plus_sign).to_be_greater_than_or_equal_to(0) \
            .with_options(test_name=expectation)
        # skip rest of function if plus (+) is missing
        if idx_plus_sign == -1:
            return retval

        # look for name parameter without any quotes around it
        looking_for = 'name'
        expectation = 'hello function return statement includes name parameter'
        idx_name_param = self.code_lower[self.code_index:].find(looking_for)
        if idx_name_param >= 0:
            # do NOT advance code_index just yet
            pass

        expect(idx_name_param).to_be_greater_than_or_equal_to(0) \
            .with_options(test_name=expectation)

        # skip rest of function if there is no name parameter in the return statement
        if idx_name_param == -1:
            return reval

        # verify name param is not surrounded by single or double quotes
        expectation = 'name parameter in return statement is NOT surrounded by quotes (single or double)'
        message_failure = 'do NOT surround the name parameter with quotes'
        possible_quote_char = self.code_lower[self.code_index - 1]
        has_quotes = possible_quote_char == '"' or possible_quote_char == "'"
        expect(has_quotes).to_be_falsey().with_options(test_name=expectation, message_fail=message_failure)

        # note: need to advance beyond " + name"
        self.code_index += idx_plus_sign + len(looking_for)
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
                self.expect_function_parameter()

        # now look at the function return statement
        if self.expect_return_statement():
            self.expect_return_expression()

    # Write any tests that should run after the code is evaluated
    def after_run(self, student_code, solution_code, student_output, solution_output):

        student_lower = student_output.lower()
        solution_lower = solution_output.lower()

        idx_hello = student_lower.find('hello,')
        expect(idx_hello).to_be_greater_than_or_equal_to(0) \
            .with_options(test_name='output contains hello, or Hello, ')


Suite()
