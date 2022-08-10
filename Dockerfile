FROM python:3.9-slim-buster

COPY ["pyproject.toml", "poetry.lock", "./"]

LABEL org.opencontainers.image.description DESCRIPTION

RUN apt-get update && \
    apt-get install -y git gcc neofetch && \
    python3 -m pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi 

COPY . .

WORKDIR /

RUN ls

CMD ["python3 -m bot"]