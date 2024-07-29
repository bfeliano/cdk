from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_ssm as ssm,
    aws_lambda as lambda_,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_kms as kms,
    aws_s3_notifications as s3_notifications,
    aws_lambda_event_sources as lambda_event_sources
)
from constructs import Construct
import os

class MonitoringPyStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Retrieve the KMS key ARN from SSM parameter store
        kms_key_ssm = ssm.StringParameter.from_string_parameter_name(
            self, "KmsKeyArnParam", string_parameter_name="/my/kms/keyarn"
        ).string_value
        kms_key = kms.Key.from_key_arn(self, "kmsKey", kms_key_ssm)

        # S3 bucket
        monitoring_bucket = s3.Bucket(self, "monitoringBucket",
                                bucket_name="my-monitoring-bucket-28072024",
                                encryption=s3.BucketEncryption.KMS,
                                encryption_key=kms_key)

        # SQS Dead letter queue
        monitoring_dlq = sqs.Queue(self, "monitoringDlq",
                        queue_name="monitoringDlq")

        # SQS Queue
        monitoring_queue = sqs.Queue(self, "monitoringQueue",
                            queue_name="monitoringQueue",
                            dead_letter_queue=sqs.DeadLetterQueue(
                                max_receive_count=3,
                                queue=monitoring_dlq
                            ))

        # IAM role for Lambda function
        lambda_role = iam.Role(self, "monitoringLambdaRole",
                                assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
                                managed_policies=[
                                    iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                                    iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess")
                                ])

        # Add the permission for CloudWatch:PutMetricData
        lambda_role.add_to_policy(iam.PolicyStatement(
            actions=["cloudwatch:PutMetricData"],
            resources=["*"]
        ))

        # Lambda function
        monitoring_lambda = lambda_.Function(self, "monitoringFunction",
                                        runtime=lambda_.Runtime.PYTHON_3_12,
                                        handler="monitoring.handler",
                                        code=lambda_.Code.from_asset(os.path.join(os.path.dirname(__file__), "../lambda")),
                                        role=lambda_role,
                                        environment={
                                            "QUEUE_URL": monitoring_queue.queue_url,
                                        })
       
        # Grant the Lambda function read permissions on the S3 bucket
        monitoring_bucket.grant_read(lambda_role)

        # Add S3 event notification to send message to SQS
        monitoring_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3_notifications.SqsDestination(monitoring_queue)
        )

        # Add event source mapping Lambda function to SQS Queue
        monitoring_lambda.add_event_source(lambda_event_sources.SqsEventSource(monitoring_queue))

        # Grant SQS Queue permissions to Lambda function
        monitoring_queue.grant_send_messages(monitoring_lambda)
