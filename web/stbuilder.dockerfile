FROM python:3.7
LABEL maintainer="Chris H"

ENV PYTHONUNBUFFERED 1

COPY ./web /var/www/stbuilder

WORKDIR /var/www/stbuilder/

RUN pip install -r requirements.txt
RUN pip install gunicorn

EXPOSE 8081

ENTRYPOINT ["./entrypoint.sh"]
