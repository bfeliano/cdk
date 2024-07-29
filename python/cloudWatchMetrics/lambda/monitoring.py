import boto3
import os
import json

s3_client = boto3.client('s3')
cloudwatch = boto3.client('cloudwatch', 'eu-west-1')

def handler(event, context):
    # Looping every SQS message
    for sqs_record in event ['Records']:
        s3_event = json.loads(sqs_record['body'])
        # Looping every record in the S3 Event Notification
        for s3_record in s3_event.get('Records', []):
            bucket_name = s3_record['s3']['bucket']['name']
            key = s3_record['s3']['object']['key']
            try:
                # Retrieve the JSON file from S3
                response = s3_client.get_object(Bucket=bucket_name, Key=key)
                file_content = response['Body'].read().decode('utf-8')

                # Read values JSON file
                data = json.loads(file_content)
                cycle_end_date = data['cycleEndDate']
                max_time_for_info1_fetch = data['Information1']['maxTimeForFetch']
                max_time_for_info2_fetch = data['Information2']['maxTimeForFetch']
                skipped_resources = data['cycleStatus']['skippedResources']

                # Extract the app name from the file name
                file_name = key.split('/')[-1]  # Get the file name from the key
                app_name = file_name.split('_')[0]  # Extract the first part of the file name

                # Add here the metric data
                maxTimeForInfo1Fetch = {
                    'MetricName': 'maxTimeForInfoFetch',
                    'Dimensions': [
                        {
                           'Name': 'Applications',
                           'Value': app_name,
                        },
                    ],
                    'Unit': 'Milliseconds',
                    'Value': max_time_for_info1_fetch,
                    'Timestamp': cycle_end_date
                }

                maxTimeForInfo2Fetch = {
                    'MetricName': 'maxTimeForInfo2Fetch',
                    'Dimensions': [
                        {
                           'Name': 'Applications',
                           'Value': app_name,
                        },
                    ],
                    'Unit': 'Milliseconds',
                    'Value': max_time_for_info2_fetch,
                    'Timestamp': cycle_end_date
                }

                skippedResources = {
                    'MetricName': 'skippedResources',
                    'Dimensions': [
                        {
                           'Name': 'Applications',
                           'Value': app_name,
                        },
                    ],
                    'Unit': 'Milliseconds',
                    'Value': skipped_resources,
                    'Timestamp': cycle_end_date
                }

                # Send the metric to cloudWatch
                cloudwatch.put_metric_data(
                    Namespace='ELM_Metrics',
                    MetricData=[maxTimeForInfo1Fetch, maxTimeForInfo2Fetch, skippedResources]
                )
                print('Processed event:', s3_event)
            except Exception as e:
                print(f'Error: {e}')
                return {
                    'statusCode': 500,
                    'body': 'Internal Server Error'
                }
        return {
            'statusCode': 200,
            'body': 'Metric ingested!'
        }