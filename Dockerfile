FROM python:3.10.4-alpine
ENV PYTHONUNBUFFERED=1
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
WORKDIR /usr/src/britam/payments/app
COPY requirements.txt ./
RUN pip install -r requirements.txt

# COPY . ./

# RUN chmod +x ./docker-entrypoint.sh

COPY . .
# These line for /entrypoint.sh
COPY docker-entrypoint.sh ./

RUN chmod +x ./docker-entrypoint.sh
# # Run the application
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
