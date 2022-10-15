FROM python:3.10

COPY . /app
WORKDIR /app

# EXPOSE 5001

# install poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python
ENV PATH "/etc/poetry/venv/bin/:${PATH}"

# add and install python requirements
# COPY pyproject.toml .
# COPY poetry.lock .
RUN poetry install --no-root

RUN pwd
RUN ls -la

# run server
CMD ["poetry", "run", "python", "src/app.py"]

# ENTRYPOINT exec uvicorn main:app --port 5001 --server-header --log-level debug --app-dir src
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001", "--app-dir", "src"]
# uvicorn main:app --host 0.0.0.0 --port 5001 --app-dir src