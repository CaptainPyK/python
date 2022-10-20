import json
import boto3
import time
import os

ec2 = boto3.client('ec2')
asg = boto3.client('autoscaling')


#indicate your asg
group_asg = ['asg_group_1','asg_group_2']



def lambda_handler(event, context):
    retasginss = asg.describe_auto_scaling_instances()
    print(retasginss)
    for retasgins in (retasginss['AutoScalingInstances']):
        if retasgins['AutoScalingGroupName'] in group_asg:
            print(retasgins['InstanceId'])
            startinstance = ec2.start_instances(InstanceIds=[retasgins['InstanceId']])
            print(startinstance)
  