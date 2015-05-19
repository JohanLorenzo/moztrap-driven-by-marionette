#!/usr/bin/env python2

from marionette import Marionette
from create_test_case_page import CreateTestCasePage
from yaml_importer import get_test_cases


def _print_counter_and_message(number, total, message):
    total_length = len(str(abs(total)))
    formatted_string = '[{0: >%s}/{1}] {2}' % total_length
    print formatted_string.format(number, total, message)


test_cases = get_test_cases('./test_cases3.yml')

client = Marionette(host='localhost', port=2828)
client.start_session()

page = CreateTestCasePage(client)

i = 0
number_of_test_cases = len(test_cases)
for test_case in test_cases:
    i += 1
    _print_counter_and_message(i, number_of_test_cases, test_case.name)
    page.create_test_case(test_case.product, test_case.suite, test_case.version, test_case.priority, test_case.name,
                          test_case.description, test_case.status, test_case.tags, test_case.steps)
