FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        docker.io \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/local/lib/docker/cli-plugins \
    && curl -fsSL "https://github.com/docker/compose/releases/download/v2.29.2/docker-compose-linux-x86_64" \
        -o /usr/local/lib/docker/cli-plugins/docker-compose \
    && chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

COPY web_app/ /app/web_app/
COPY python_app/teste_prompt_e2e_semantico/ /app/python_app/teste_prompt_e2e_semantico/
COPY python_app/avaliacao_prompts/ /app/python_app/avaliacao_prompts/

RUN pip install \
    -r /app/web_app/requirements.txt \
    -r /app/python_app/teste_prompt_e2e_semantico/requirements.txt \
    -r /app/python_app/avaliacao_prompts/requirements.txt

WORKDIR /app/web_app

EXPOSE 8000

CMD ["uvicorn", "web_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
