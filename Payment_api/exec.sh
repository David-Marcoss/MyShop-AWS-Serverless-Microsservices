cd Payment-app;
docker run --name dynamodb3 -p 8002:8000 -d -v DynamodbVolume:/var/lib/dynamodb amazon/dynamodb-local;
aws dynamodb create-table --cli-input-json file://db/create-table-boleto.json --endpoint-url http://localhost:8002;
sam build;
sam local start-api -p 3002;
