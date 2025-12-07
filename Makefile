.PHONY: up demo test down clean

up:
	docker-compose up -d --build

demo:
	docker-compose run --rm app python -m src.app

test:
	docker-compose exec app pytest -q --disable-warnings --maxfail=1

down:
	docker-compose down

clean:
	rm -rf data/output/*
