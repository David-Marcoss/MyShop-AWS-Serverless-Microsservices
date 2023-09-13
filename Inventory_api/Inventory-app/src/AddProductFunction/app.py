import os
import uuid
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

        items = json.loads(event['body'], parse_float=Decimal)

        product_table = conect_db()

        if event['path'] == "/inventory/add-products/":
     
            if items['id'] and items['nome'] and items["valor"] and items["quantidade"] and items['ativo']:
            
                product_table.put_item(Item=items)
                    
                response = {
                    "statusCode": 200,
                    "body": json.dumps(f'Produto cadastrado!')}

        else:
            msg = ''

            for key,item in items.items():
                try:
                    if item['id'] and item['nome'] and item["valor"] and item["quantidade"] and item['ativo']:        
                        product_table.put_item(Item=item)
                        msg += f"item {key} cadastrado, "     
                    
                except:
                    msg += f"item {key} invalido, "

            response = {
            "statusCode": 200,
            "body": json.dumps(msg)}
    except:
        response = {
            "statusCode": 400,
            "body": json.dumps(f'Bad request!')}

    return response
