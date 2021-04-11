FROM python:3
ENV PYTHONUNBUFFERED=1

ARG ENVIRONMENT

# dir variables
ENV CODE_DIR="/code"
ENV REQUIREMENTS_DIR="${CODE_DIR}/requirements"
ENV SCRIPTS_DIR="${CODE_DIR}/scripts"

# sh file names variables
ENV REQUIREMENTS_SH_FILE_NAME="setup_requirements.sh"

RUN pip install pip-tools

WORKDIR ${CODE_DIR}
COPY . ${CODE_DIR}

WORKDIR ${SCRIPTS_DIR}
RUN ./${REQUIREMENTS_SH_FILE_NAME}

WORKDIR ${CODE_DIR}
