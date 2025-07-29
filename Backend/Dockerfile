FROM python:3.11

WORKDIR /app

COPY ./app /app/app
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]