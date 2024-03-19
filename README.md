# README

## Docker MySQL

Note: Run steps 1-6 if first time. Run steps 4-6 if already created before.

1. docker network create dmss (Create docker network if not yet created)
2. docker build -t dmss_mysql_image -f Dockerfile.mysql .
3. docker run -d --name dmss_mysql_container --network=dmss -p 3306:3306 dmss_mysql_image
4. docker start dmss_mysql_container
5. docker exec -it dmss_mysql_container mysql -uroot -p
6. Note: password = default1111

## Docker Python

1. docker network create dmss (Create docker network if not yet created)
2. docker build -t dmss_python_image -f Dockerfile.python .
3. docker rm -f dmss_python_container || true && docker run -d -e DOCKER_CONTAINER=true --name dmss_python_container --network=dmss -p 5000:5000 dmss_python_image

## Backend Local Setup Python

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
