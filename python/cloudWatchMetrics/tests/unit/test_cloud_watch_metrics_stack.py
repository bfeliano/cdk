import aws_cdk as core
import aws_cdk.assertions as assertions

from cloud_watch_metrics.cloud_watch_metrics_stack import CloudWatchMetricsStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cloud_watch_metrics/cloud_watch_metrics_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CloudWatchMetricsStack(app, "cloud-watch-metrics")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
