# README

## Docker MySQL

Note: Run steps 1-6 if first time. Run steps 4-6 if already created before.

1. docker network create dmss (Create docker network if not yet created)
2. docker build -t mysql_server_1 -f Dockerfile_mysql_server_1 .
3. docker rm -f mysql_instance_1 || true && docker run -d --name mysql_instance_1 --network=dmss -p 3306:3306 mysql_server_1
4. docker start mysql_instance_1
5. docker exec -it mysql_instance_1 mysql -uroot -p
6. Note: password = default1111

## Docker Backend Image Build - Python

1. docker network create dmss (Create docker network if not yet created)
2. docker build -t python_api_image -f Dockerfile_python .
3. docker rm -f dmss_backend || true && docker run -d -e DOCKER_CONTAINER=true --name dmss_backend --network=dmss -p 5000:5000 python_api_image

## Python Backend Local Setup

1. Open anaconda prompt
2. conda create -n moneyGoWhere python=3.11.7
3. conda activate moneyGoWhere
4. cd path/to/requirement.txt
5. pip install -r requirement.txt 🎇Just to be sure, run this if there are new imports🎇
6. Open ..src/main/python/config.ini
7. Edit USERNAME, PASSWORD, PORT

## Postman

1. Open Postman
2. Import moneyGoWhere.postman_collection.json
3. After setup, try to call the api

## Testing Connection on Postman

1. Create Post Request (http://localhost:5000/currency/currencyConverter)
2. In the body select raw and copy, paste the following

{
"amount": 69.69,
"from_currency": "USD",
"to_currency": "SGD"
}
