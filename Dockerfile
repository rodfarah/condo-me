# ======================
#  STAGE 1: Builder
# ======================
FROM python:3.10-buster AS builder

# Upgrade pip to the latest version and install Poetry
RUN python -m pip install --upgrade pip \
    && pip install poetry==1.8.4

# Set environment variables for Poetry and app directory configuration
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    APP_HOME=/app

# Define the working directory inside the container
WORKDIR $APP_HOME

# Copy project dependency configuration files into the container
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry with caching enabled for faster builds
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root


# ======================
#  STAGE 2: Runtime
# ======================
FROM python:3.10-slim-buster AS runtime

# Upgrade pip and install required system utilities
RUN python -m pip install --upgrade pip \
    && apt-get update && apt-get install -y netcat

# Install Poetry for runtime dependency management
RUN pip install poetry==1.8.4 

# Configure environment variables for the runtime environment
ENV USER=django_user \
    GROUP=django_user \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    APP_HOME=/app

# Set the working directory inside the container
WORKDIR $APP_HOME

# Arguments for custom UID and GID for user permissions
ARG UID=1000
ARG GID=1000

# Create a group and user to align host and container permissions
RUN groupadd -g ${GID} ${GROUP} \
    && useradd -u ${UID} -g ${GID} -m -s /bin/bash ${USER} \
    && mkdir -p $APP_HOME && chown -R ${USER}:${GROUP} $APP_HOME

# Copy the virtual environment from the builder stage
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Copy the application code and scripts into the container
COPY . . 

# Ensure correct ownership of the virtual environment for the application user
RUN chown -R django_user:django_user ${VIRTUAL_ENV}

# Expose the application port for the service
EXPOSE 8000

# Make the commands.sh script executable
RUN chmod +x $APP_HOME/docker-scripts/commands.sh

# Switch to the custom application user
USER ${USER}

# Set the default command to execute the commands.sh script
CMD ["/app/docker-scripts/commands.sh"]
