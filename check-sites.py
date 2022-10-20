import json
import os
import boto3

#connexion lab via aws profile
session = boto3.Session(profile_name='your aws profile')
ec2client=session.client('ec2')
asg=session.client('autoscaling')

# initiation du dictionnaire asgsites qui contiendra les numéro de sites pour chaaue groupe
asgsites={}


#############################################################################################
#   Creation dictionnaire pour les valeurs ASGGROUP/IDSITES
#############################################################################################

#On recupère la liste des tags sites pour les groupes autoscalings qui ont une balise avec la clé 'Sites'
retasgtags = asg.describe_tags(
      Filters=[
        {
            'Name': 'key',
            'Values': [
                'Sites',
            ],
        },
    ],
)

#On enregistre dans un dictionnaire agsite la valeur du site, pour chaque valeur la clé est le nom du groupe
for tags in (retasgtags['Tags']):
    asgsites[tags['ResourceId']]=tags['Value']
    
print(asgsites)


#############################################################################################
# Modif sur Autoscaling: 
# 1- On liste les instance pour chaque groupe d'autoscaling 
# 2- Pour chaque instance on check la présence d'un tag
# 3- Si tag Sites présent on le compare avec le dictionnaire de l'asg
# 4- Si tag non conforme on le change
#############################################################################################

#On liste les instances présents dans les groupes d'autoscaling
asginstances=asg.describe_auto_scaling_instances()


for k in asginstances['AutoScalingInstances']:
    print("#####")
    print("Verification Instance {} dans ASG {}".format(k['InstanceId'],k['AutoScalingGroupName']))
    print("Result:")
    instanceinfo = ec2client.describe_tags(
        Filters=[
            {
                'Name': 'resource-id',
                "Values" : [
                    k['InstanceId'],
                ]
            },
            {
                'Name': 'key',
                "Values" : [
                    'Sites',
                ]
            },
        ],
    )
    for t in instanceinfo['Tags']:
        if (t['Value']==asgsites[k['AutoScalingGroupName']]):
            print("----tags site conforme----")
            print ("EC2:Le Tag Sites de l'instance {} de l'ASG {} est {} ".format(t['ResourceId'],k['AutoScalingGroupName'],t['Value']))
            print ("ASG: Le Tag Site de l'ASG {} est {}".format(k['AutoScalingGroupName'],asgsites[k['AutoScalingGroupName']]))
        else:
            print("non conforme")
            print ("EC2:Le Tag Sites de l'instance {} de l'ASG {} est {} ".format(t['ResourceId'],k['AutoScalingGroupName'],t['Value']))
            print ("ASG: Le Tag Site de l'ASG {} est {}".format(k['AutoScalingGroupName'],asgsites[k['AutoScalingGroupName']]))
            modiftags=ec2client.create_tags(
                Resources=[
                    t['ResourceId'],
                ],
                Tags=[
                    {
                        'Key': 'Sites',
                        'Value': asgsites[k['AutoScalingGroupName']]
                    },
                ]
            )
    print("-----")

    


