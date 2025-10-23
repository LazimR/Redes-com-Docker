FROM ubuntu:latest

RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip iputils-ping net-tools && apt-get clean

WORKDIR /app
COPY . /app

EXPOSE 80

CMD ["python3", "server_async.py"]
