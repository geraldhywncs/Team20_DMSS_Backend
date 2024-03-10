# README

## Docker Setup

- Run `npm run docker:build` to build the docker image.
- Run `npm run docker:run` to start and run the docker container using the docker image (for first time only).
- Run `npm run docker:start` if container exists but not running.

## Docker Backend Image Build

1. docker build -t java_api_image -f Dockerfile_java .
2. docker build -t python_api_image -f Dockerfile_python .
3. docker run -p 8080:8080 java_api_image
4. docker run -p 8081:8081 python_api_image

## Python Backend Local Setup

1. Open anaconda prompt
2. conda create -n moneyGoWhere python=3.11.7
3. conda activate moneyGoWhere
4. cd path/to/requirement.txt
5. pip install -r requirement.txt
6. Open ..src/main/python/config.ini
7. Edit USERNAME, PASSWORD, PORT

## Java Backend Local Setup

1. Open command prompt
2. cd path/to/project
3. mvn clean install
4. cd target
5. java -jar Money-Go-Where-0.0.1-SNAPSHOT.jar

## Postman

1. Open Postman
2. Import setup/moneyGoWhere.postman_collection.json
3. After setup, try to call the api

## Docker MySQL

1. docker build -t mysql_server_1 -f Dockerfile_mysql_server_1 .
2. docker run -d --name mysql_instance_1 -p 3306:3306 mysql_server_1
3. docker start mysql_instance_1
4. docker exec -it mysql_instance_1 mysql -uroot -p
   \n password = default1111
