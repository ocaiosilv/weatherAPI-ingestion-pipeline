# pyodbc image idea source: https://github.com/laudio/pyodbc
FROM python:3.13-slim-bookworm AS main

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


RUN apt-get update && \
  apt-get install -y curl build-essential unixodbc-dev g++ apt-transport-https && \
  curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft-prod.gpg && \
  curl -sSL https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list && \
  apt-get update && \
  # Install ODBC Driver for SQL Server
  ACCEPT_EULA='Y' apt-get install -y msodbcsql18 && \
  # Cleanup build dependencies
  rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./
# put the .env when running the container.
RUN uv sync --locked

COPY src/ ./src/

WORKDIR /app/src/weatherapi_ingestion_pipeline

CMD ["uv", "run", "python","-m", "pipeline.main"]