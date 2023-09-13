import os
import json
import requests


def lambda_handler(event, context):

    try: 
        items = {}       
        
        #faz a comunicação com o microsservirço Inventory-api
        api_url = os.environ['INVENTORYAPIURL'] + "/inventory/get-products/"
        items = requests.get(api_url)
        
        response = {
            "statusCode": 200,
            "body": items.text}
    
    
    except:
        response = {
            "statusCode": 400,
            "body": json.dumps("Bad Request!"),}
        

    return response
