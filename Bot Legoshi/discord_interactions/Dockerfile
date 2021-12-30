FROM python:3.8-slim AS base
RUN apt-get update && apt-get install --no-install-recommends --yes python3

RUN pip install mysql.connector
RUN pip install pika
RUN pip install requests
RUN pip install discord

ENV PYTHONUNBUFFERED 1

ARG DATABASE_IP
ENV DATABASE_IP $DATABASE_IP

COPY ./create_gif_database.py ./create_gif_database.py
COPY ./gif_Interaction.py ./gif_Interaction.py



CMD ["python", "gif_Interaction.py"]