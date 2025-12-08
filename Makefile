up:
	docker-compose build
	docker-compose up -d

demo:
	# 1) run main pipeline (uses env from compose)
	docker-compose run --rm app python -m src.app
	# 2) verify logs
	docker-compose run --rm app python -m src.verify_logs
	# 3) run evaluation scenarios
	docker-compose run --rm app python -m src.evaluate
