import socket
import time
import boto3
cloudwatch = boto3.client('cloudwatch')

def lambda_handler(event, context):
    ec2_ip = '10.141.19.71' 
    port = 443

    # Check port 443 connectivity
    result = check_port(ec2_ip, port)

    cloudwatch.put_metric_data(
        Namespace='DydraEC2',
        MetricData=[
            {
                'MetricName': 'Port443Status',
                'Dimensions': [
                    {
                        'Name': 'InstanceIP',
                        'Value': '10.141.19.71'
                    },
                ],
                'Timestamp': time.time(),
                'Value': result,
                'Unit': 'Count'
            },
        ]
    )
    return {
        'statusCode': 200,
        'body': result
    }

def check_port(ip, port):
    try:
        # Establish a connection to the EC2 IP and port
        with socket.create_connection((ip, port), timeout=5) as s:
            return 1  # Port is open
    except (socket.timeout, socket.error):
        return 0  # Port is closed or unreachable
