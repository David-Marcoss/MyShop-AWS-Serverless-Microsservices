import os
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

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

    table = conect_db()

    if event['path'] == "/User/get-all-buys/":

        response = table.scan()
        items = response['Items']
 
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])
        
        
        response = {
            "statusCode": 200,
            "body": json.dumps(f"Buys: {items}"),}
    
    else:

        id = event['queryStringParameters']

        if id:
        
            items = table.query(
                IndexName='user-index',
                ProjectionExpression = 'id, product, valor, quantidade',
                KeyConditionExpression=Key('user').eq(id['id'])
            )
   
            response = {
                "statusCode": 200,
                "body": f"Compras do usuario {id}: {items['Items']}"}
        
        
        
        else:
            response = {
                "statusCode": 400,
                "body": json.dumps("Informe um id para a busca !"),}
        
    return response