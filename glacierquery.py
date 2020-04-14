from __future__ import print_function
import json
import urllib
import boto3
import uuid
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Global parameters
archiveid = os.getenv('archiveid')
vault = os.getenv('vaultname')
s3bucket= os.getenv('bucketname')
s3prefix= os.getenv('prefix')


glacier = boto3.client('glacier')

logger.info('starting Lambda')

def lambda_handler(event, context):

    
   #glacier block
     
    logger.info('starting glacier block')
    print(archiveid)
    try:
		jobParameters = {"Type": "select", "ArchiveId": archiveid,"Tier": "Expedited", "SelectParameters": {
        "InputSerialization": {"csv": {}},
        "ExpressionType": "SQL",
        "Expression": "select * from archive s",
        "OutputSerialization": {
            "csv": {}
        }
		},
		"OutputLocation": {
        "S3": {"BucketName": s3bucket, "Prefix":s3prefix}
		}
		}
		response=glacier.initiate_job(vaultName=vault, jobParameters=jobParameters)
        
    except Exception as e:
      print(e)
      print("Error selecting data from archive ", archiveid, "from vault ", vault, "to bucket",s3bucket)
      raise e  
    logger.info('downloaded data from glacier archive')
    print(response)
    return response
