# Cloud Watch Custom Metrics Project
This project sets up an AWS infrastructure using AWS CDK. The stack includes an S3 bucket, an IAM role, an SQS queue with a dead-letter queue (DLQ), and a Lambda function triggered by S3 events via SQS.

## Components

1. **S3 Bucket**: Stores files and triggers the Lambda function via SQS on object creation.
2. **IAM Role**: Grants the Lambda function the necessary permissions to interact with S3 and CloudWatch.
3. **SQS Queue**: Receives notifications from S3 events and triggers the Lambda function. It includes a DLQ for failed messages.
4. **Lambda Function**: Processes files uploaded to S3, extracts metrics from the JSON content, and pushes these metrics to CloudWatch.

## Directory Structure

├── cloud_watch_metrics/  
│  └── cloud_watch_metrics_stack.py  
├── lambda/  
│  └── monitoring.py  
└──  app.py  


## Lambda Function

The Lambda function (`lambda/monitoring.py`) processes files uploaded to the S3 bucket. It extracts several metrics from the JSON content of the files and pushes these metrics to CloudWatch.

### Extracted Metrics

1. **maxTimeForInfo1Fetch**
2. **maxTimeForInfo2Fetch**
3. **skippedResources**

All of these are generic metrics that can be updated as needed.

### Example JSON File

[applicationName.json](./applicationName.json) 

## Deployment

### Prerequisites
1. AWS CLI configured with your credentials.
2.  AWS CDK installed (npm install -g aws-cdk).

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
 