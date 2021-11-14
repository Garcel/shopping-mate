FROM python:3.10.0-alpine3.14
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

# Add a new user non root user
RUN useradd docker_user

# Change to non-root privilege
USER docker_user

COPY . /code/
