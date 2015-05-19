class TestCase(object):
    def __init__(self, product, suite, version, priority, name, description, status, tags, steps):
        self.product = product
        self.suite = suite
        self.version = version
        self.priority = priority
        self.name = name
        self.description = '' if description is None else description
        self.status = status
        self.tags = tags
        for step in steps:
            if 'instruction' not in step:
                raise KeyError
        self.steps = steps

    @classmethod
    def from_dict(cls, dictionary):
        return TestCase(dictionary['product'], dictionary['suite'], dictionary['version'], dictionary['priority'],
                        dictionary['name'], dictionary['description'], dictionary['status'], dictionary['tags'],
                        dictionary['steps'])
