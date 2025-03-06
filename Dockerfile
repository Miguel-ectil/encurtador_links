# Etapa 1: Definindo a imagem base
FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
