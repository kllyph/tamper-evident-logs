#makes sure your WSL environment has the developer tools

bootstrap:
	@echo "Bootstrapping project..."
	@sudo apt update && sudo apt install -y build-essential docker-compose
	@echo "Environment ready."



