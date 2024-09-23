from unittest import TestCase, TestSuite, makeSuite, TextTestRunner
from lambda_function import handler
from uuid import uuid4

class TestMapArray(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.input_list = ['a', 'b', 'c']

        self.event = {
            "requestId": str(uuid4()),
            "params": {
                "Operation": "",
                "InputArray": self.input_list
            }
        }
    
    def test_suffix(self, *_, **__):
        suffix = '_this_is_an_suffix'
        self.event['params']['Operation'] = 'ADD_SUFFIX'
        self.event['params']['Suffix'] = suffix

        transformed = handler(self.event, None)
        self.assertEqual(transformed['status'], 'success')
        response = transformed.get('fragment', [])
        
        for i in range(0, len(self.input_list)):
            self.assertEqual(f'{self.input_list[i]}{suffix}', response[i])

    def test_prefix(self, *_, **__):
        prefix = 'this_is_an_prefix_'
        self.event['params']['Operation'] = 'ADD_PREFIX'
        self.event['params']['Prefix'] = prefix

        transformed = handler(self.event, None)
        self.assertEqual(transformed['status'], 'success')
        response = transformed.get('fragment', [])
        
        for i in range(0, len(self.input_list)):
            self.assertEqual(f'{prefix}{self.input_list[i]}', response[i])
    
    def test_replace(self, *_, **__):
        old = 'b'
        new = 'z'
        self.event['params']['Operation'] = 'REPLACE'
        self.event['params']['Old'] = old
        self.event['params']['New'] = new

        transformed = handler(self.event, None)
        self.assertEqual(transformed['status'], 'success')
        response = transformed.get('fragment', [])
        
        for i in range(0, len(self.input_list)):
            self.assertEqual(str(self.input_list[i]).replace(old, new), response[i])
    
    def test_operation_not_found(self, *_, **__):
        self.event['params']['Operation'] = 'not-found'

        transformed = handler(self.event, None)
        self.assertEqual(transformed['status'], 'failure')
        self.assertEqual(transformed['errorMessage'], 'Operation not found')


suite_tests = TestSuite()
suite_tests.addTest(makeSuite(TestMapArray))

runner = TextTestRunner()
runner.run(suite_tests)

