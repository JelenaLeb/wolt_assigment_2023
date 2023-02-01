SERVER_HOST = 127.0.0.1
SERVER_PORT = 9876

# just install already calculated dependencies
install:
	python3 -m pip install -r requirements.txt -r requirements-dev.txt
.PHONY: install

test:
	python3 -m pytest -v
.PHONY: test

coverage:
	python3 -m pytest --cov=src --cov-branch --cov-report=term-missing
.PHONY: coverage

server:
	uvicorn --host $(SERVER_HOST) --port $(SERVER_PORT) --reload src.api:app
.PHONY: server

request:
	curl -X POST http://$(SERVER_HOST):$(SERVER_PORT)/fee -H 'content-type: application/json' -d '{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2021-10-12T13:00:00Z"}'
	@ echo
.PHONY: request
