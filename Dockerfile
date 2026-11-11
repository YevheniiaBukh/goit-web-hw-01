FROM python:3.13.5-slim

RUN pip install poetry

WORKDIR /app

COPY . .

RUN poetry install

CMD [ "poetry", "run", "python", "main.py"]
