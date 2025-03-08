.PHONY: install build run stop logs test clean redis-cli

install:
    apt install firefox xorg

build:
    docker compose build

run:
    docker compose up -d

stop:
    docker compose down

logs:
    docker compose logs -f

test:
    MOZ_HEADLESS=1 python main.py

clean:
    docker compose down --rmi all
    docker system prune -f

restart: stop run logs

redis-cli:
    docker compose exec redis redis-cli

dev:
    MOZ_HEADLESS=1 gunicorn -k uvicorn.workers.UvicornWorker main:app --reload
