#! /usr/bin/python
# Work in progress lol
import json
import os
import argparse
import sys
import boto3



NAGIOSUNKNOWN = -1
NAGIOSOK = 0
NAGIOSWARNING = 1
NAGIOSCRITICAL = 2


accesskey=""
accesssecret=""
region="eu-west-3"


#For Read the args 
def read_args():
    parser = argparse.ArgumentParser(
       description= "You can check the desired capacity of an aws AutoScaling Group",
       epilog= ":)"
    )
    #parser.add_argument("-awsregion", "--awsregion", help="--> You're AWS KEY For IAM USER, parameter is required",required=True)
    #parser.add_argument("-awskey", "--awskey", help="--> You're AWS KEY For IAM USER, parameter is required",required=True)
    #parser.add_argument("-awssecret", "--awssecret", help="--> You're AWS SECRET For IAM USER, parameter is required",required=True)
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

def asg_infos(asg_name,asg):

    decribeasg = asg.describe_auto_scaling_groups(
    AutoScalingGroupNames=[
        asg_name,
    ],
    )
       



def main():
   param_checks = read_args()
   #asg_session=config_session_boto3(param_checks.awskey,param_checks.awssecret,param_checks.awsregion)
   asg_session=config_session_boto3(accesskey,accesssecret,region)
   infosaws=asg_infos(param_checks.asg,asg_session)
   



if __name__ == '__main__':
  main()