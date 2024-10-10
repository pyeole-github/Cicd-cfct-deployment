# test_lambda_function.py

import pytest
import boto3
from moto import mock_ec2, mock_sts, mock_ce
from lambda_function import lambda_handler

# Mock the AWS services used by the Lambda function
@mock_sts
@mock_ce
@mock_ec2
def test_lambda_handler():
    # Create a mock event with necessary parameters
    mock_event = {
        'ManagementAccountId': '123456789012',
        'RoleName': 'CostExplorerAccessRole',
        'ALLOCATION_THRESHOLD': 1.00
    }

    # Create a mock context (you can leave it as None if not used)
    mock_context = None

    # Call the Lambda function with the mock event and context
    response = lambda_handler(mock_event, mock_context)

    # Assert the expected results
    assert response['statusCode'] == 200
    assert 'Total cost' in response['body']
