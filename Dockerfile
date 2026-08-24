FROM python:3.14-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY . .

ARG BOT_TOKEN
ARG ADMIN_USER_NAME
ARG PORT

ENV BOT_TOKEN=${BOT_TOKEN}
ENV ADMIN_USER_NAME=${ADMIN_USER_NAME}
ENV PORT=${PORT}

EXPOSE 8000

CMD ["uv", "run", "python", "app.py"]