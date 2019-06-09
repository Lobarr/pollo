init:
	pip install -r requirements.txt

start:
	docker build -t pollo:prod .
	docker run -d --rm -p 80:3000 pollo:prod

freeze: 
	pip freeze > requirements.txt

test:
	python -m pytest 

test-docker:
	docker build -t pollo:test -f Dockerfile.test .
	docker run --rm pollo:test
