from marionette_driver import By, Actions, Wait
from time import sleep


class CreateTestCasePage(object):

    _URL = 'https://moztrap.mozilla.org/manage/case/add/'

    _PRODUCT_LOCATOR = (By.ID, 'id_product')
    _SUITE_LOCATOR = (By.ID, 'id_suite')
    _VERSION_LOCATOR = (By.ID, 'id_productversion')
    _PRIORITY_LOCATOR = (By.ID, 'id_priority')
    _NAME_LOCATOR = (By.ID, 'id_name')
    _DESCRIPTION_LOCATOR = (By.ID, 'id_description')
    _STATUS_LOCATOR = (By.ID, 'id_status')
    _TAGS_LOCATOR = (By.ID, 'id_add_tags')
    _SUGGESTIONS_LOCATOR = (By.CSS_SELECTOR, '.suggest')
    _SAVE_BUTTON_LOCATOR = (By.CSS_SELECTOR, 'button[name="save"]')

    _DEFAULT_TIMEOUT = 10

    def __init__(self, marionette):
        self.marionnette = marionette

    @property
    def product(self):
        return self.marionnette.find_element(*self._PRODUCT_LOCATOR).text

    @product.setter
    def product(self, value):
        self._tap_and_fill_field(self._PRODUCT_LOCATOR, value)

    @property
    def suite(self):
        return self.marionnette.find_element(*self._SUITE_LOCATOR).text

    @suite.setter
    def suite(self, value):
        self._tap_and_fill_field(self._SUITE_LOCATOR, value)

    @property
    def version(self):
        return self.marionnette.find_element(*self._VERSION_LOCATOR).text

    @version.setter
    def version(self, value):
        self._tap_and_fill_field(self._VERSION_LOCATOR, value)

    @property
    def priority(self):
        return self.marionnette.find_element(*self._PRIORITY_LOCATOR).text

    @priority.setter
    def priority(self, value):
        self._tap_and_fill_field(self._PRIORITY_LOCATOR, value)

    @property
    def name(self):
        return self.marionnette.find_element(*self._NAME_LOCATOR).text

    @name.setter
    def name(self, value):
        self.marionnette.find_element(*self._NAME_LOCATOR).send_keys(value)

    @property
    def description(self):
        return self.marionnette.find_element(*self._DESCRIPTION_LOCATOR).text

    @description.setter
    def description(self, value):
        self.marionnette.find_element(*self._DESCRIPTION_LOCATOR).send_keys(value)

    @property
    def status(self):
        return self.marionnette.find_element(*self._STATUS_LOCATOR).text

    @status.setter
    def status(self, value):
        self._tap_and_fill_field(self._STATUS_LOCATOR, value)

    def add_tag(self, tag):
        line_edit = self.marionnette.find_element(*self._TAGS_LOCATOR)
        suggestions = self.marionnette.find_element(*self._SUGGESTIONS_LOCATOR)
        line_edit.send_keys(tag)
        Wait(self.marionnette, self._DEFAULT_TIMEOUT).until(lambda m: suggestions.is_displayed())
        line_edit.send_keys('\n')
        Wait(self.marionnette, self._DEFAULT_TIMEOUT).until(lambda m: not suggestions.is_displayed())

    def _instruction_locator(self, index):
        return By.ID, 'id_steps-{}-instruction'.format(index)

    def _expected_locator(self, index):
        return By.ID, 'id_steps-{}-expected'.format(index)

    def add_instruction(self, index, value):
        locator = self._instruction_locator(index)
        self._tap_and_fill_field(locator, value)
        self._wait_for_instruction_to_appear(index + 1)

    def add_expected(self, index, value):
        locator = self._expected_locator(index)
        self.marionnette.find_element(*locator).send_keys(value)

    def save_test_case(self):
        self.marionnette.find_element(*self._SAVE_BUTTON_LOCATOR).click()

    def create_test_case(self, product, suite, version, priority, name, description, status, tags, steps):
        self.marionnette.navigate(self._URL)

        self.product = product
        self.suite = suite
        self.version = version
        self.priority = priority
        self.name = name
        self.description = description
        self.status = status
        for tag in tags:
            self.add_tag(tag)

        for i in range(len(steps)):
            instruction = steps[i]['instruction']
            self.add_instruction(i, instruction)

            try:
                expected = steps[i]['expected']
                self.add_expected(i, expected)
            except KeyError:
                pass

        sleep(5)    # Help the user to check the data
        self.save_test_case()
        Wait(self.marionnette, self._DEFAULT_TIMEOUT).until(lambda m: self.marionnette.get_url() != self._URL)

    def _tap_and_fill_field(self, locator, value):
        element = self.marionnette.find_element(*locator)
        Actions(self.marionnette).tap(element).perform()
        element.send_keys(value)

    def _wait_for_instruction_to_appear(self, index):
        next_instruction_locator = self._instruction_locator(index)
        next_instruction = self.marionnette.find_element(*next_instruction_locator)
        Wait(self.marionnette, self._DEFAULT_TIMEOUT).until(lambda m: next_instruction.is_displayed())
