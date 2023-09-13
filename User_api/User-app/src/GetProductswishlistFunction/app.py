import os
import json
import requests


def lambda_handler(event, context):

    try: 
        items = {}       
        
        #faz a comunicação com o microsservirço Inventory-api
        api_url = os.environ['INVENTORYAPIURL'] + "/inventory/get-product-wishlist/"
        items = requests.get(api_url)
        
        id = event['queryStringParameters']

        if id:
            
            items = requests.post(api_url,json=id).text
            
            response = {
                "statusCode": 200,
                "body": f"Compras do usuario {id['id']}: {items}"}
        
        else:
            response = {
                "statusCode": 400,
                "body": json.dumps("Informe um id para a busca !"),}
    except:

        response = {
            "statusCode": 400,
            "body": json.dumps("Bad Request!"),}

        
    return response
        

