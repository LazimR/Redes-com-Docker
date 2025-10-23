FROM ubuntu:latest


RUN apt-get update && apt-get install -y python3 python3-pip iputils-ping net-tools

WORKDIR /app
COPY . /app

RUN chmod +x /app/start.sh
EXPOSE 80 3000

CMD ["./start.sh"]
