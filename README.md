# shopping-mate
[![CircleCI](https://circleci.com/gh/circleci/circleci-docs.svg?style=shield)](https://circleci.com/gh/circleci/circleci-docs)
[![codecov](https://codecov.io/gh/Garcel/shopping-mate/branch/master/graph/badge.svg?token=2J24VWKURW)](https://codecov.io/gh/Garcel/shopping-mate)

Shopping list assistant app backend

## Overview :male_detective:
Shopping-mate is an application to help you to create, manage and share shopping lists.

## Prerequisites :rotating_light:
This project requires a database whose connection url must be passed as an environment variable.

## Environment variables 📋
Some variables are expected to exist into the environment. In my development environment I'm using and `.env` file 
with these properties:
```properties
DATABASE_URL=<schema>://<user>:<pass>@<host>:<port>/<db_name>
SECRET_KEY=
```

## Running the application 🚀
```bash
docker-compose up
```

## Author :writing_hand:
José Antonio Garcel (garcel.developer@gmail.com)

April 11 2021
