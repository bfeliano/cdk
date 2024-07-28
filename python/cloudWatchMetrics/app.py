#!/usr/bin/env python3
import os
import aws_cdk as cdk

from cloud_watch_metrics.cloud_watch_metrics_stack import MonitoringPyStack

target_account = os.environ.get('TARGET_ACCOUNT')
target_region = os.environ.get('TARGET_REGION')
env = {
   'account': target_account or os.environ.get('AWS_DEFAULT_ACCOUNT'),
   'region': target_region or os.environ.get('AWS_DEFAULT_REGION')
}

app = cdk.App()
MonitoringPyStack(app, "MonitoringPyStack", env=env)

app.synth()
