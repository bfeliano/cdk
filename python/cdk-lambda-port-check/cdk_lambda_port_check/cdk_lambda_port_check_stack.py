from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_ec2 as ec2,
    aws_events as events,
    aws_events_targets as targets,
)
from constructs import Construct
import os


class CdkLambdaPortCheckStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Retrieve existing VPC values to be used by the Lambda function
        # Replace xxxx values for VPC, Subnets and Security Group with your existing ones
        vpc = ec2.Vpc.from_lookup(self, 'myExistingVpc', vpc_id='vpc-xxxx')
        subnet_selection = ec2.SubnetSelection(
            subnet_filters=[
                ec2.SubnetFilter.by_ids(
                    subnet_ids=["subnet-xxxx", "subnet-xxxx"]
                )
            ]
        )
        security_group = ec2.SecurityGroup.from_security_group_id(self, 'MyExistingSG', "sg-xxxx")

        # IAM role to be used by Lambda function
        lambda_role = iam.Role(self, "portCheckLambdaRole",
            role_name="lambda-port-check-iam-role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"),
                iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
            ])

        # Lambda function
        lambda_function = lambda_.Function(self, "portCheckLambdaFunction",
            function_name="lambda-port-check-function",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="handler.lambda_handler",
            code=lambda_.Code.from_asset(os.path.join(os.path.dirname(__file__), "../lambda_code")),
            role=lambda_role,
            timeout=Duration.seconds(30),
            vpc=vpc,
            vpc_subnets=subnet_selection,
            security_groups=[security_group],
        )

        # Event Bridge Rule triggered every minute
        rule = events.Rule(self, "portCheckLambdaTrigger",
                           rule_name="lambda-port-check-trigger",
                           schedule=events.Schedule.rate(Duration.minutes(1))
                           )

        # Add the lambda function as the rule's target
        rule.add_target(targets.LambdaFunction(lambda_function))