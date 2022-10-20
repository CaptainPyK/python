#suspend asg scaling processes

import json
import boto3
import time
import os


ec2 = boto3.client('ec2')
asg = boto3.client('autoscaling')

#indicate your asg
group_asg = ['asg_group_1','asg_group_2']


def lambda_handler(event, context):
    retasgs = asg.describe_auto_scaling_groups()
    print(retasgs)
    for retasg in (retasgs['AutoScalingGroups']):
        if retasg['AutoScalingGroupName'] in group_asg:
            print(retasg['AutoScalingGroupName'])
            suspendasg = asg.suspend_processes(AutoScalingGroupName=retasg['AutoScalingGroupName'],ScalingProcesses=['Terminate','HealthCheck'])