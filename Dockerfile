# Using an official Python image as the base
FROM python:3.10-slim

# Defining variables for app path and user/group
ENV APP_HOME=/app
ENV TEMP_STATIC="/app/temp_static"
ENV USER=django_user
ENV GROUP=django_user
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

# Custom UID and GID are used to align host and container permissions
ARG UID=1000
ARG GID=1000

# Installing system dependencies for Poetry and PostgreSQL (if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install poetry via curl (may take a while...)
RUN echo "Installing Poetry via curl, this may take a while..." \
    && sleep 2 \
    && curl -sSL https://install.python-poetry.org | python3 - --version 1.8.4

# Setting the working directory for the app
WORKDIR $APP_HOME

# Create group and user according to customized UID and GID
RUN groupadd -g ${GID} ${GROUP} && useradd -u ${UID} -g ${GID} -m -s /bin/bash ${USER}

# Create temp_static folder and set permissions to USER
RUN mkdir -p ${TEMP_STATIC} \
    && chown ${USER}:${USER} ${TEMP_STATIC}

# Copying the entire project before installing dependencies
COPY . $APP_HOME

# Making the "commands.sh" script executable
RUN chmod +x $APP_HOME/docker-scripts/commands.sh

# Installing dependencies with Poetry, without creating a virtual environment
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi || true

# Setting the non-root user for container (commands.sh) execution
USER $USER

# Exposing the app port
EXPOSE 8000

# Command to start the script that will execute setup commands and start the server
CMD ["/app/docker-scripts/commands.sh"]
