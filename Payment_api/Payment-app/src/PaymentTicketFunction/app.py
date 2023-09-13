from decimal import Decimal
import os
import json
import boto3
import uuid

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
        items = json.loads(event['body'], parse_float=Decimal)


        if items and items["product"] and items["user"] and items["quantidade"] and items["valor"]:
            
            table = conect_db()

            items['id'] = str(uuid.uuid4())
            
            table.put_item(Item=items)

            items['sucess'] = True
            items['valor'] = float(items['valor'])
            
            response = {
                "statusCode": 200,
                "body": json.dumps(items)}
        else:
            response = {
            "statusCode": 400,
            "body": 'Bad Request!!'}
    except:

        response = {
            "statusCode": 400,
            "body": 'Bad Request!!'}

    return response