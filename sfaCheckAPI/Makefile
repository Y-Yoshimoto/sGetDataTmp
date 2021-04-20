NAME=python_dev
VERSION=0.1

build:
	docker-compose build

start:
	docker-compose up -d
	docker-compose ps 
restart:
	docker-compose restart

recreate:
	docker-compose down
	docker-compose up -d

rebuild:
	docker-compose build
	docker-compose down
	docker-compose up -d
	docker-compose ps 

fullbuild:
	docker-compose down --rmi all --volumes
	docker-compose up -d --build
	docker ps -a

exec:
	docker exec -it python_dev /bin/ash

logs:
	docker-compose logs -f

down: 
	docker-compose down