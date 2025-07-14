FROM python:3.13-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root

COPY . .

CMD ["poetry", "run", "pytest"]