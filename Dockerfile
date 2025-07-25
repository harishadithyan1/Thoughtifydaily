# Use official Python base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files (optional, only if using Django static)
RUN python manage.py collectstatic --noinput

# Expose the port Gunicorn will run on
EXPOSE 8000

# Run Gunicorn
CMD ["gunicorn", "blog.wsgi:application", "--bind", "0.0.0.0:8000"]
