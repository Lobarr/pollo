init:
	pip install -r requirements.txt

start-server:
	python app.py

start-client:
	cd client && npm run serve -- --port=3001

start-app:
	docker-compose -f docker-compose.yml kill && docker-compose up --build --remove-orphans

start-docker:
	docker build -t pollo:prod .
	docker run -p 80:3000 pollo:prod

freeze: 
	pip freeze > requirements.txt
