#! /usr/bin/python

import argparse
import sys
import os
import boto3

NAGIOSUNKNOWN = -1
NAGIOSOK = 0
NAGIOSWARNING = 1
NAGIOSCRITICAL = 2

accesskey=""
accesssecret=""
region="eu-west-3"


# Read the args arguments
def read_args():
    parser = argparse.ArgumentParser(
       description= "You can check the Status of an cloudwatch alarm",
       epilog= ":)"
    )
    #parser.add_argument("-awsregion", "--awsregion", help="--> You're AWS KEY For IAM USER, parameter is required",required=True)
    #parser.add_argument("-awskey", "--awskey", help="--> You're AWS KEY For IAM USER, parameter is required",required=True)
    #parser.add_argument("-awssecret", "--awssecret", help="--> You're AWS SECRET For IAM USER, parameter is required",required=True)
    parser.add_argument("-cw", "--cwalarm", help="--> You're Cloudwatch Alarm Name, parameter is required",required=True)
    args=parser.parse_args()
    return args

# Configure AWS boto3 session
def config_session_boto3(awskey,awssecret,awsregion):
    try:
        session = boto3.Session(aws_access_key_id=awskey,aws_secret_access_key=awssecret,region_name=awsregion)
        cw = session.resource('cloudwatch')
        return cw
    except:
        print("Please Check your AWS Credential")

def check_alarms(Alarm_name,cw):
    Alarm_result = cw.Alarm(Alarm_name)
    status = ' => The Cloudwatch Alarm {0} is {1}.'.format(Alarm_result.alarm_name,Alarm_result.state_value)
    if Alarm_result.state_value == 'OK':
        print('OK{0}'.format(status))
        sys.exit(NAGIOSOK)
    else:
        print('CRITICAL{0}'.format(status))
        sys.exit(NAGIOSCRITICAL)


def main():
   param_checks = read_args()
   cw=config_session_boto3(accesskey,accesssecret,region)
   check_alarms(param_checks.cwalarm,cw)

if __name__ == '__main__':
  main()