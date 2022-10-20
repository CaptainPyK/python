import json
import boto3
import time
import os

rds = boto3.client('rds')

#indicate your rds
devrds = ['rds-1','rds-2']

def lambda_handler(event, context):
    rdsbases = rds.describe_db_instances()
    print(rdsbases)
    for rdsbase in (rdsbases['DBInstances']):
        if rdsbase['DBInstanceIdentifier'] in devrds:
            print(rdsbase['DBInstanceIdentifier'])
            stoprds = rds.stop_db_instance(DBInstanceIdentifier=rdsbase['DBInstanceIdentifier'])
            print(stoprds)