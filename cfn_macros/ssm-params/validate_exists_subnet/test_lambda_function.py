import os
from dotenv import load_dotenv
load_dotenv(override=True)

from unittest import TestCase, TestSuite, makeSuite, TextTestRunner, mock
from botocore.exceptions import ClientError
from lambda_function import handler
from uuid import uuid4

ENVIRONMENT = os.environ['ENVIRONMENT']
APP_NAME = os.environ['APP_NAME']

class MockSSM:
    def get_parameter(*args, Name, **kwargs):
        if Name == 'not_exists':
            raise ClientError({
                'Error': {
                    'Code': 'ParameterNotFound'
                }
            }, 'ssm')
        elif Name == '/my-awesome-param/exists':
            return {
                'Parameter': {'value': '10.24.0.0/32'}
            }

@mock.patch(f"boto3.client", return_value=MockSSM())
class TestValidateSSMSubnet(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.event = {
            "requestId": str(uuid4())
        }
    
    def test_not_exists_and_bad_cidr_format(self, *_, **__):
        self.event['params'] = {
            "Path": "not_exists"
        }
        transformed = handler(self.event, None)
        self.assertEqual(transformed['status'], 'failure')
        self.assertEqual(transformed['errorMessage'], 'Invalid CIDR format')
    
    def test_not_exists_and_bad_cidr_format(self, *_, **__):
        self.event['params'] = {
            "Path": "not_exists"
        }
        self.event['params']['VpcCidr'] = '10.24.0.0/24'
        self.event['params']['SubnetMask'] = '/8'
        transformed = handler(self.event, None)
        self.assertEqual(transformed['status'], 'failure')
        self.assertEqual(transformed['errorMessage'], 'The provided mask is not within the range of the given CIDR')
    
    def test_read_from_path(self, *_, **__):
        self.event['params'] = {
            "Path": f"/my-awesome-param/exists"
        }
        self.event['params']['VpcCidr'] = '10.24.0.0/24'
        self.event['params']['SubnetMask'] = '/32'
        transformed = handler(self.event, None)
        self.assertEqual(transformed['status'], 'success')

        response = transformed['fragment']
        self.assertEqual(response, '10.24.0.0/32')
    
    def test_not_exists_good_input(self, *_, **__):
        self.event['params'] = {
            "Path": "not_exists"
        }
        self.event['params']['VpcCidr'] = '15.67.0.0/24'
        self.event['params']['SubnetMask'] = '/32'
        transformed = handler(self.event, None)
        self.assertEqual(transformed['status'], 'success')

        response = transformed['fragment']
        self.assertEqual(response, '15.67.0.0/32')



suite_tests = TestSuite()
suite_tests.addTest(makeSuite(TestValidateSSMSubnet))
#validate_ssm_test = TestValidateSSMSubnet()
#validate_ssm_test.setUp()
#suite_tests.addTest(validate_ssm_test.test_not_exists_good_input)

runner = TextTestRunner()
runner.run(suite_tests)

