FROM python:3.11

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy and install requirements
COPY requirements/prod.txt .
RUN uv pip install --system --no-cache -r prod.txt

# Copy application
COPY . .

ENV PYTHONPATH=/app

EXPOSE 8000

CMD python manage.py migrate && \
    uvicorn settings.asgi:application --host 0.0.0.0 --port 8000