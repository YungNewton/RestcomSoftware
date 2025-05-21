#!/bin/bash

if [ "$1" = "celery" ]; then
  echo "Starting Celery..."
  celery -A restcom_backend worker --loglevel=info
else
  echo "Starting Django app..."
  gunicorn restcom_backend.wsgi:application --bind 0.0.0.0:8000
fi