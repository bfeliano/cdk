# Lambda Port Check Project

This project sets up an AWS Lambda Function that checks connectivity of a
specific port on an EC2 instance and record the result in a CloudWatch
custom metric.  
The stack includes a Lambda Function, an IAM role, and a Event Bridge rule.  
Currently, only one Instance and one port is being monitored, but more
instances or ports can be added to the code, located in
[lambda_code/handler.py](./lambda_code/handler.py).  

## Components

1. **IAM Role**: Grants the Lambda function the necessary permissions
to interact with CloudWatch.
2. **Lambda Function**: Check connectivity with a specific IP/Port and
sends the results to a custom metric in CloudWatch.
3. **Event Bridge Rule**: Trigger the Lambda every minute.

## Directory Structure

├── cdk_lambda_port_check/  
│  └── cdk_lambda_port_check_stack.py  
├── lambda_code/  
│  └── handler.py  
└──  app.py  

## Deployment

### Prerequisites

1. AWS CLI configured with your credentials.
2. AWS CDK installed (npm install -g aws-cdk).

### Steps

1. Install Dependencies  
`pip install -r requirements.txt`

2. Bootstrap CDK Environment  
`cdk bootstrap`

3. Deploy the Stack  
`cdk deploy`

### Cleanup

1. To delete the stack and all resources:  
`cdk destroy`
