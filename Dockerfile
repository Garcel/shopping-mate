FROM python:3.10
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Add a new user non root user
RUN useradd docker_user

# Change to non-root privilege
USER docker_user

COPY . /code/
