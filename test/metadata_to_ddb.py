import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('VisualSearchMetadata')


with open('./metadata.json') as json_data:
    products = json.load(json_data)

for product in products:

    response = table.put_item(Item=product)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        pass
    else:
        print('FAILURE TO WRITE')
        break
