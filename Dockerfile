FROM python:3.10-buster AS builder


# Update pip
RUN python -m pip install --upgrade pip \
    && pip install poetry==1.8.4

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    APP_HOME=/app

WORKDIR $APP_HOME

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root


FROM python:3.10-slim-buster AS runtime

RUN python -m pip install --upgrade pip \
    && apt-get update && apt-get install -y netcat

RUN pip install poetry==1.8.4 

ENV USER=django_user \
    GROUP=django_user \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    APP_HOME=/app

WORKDIR $APP_HOME

# Custom UID and GID are used to align host and container permissions
ARG UID=1000
ARG GID=1000

# Create group and user according to customized UID and GID
RUN groupadd -g ${GID} ${GROUP} \
    && useradd -u ${UID} -g ${GID} -m -s /bin/bash ${USER} \
    && mkdir -p $APP_HOME && chown -R ${USER}:${GROUP} $APP_HOME

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY . . 

RUN chown -R django_user:django_user ${VIRTUAL_ENV}

# Exposing the app port
EXPOSE 8000

# Making the "commands.sh" script executable
RUN chmod +x $APP_HOME/docker-scripts/commands.sh

USER ${USER}

CMD ["/app/docker-scripts/commands.sh"]
