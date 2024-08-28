from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_grafana as grafana,
)
from constructs import Construct

class GrafanaWorkspaceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # IAM Role for Grafana Workspace
        grafana_role = iam.Role(
            self,
            "GrafanaRole",
            role_name=f"grafana-workspace-role",
            assumed_by=iam.ServicePrincipal("grafana.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonGrafanaCloudWatchAccess"),
            ],
        )

        ## Grafana Workspace
        grafana.CfnWorkspace(
            self,
            "GrafanaWorkspace",
            name=f"grafana-workspace-dev",
            authentication_providers=["AWS_SSO"],
            account_access_type="CURRENT_ACCOUNT",
            permission_type="SERVICE_MANAGED",
            role_arn=grafana_role.role_arn,
            data_sources=["CLOUDWATCH"],
            notification_destinations=["SNS"],
        )
