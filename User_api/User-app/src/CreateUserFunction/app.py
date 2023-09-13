import os
import json
import boto3
from decimal import Decimal

#conecta com a tabela do bd
def conect_db():
    table_name = os.environ['TABLE']
    region = os.environ['REGION']
    aws_environment = os.environ['AWSENV']
    db_conection = os.environ['DBLOCALURL']
    
    # Check if executing locally or on AWS, and configure DynamoDB connection accordingly.
    if aws_environment == "AWS_SAM_LOCAL":
        table = boto3.resource('dynamodb', endpoint_url=db_conection).Table(table_name)
    
    else:
        # AWS
        table = boto3.resource('dynamodb', region_name=region).Table(table_name)
    
    return table


def lambda_handler(event, context):

    try:  
       items = json.loads(event['body'])
       table = conect_db()
       
       if (items['id'] and items['nome'] and items['email'] and items["senha"]):
    
        table.put_item(Item=items)
            
        response = {
            "statusCode": 200,
            "body": json.dumps(f'Usuario cadastrado!!!')}
    except:

        response = {
            "statusCode": 400,
            "body": json.dumps('Bad request !')}


    return response
