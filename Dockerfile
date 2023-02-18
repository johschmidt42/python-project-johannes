FROM python:3.10-slim as base

WORKDIR /app

# ignore 'Running pip as the root user...' warning
ENV PIP_ROOT_USER_ACTION=ignore

# update pip
RUN pip install --upgrade pip

FROM base as builder

# install poetry
ENV POETRY_VERSION=1.3.1
RUN pip install "poetry==$POETRY_VERSION"

# copy application
COPY ["pyproject.toml", "poetry.lock", "README.md", "./"]
COPY ["src/", "src/"]

# build wheel
RUN poetry build --format wheel

FROM base as production

# expose port
EXPOSE 80

# copy the wheel from the build stage
COPY --from=builder /app/dist/*.whl /app/

# install package
RUN pip install /app/*.whl

# install gunicorn (ASGI web implementation)
RUN pip install gunicorn==20.1.0

# copy entrypoint of the app
COPY ["main.py", "./"]

# command to run
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:80", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker"]
