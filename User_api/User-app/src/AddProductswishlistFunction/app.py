import os
import json
import requests

def lambda_handler(event, context):
        
    items = json.loads(event['body'])

    try:    
       if (items['user'] and items['product'] and items["quantidade"]):

        api_url = os.environ['INVENTORYAPIURL'] + "/inventory/add-product-wishlist/"

        req = requests.post(api_url,json=items)
    
        response = {
            "statusCode": 200,
            "body": req.text}
    except:

        response = {
            "statusCode": 400,
            "body": json.dumps('Bad request !')}


    return response
