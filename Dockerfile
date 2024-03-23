FROM python:3.11.4
WORKDIR /app
COPY . .
RUN pip install psycopg2
ENTRYPOINT cd app && python server.py