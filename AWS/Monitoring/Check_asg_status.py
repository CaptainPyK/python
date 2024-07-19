#! /usr/bin/python

import json
import os
import argparse
import sys
import boto3
import yaml


NAGIOSUNKNOWN = -1
NAGIOSOK = 0
NAGIOSWARNING = 1
NAGIOSCRITICAL = 2

#For Read the args 
def read_args():
    parser = argparse.ArgumentParser(
       description= "You can check the desired capacity of an aws AutoScaling Group",
       epilog= ":)"
    )
    parser.add_argument("-awsregion", "--awsregion", help="--> You're AWS KEY For IAM USER, parameter is required",required=True)
    parser.add_argument("-awskey", "--awskey", help="--> You're AWS KEY For IAM USER, parameter is required",required=True)
    parser.add_argument("-awssecret", "--awssecret", help="--> You're AWS SECRET For IAM USER, parameter is required",required=True)
    parser.add_argument("-asg", "--asg", help="--> You're autoscaling Group Name, parameter is required",required=True)
    parser.add_argument("-w","--warning",type=int, help="--> warning value for desired capacity")
    parser.add_argument("-c","--critical",type=int, help="--> critical value for desired capacity")
    args=parser.parse_args()
    return args

# Configure AWS boto3 session
def config_session_boto3(awskey,awssecret,awsregion):
    try:
        session = boto3.Session(aws_access_key_id=awskey,aws_secret_access_key=awssecret,region_name=awsregion)
        asg=session.client('autoscaling')
        return asg
    except:
        print("Please Check your AWS Credential")

# Retrieve Asg value in AWS
def asg_infos(asg_name,asg):

    try:
        decribeasg = asg.describe_auto_scaling_groups(
        AutoScalingGroupNames=[
            asg_name,
        ],
        )
        asg_params=decribeasg["AutoScalingGroups"][0]

        actualcapacity= {"min": asg_params["MinSize"], "max": asg_params["MaxSize"], "desired": asg_params["DesiredCapacity"]}

        #print(f'ASG: {asg_name}, min : {actualcapacity["min"]} , max : {actualcapacity["max"]}, DesiredCapacity : {actualcapacity["desired"]}')
        return actualcapacity
    except:
       print("Please Check your AutoscalingGroup Name")
       sys.exit(NAGIOSUNKNOWN)

# Processing alert Value
def alert_analyser(asg_name,warning,critical,agscap):
    #print(f'warning : {warning} ; critical : {critical} ; asgvalue_min : {agscap["min"]} ; asgvalue_max : {agscap["max"]} ; asgvalue_desired : {agscap["desired"]}')
    status = f' => Desired EC2 instances Value in {asg_name} is {agscap["desired"]}.'
    if warning and critical:
        
        if agscap["desired"] >= critical:
            print(f'CRITICAL{status}')
            sys.exit(NAGIOSCRITICAL)

        elif agscap["desired"] >= warning:
            print(f'WARNING{status}')
            sys.exit(NAGIOSWARNING)

        else:
            print(f'OK{status}')
            sys.exit(NAGIOSOK)
    else:
        print(f'Please indicates -w and -c Values{status}')
        sys.exit(NAGIOSUNKNOWN)


def main():
   param_checks = read_args()
   asg_session=config_session_boto3(param_checks.awskey,param_checks.awssecret,param_checks.awsregion)
   infosaws=asg_infos(param_checks.asg,asg_session)
   alert_analyser(param_checks.asg,param_checks.warning,param_checks.critical,infosaws)



if __name__ == '__main__':
  main()