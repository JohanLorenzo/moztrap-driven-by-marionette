import yaml
from test_case import TestCase


def get_test_cases(file_url):
    with open(file_url) as f:
        test_cases_dicts = yaml.safe_load_all(f)

        test_cases = []
        for test_case_dict in test_cases_dicts.next():
            test_case = TestCase.from_dict(test_case_dict)
            test_cases.append(test_case)

        return test_cases
