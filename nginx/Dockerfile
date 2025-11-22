FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/mynginx.conf

COPY html/ /usr/share/nginx/html/

EXPOSE 80
