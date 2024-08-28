import aws_cdk as core
import aws_cdk.assertions as assertions

from grafana_workspace.grafana_workspace_stack import GrafanaWorkspaceStack

# example tests. To run these tests, uncomment this file along with the example
# resource in grafana_workspace/grafana_workspace_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = GrafanaWorkspaceStack(app, "grafana-workspace")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
