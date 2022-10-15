.DEFAULT_GOAL := clean

say_hello:
	@echo "Hello World"

tree:
	clear
	tree -L 3 -I __pycache__

clean:
	@echo "Clean Up..."
	find . -type f -iname ".DS_Store" -delete
	find . -type d -iname ".pytest_cache" -exec rm -r {} +
	find . -type d -iname "__pycache__" -exec rm -r {} +
	find . -type d -iname "htmlcov" -exec rm -r {} +
	find . -type f -iname ".coverage" -exec rm -r {} +


test:
	@echo "Testing..."
	poetry run pytest -vrP src/tests/

coverage:
	@echo "Making Coverage..."
	poetry run pytest --cov=src
	poetry run coverage html

serve:
	@echo "Starting uvicorn server..."
	poetry run uvicorn main:app --app-dir src

build:
	@echo "Building Docker image..."
	docker build -t ress/smalltalk .

run:
	@echo "Running in Docker..."
	docker run ress/smalltalk

rundaemon:
	@echo "Running in Docker..."
	docker run -d ress/smalltalk

# deploy:
# 	@echo "Deploying to basscadet..."
# 	poetry run python src/deploy.py

lint:
	@echo "Linting..."
	poetry run black --line-length 220 --target-version py310 src/
	# poetry run flake8 src/
