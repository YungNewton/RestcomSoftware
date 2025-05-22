# Base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev curl \
    && apt-get clean

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Make sure start.sh is executable
RUN chmod +x /app/start.sh

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the Django port
EXPOSE 8000

# Run the app using your custom script
CMD ["/app/start.sh"]