FROM python:3.12


ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.8.0


RUN apt-get update && apt-get install -y \
    curl \
    libpq-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app


COPY pyproject.toml ./


COPY src/ /app/src/


RUN poetry install --no-dev


ENV SERVER_ADDRESS=0.0.0.0:8080


EXPOSE 8080

CMD ["poetry", "run", "uvicorn", "src.__main__:app", "--host", "0.0.0.0", "--port", "8080"]
