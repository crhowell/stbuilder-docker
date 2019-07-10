FROM nginx:latest

MAINTAINER Chris H

VOLUME /var/cache/nginx

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./web/static /var/www/public/stbuilder/static
COPY ./web/media /var/www/public/stbuilder/media

EXPOSE 8080

ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]
