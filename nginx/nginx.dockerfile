FROM nginx:latest

MAINTAINER Chris H

VOLUME /var/cache/nginx

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

EXPOSE 8080

ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]
