# Use a more reliable base image
FROM python:3.10-slim-buster
 
# Environment variables to optimize Python behavior
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
 
# Set working directory
WORKDIR /app
 
# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gettext \
    curl \
&& rm -rf /var/lib/apt/lists/*
 
# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
&& pip install --no-cache-dir -r requirements.txt
 
# Copy the rest of the project
COPY . .
 
# Run collectstatic (you can remove if you're not using static files)
RUN python manage.py collectstatic --noinput || true
 
# Expose port for Gunicorn/Django
EXPOSE 5000
 
# Start the Gunicorn server
CMD ["gunicorn", "my_site.wsgi:application", "--bind", "0.0.0.0:5000"]
