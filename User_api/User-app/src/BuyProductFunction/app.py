import os
import json
import boto3
from decimal import Decimal
import requests

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
       
        table = conect_db()
        items = json.loads(event['body'])

        print(items)

        if items and items['product'] and items['user'] and items['quantidade']:
             
            
            api_url = os.environ['INVENTORYAPIURL'] + "/inventory/buy-product/"
            
            #Envia requisição de compra para o Microsserviço Inventory_api 
            requestBuy = requests.post(api_url,json=items)
            
            compra = json.loads(requestBuy.text,parse_float=Decimal)
            
            if compra["sucess"] == True:
                
                table = conect_db()

                table.put_item(Item=compra)
                
                response = {
                "statusCode": 200,
                "body": json.dumps(f'Compra processada, id compra: { compra["id"] } !!!')}
            
            else:
                response = {
                "statusCode": 400,
                "body": json.dumps(f'Nao foi possivel concluir compra!!!')}  

    except:
        response = {
            "statusCode": 400,
            "body": json.dumps('Bad request !')}


    return response
