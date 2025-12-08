.PHONY: up demo

up:
	docker-compose build
	docker-compose up -d

demo:
	@echo ">>> Running main pipeline"
	docker-compose run --rm app python -m src.app
	@echo ">>> Verifying logs"
	docker-compose run --rm app python -m src.verify_logs
	@echo ">>> Running evaluation scenarios"
	docker-compose run --rm app python -m src.evaluate
