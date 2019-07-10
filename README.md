# Social Team Builder (Docker)

The [Social Team Builder](https://github.com/crhowell/social-team-builder) project rebuilt for Docker.

> **NOTE**: This repo was created primarily for:
> 1. Practicing with Docker Compose
> 2. Experiments using NGINX to load balance (round-robin) between 2 Django app instances
>

### To run

1. Clone this repo.
2. `docker-compose up --build` 

> Building the docker images using the docker-compose command will attempt to run 4 separate containers.

### Containers created

1. NGINX
2. Django App Instance 1 with Gunicorn
3. Django App Instance 2 with Gunicorn
4. Postgres Database

**NGINX**
* Handles media and static file requests.
* Acting as a proxy server, forwards all non-media/non-static file requests over to gunicorn for Django to process.

**Django App Instances + Gunicorn**
Running identical application instances in separate containers with Gunicorn + 3 workers.

**Postgres**
Django app instances are connected to the same postgres database container.