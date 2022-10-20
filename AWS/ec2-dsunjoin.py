#execute a ssm document on ec2 in asg, the ssm document disable the auto domain unjoin 

import json
import boto3
import time
import os

ec2 = boto3.client('ec2')
asg = boto3.client('autoscaling')
ssm = boto3.client('ssm')


#indicate your asg
group_asg = ['asg_group_1','asg_group_2']


def lambda_handler(event, context):
    retasgs = asg.describe_auto_scaling_instances()
    print(retasgs)
    for retasg in (retasgs['AutoScalingInstances']):
        if retasg['AutoScalingGroupName'] in group_asg:
            print(retasg['InstanceId'])
            response = ssm.send_command(InstanceIds=[retasg['InstanceId'],],DocumentName='ssm_disable_unjoin',DocumentVersion='$LATEST',CloudWatchOutputConfig={'CloudWatchOutputEnabled': True})