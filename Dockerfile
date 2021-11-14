FROM python:3.10.0-alpine3.14
ARG UID=1000
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

# Add a new user non root user
RUN adduser docker_user -u ${UID} --disabled-password

# Change to non-root privilege
USER docker_user

COPY . /code/
