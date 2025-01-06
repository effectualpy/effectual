FROM ghcr.io/astral-sh/uv:python3.11-alpine

WORKDIR /effectual
COPY . .

RUN uv venv --python 3.11
RUN uv lock
RUN uv sync

CMD ["uv", "build"]