DOCKER_IMG := "python-tg-bot:develop"

.PHONY: run lint format test docker-build docker-run

run:
	python -m bot

lint:
	ruff check .

format:
	ruff format .

test:
	python -m pytest tests/unit -q

docker-build:
	docker build -t $(DOCKER_IMG) .

docker-run:
	docker run --rm --env-file .env $(DOCKER_IMG)
