FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY pyproject.toml /app/pyproject.toml
COPY teste_prompt_e2e_semantico /app/teste_prompt_e2e_semantico

ENTRYPOINT ["python", "-m", "teste_prompt_e2e_semantico"]
