# Social Team Builder (Docker)

The [Social Team Builder](https://github.com/crhowell/social-team-builder) project rebuilt for Docker.

> **NOTE**: This repo was created primarily for experiments on my local NAS box.

### To run

1. Clone this repo.
2. `docker-compose up --build` 

> **NOTE** (Mac): If you get an ERROR containing `OCI runtime create failed:` against the `entrypoint.sh` file.
> you will need to `cd` into the `web` directory and `chmod +x entrypoint.sh` to make it executable.

Building the docker images using the docker-compose command will attempt to run 4 separate containers.

### Containers created

1. NGINX
2. Django App Instance 1 with Gunicorn
3. Django App Instance 2 with Gunicorn
4. Postgres Database

**NGINX**

* Load balancing (round-robin) between two app instances.
* Handles media and static file requests.
* Acting as a proxy server, forwards all non-media/non-static file requests over to gunicorn for Django to process.

**Django App Instances + Gunicorn**

Running identical application instances in separate containers with Gunicorn + 3 workers.

**Postgres**

Django app instances are connected to the same postgres database container.