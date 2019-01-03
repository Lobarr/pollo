init:
	pip install -r requirements.txt
start:
	docker build -t pollo:prod .
	docker run -d --rm -p 80:3000 pollo:prod