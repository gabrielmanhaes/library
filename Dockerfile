
####### Builder #######

FROM python:3.13-slim AS builder

ARG PACKAGE_NAME

WORKDIR /build

RUN pip install --upgrade pip && pip install poetry && poetry self add poetry-plugin-export

COPY pyproject.toml README.md ./
COPY src/$PACKAGE_NAME ./src/$PACKAGE_NAME

RUN sed -i "/packages = \[/,/]/c\packages = [\n    { include = \"$PACKAGE_NAME\", from = \"src\" },\n]" pyproject.toml

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN poetry build

# ----------------------
# Librarian
# ----------------------

FROM python:3.13-slim AS librarian

WORKDIR /app

COPY --from=builder /build/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=builder /build/dist/*.whl ./
RUN pip install --no-cache-dir *.whl

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV CONTAINER=true

CMD ["uvicorn", "librarian.app:app", "--host", "0.0.0.0", "--port", "80"]

# ----------------------
# Archiver
# ----------------------

FROM python:3.13-slim AS archiver

WORKDIR /app

COPY --from=builder /build/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=builder /build/dist/*.whl ./
RUN pip install --no-cache-dir *.whl

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV CONTAINER=true

CMD ["uvicorn", "archiver.app:app", "--host", "0.0.0.0", "--port", "80"]

# ----------------------
# Worker
# ----------------------

# TODO - Uncomment and build the worker properly

# FROM archiver AS worker

# CMD ["celery", "-A", "src.archiver.worker.app", "worker", "--loglevel=info", "--concurrency=4"]
