import boto3
import csv
import os

s3 = boto3.client('s3')
def lambda_handler(event, context):
    r = s3.select_object_content(
        Bucket='buckectname',
        Key='example.csv',
        ExpressionType='SQL',
        #type of the query you want fire on the object
        Expression="select * from s3object s",
        InputSerialization = {'CSV': {"FileHeaderInfo": "Use"}},
        OutputSerialization = {'CSV': {}},
    )
    for event in r['Payload']:
        if 'Records' in event:
            records = event['Records']['Payload'].decode('utf-8')
            with open("/tmp/results.txt","w+") as f:
                #a = csv.writer(f, delimiter='|')
                #a.writerows(records)
                f.writelines(records)
            s3.upload_file("/tmp/results.txt","bucketname","prefix")
            print(records)
        elif 'Stats' in event:
            statsDetails = event['Stats']['Details']
            print("Stats details bytesScanned: ")
            print(statsDetails['BytesScanned'])
            print("Stats details bytesProcessed: ")
            print(statsDetails['BytesProcessed'])
    return records
