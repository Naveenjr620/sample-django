# Use a fuller base image for fewer install issues
FROM python:3.10

# Environment variables to optimize Python behavior
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        gettext \
        curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files (skip errors if collectstatic fails)
RUN python manage.py collectstatic --noinput || echo "Skipping collectstatic"

# Expose port for Gunicorn
EXPOSE 5000

# Start Gunicorn server
CMD ["gunicorn", "my_site.wsgi:application", "--bind", "0.0.0.0:5000"]
