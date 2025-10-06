FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-pip iputils-ping net-tools

WORKDIR /app
COPY . /app

EXPOSE 80

CMD ["python3", "server_async.py"]
