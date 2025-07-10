# Define the default target
.DEFAULT_GOAL := run

# Define the FastAPI app module and command
APP_MODULE := app.main:app
UVICORN_COMMAND := uvicorn $(APP_MODULE) --reload --use-colors

# Run the FastAPI app using uvicorn
run:
	@$(UVICORN_COMMAND)

install:
	@pip install -r requirements.txt
	@pip install -r tests-requirements.txt

uninstall:
	@pip freeze | xargs pip uninstall -y

test:
	@pytest tests

format:
	@ruff format .
	@ruff check . --fix
	@mypy . --exclude "^(tests|venv)" --config-file "pyproject.toml"