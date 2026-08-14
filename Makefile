UV ?= uv
DOCKER ?= docker
DOCKER_IMAGE ?= python-tg-bot-template:develop
UV_RUN := $(UV) run --frozen --no-sync
export PYTHONDONTWRITEBYTECODE := 1

.PHONY: sync run format lint type lock lock-check test test-architecture test-unit test-integration rename-smoke check docker-build docker-run

sync:
	$(UV) sync --frozen

run:
	$(UV_RUN) python .

lint:
	$(UV_RUN) ruff check --no-cache .
	$(UV_RUN) ruff format --check --no-cache .
	shellcheck scripts/*.sh

format:
	$(UV_RUN) ruff check --fix .
	$(UV_RUN) ruff format .

type:
	$(UV_RUN) mypy --no-incremental --cache-dir=/dev/null

lock:
	$(UV) lock
	$(UV) export --frozen --no-header --no-dev --no-emit-project --format requirements-txt -o requirements.lock

lock-check:
	./scripts/check-lock.sh

test: test-architecture test-unit test-integration

test-architecture:
	$(UV_RUN) python -m pytest -p no:cacheprovider tests/architecture -q

test-unit:
	$(UV_RUN) python -m pytest -p no:cacheprovider tests/unit -q

test-integration:
	$(UV_RUN) python -m pytest -p no:cacheprovider tests/integration -q

rename-smoke:
	./scripts/verify-template.sh

check: lint type lock-check test rename-smoke

docker-build:
	$(DOCKER) build -t $(DOCKER_IMAGE) .

docker-run:
	$(DOCKER) run --rm --env-file .env $(DOCKER_IMAGE)
