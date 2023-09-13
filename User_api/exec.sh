cd User-app;
docker run --name dynamodb2 -p 8001:8000 -d -v DynamodbVolume:/var/lib/dynamodb amazon/dynamodb-local;
aws dynamodb create-table --cli-input-json file://db/create-table-User.json --endpoint-url http://localhost:8001;
aws dynamodb create-table --cli-input-json file://db/create-table-BuysUser.json --endpoint-url http://localhost:8001;
sam build;
sam local start-api -p 3001;
