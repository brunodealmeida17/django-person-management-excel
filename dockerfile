FROM python:3.10-slim

WORKDIR /app
COPY ./requirements.txt /app/
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*/ \
    && apt-get install -y curl

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY ./src /app

COPY ./.env /app
COPY ./entrypoint.sh /app

ENTRYPOINT ["sh", "./entrypoint.sh"]


   