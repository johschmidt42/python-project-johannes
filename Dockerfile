FROM python:3.10-slim

WORKDIR /app

# install poetry
ENV POETRY_VERSION=1.2.0
RUN pip install "poetry==$POETRY_VERSION"

# install gunicorn (ASGI web implementation)
RUN pip install gunicorn==20.1.0

# copy application
COPY ["pyproject.toml", "poetry.lock", "README.md", "main.py", "./"]
COPY ["src/", "src/"]

# build wheel
RUN poetry build --format wheel

# install package
RUN pip install dist/*.whl

# expose port
EXPOSE 80

# command to run
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:80", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker"]
