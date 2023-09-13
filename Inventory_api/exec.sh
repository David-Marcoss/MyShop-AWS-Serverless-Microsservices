cd Inventory-app;
docker run --name dynamodb1 -p 8000:8000 -d -v DynamodbVolume:/var/lib/dynamodb amazon/dynamodb-local;
aws dynamodb create-table --cli-input-json file://db/create-table-products.json --endpoint-url http://localhost:8000;
aws dynamodb create-table --cli-input-json file://db/create-table-wishlist.json --endpoint-url http://localhost:8000;
sam build;
sam local start-api -p 3000;
