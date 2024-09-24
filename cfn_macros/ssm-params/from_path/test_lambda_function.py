import os
from dotenv import load_dotenv
load_dotenv(override=True)

from unittest import TestCase, TestSuite, makeSuite, TextTestRunner
from lambda_function import handler
from uuid import uuid4

ENVIRONMENT = os.environ['ENVIRONMENT']
APP_NAME = os.environ['APP_NAME']

class TestReadSSM(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.event = {
            "requestId": str(uuid4()),
            "params": {
                "Path": f"/config/infra/{APP_NAME}/vpc-networking/cidr-private-subnet/"
            }
        }
    
    def test_read_from_path(self, *_, **__):
        transformed = handler(self.event, None)
        self.assertEqual(transformed['status'], 'success')
        response = transformed.get('fragment', [])

        self.assertGreater(len(response), 0)



suite_tests = TestSuite()
suite_tests.addTest(makeSuite(TestReadSSM))

runner = TextTestRunner()
runner.run(suite_tests)

