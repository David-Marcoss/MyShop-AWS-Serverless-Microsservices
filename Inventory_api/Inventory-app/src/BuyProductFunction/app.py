import os
import json
import boto3
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

"""verifica se o produto está ativo e se possui quantidade
para a venda"""
def validade_buy(product, quantidade):
    valid = False
    
    if product['ativo'] == "True" and quantidade > 0 and quantidade <= product['quantidade']:
        valid = True
    
    return valid

#atualiza quantidade do produto depois de uma venda
def updateQuantity_product(table,product,quantidade):

    product['quantidade']-=quantidade

    if product['quantidade'] == 0:
        product['ativo'] = "False"
        table.update_item(Key={'id':product['id']},
            AttributeUpdates={"quantidade":{'Value':product['quantidade']},"ativo":{'Value':product['ativo']}})
    else:

        table.update_item(Key={'id':product['id']},
            AttributeUpdates={"quantidade":{'Value':product['quantidade']}})


def lambda_handler(event, context):

    compra =  {'sucess': False}
    response = {
        "statusCode": 400,
        "body": json.dumps(compra)}

    try:
        data = json.loads(event['body'])

        if data and data['product'] and data['user'] and data['quantidade']:
            
            table_product = conect_db()
            
            product = table_product.get_item(Key={"id": data['product']})['Item']

            if validade_buy(product,data['quantidade']):
                
                #enviando req para o microserviço Payment_api

                req_payment_data = {
                    'product': product['id'], 
                    'user': data['user'],
                    'quantidade': data['quantidade'],
                    'valor': float(data['quantidade'] * product['valor'])}
                        
                api_url = os.environ['INVENTORYAPIURL'] + "/Payment/payment-ticket/"
                
                requestPayment = requests.post(api_url,json = req_payment_data).text

                updateQuantity_product(table_product,product,data['quantidade'])
                
                response = {
                    "statusCode": 200,
                    "body": requestPayment}

    except:
      pass

    return response
