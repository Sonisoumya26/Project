FROM python:3.11-slim

# Set environment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /chat2

# Install system dependencies
RUN apt-get update && apt-get install -y gcc

# Install Python dependencies
COPY DjangoTest1/chatbot/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY DjangoTest1/chatbot /chat2

# Collect static files on build (optional)
RUN python manage.py collectstatic --noinput || true

CMD ["gunicorn", "chatbot.wsgi:application", "--bind", "0.0.0.0:8000"]
