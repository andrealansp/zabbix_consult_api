FROM python:3.13.5-slim
LABEL authors="a.alves"
WORKDIR /app
RUN apt-get update && apt-get install -y curl
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8001"]

EXPOSE 8001