FROM python:3.10-slim

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

ENV PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

WORKDIR /app

COPY . /app

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["python", "manage.py", "runserver", "8000"]