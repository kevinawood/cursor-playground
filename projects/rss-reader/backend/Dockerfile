FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Install system dependencies (alpine uses apk)
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    curl \
    && rm -rf /var/cache/apk/*

# Set Python environment variables for memory optimization
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONHASHSEED=random
ENV PYTHONOPTIMIZE=1

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with optimizations
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN adduser -D -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5001

# Health check - use simple /health endpoint for faster response
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5001/health || exit 1

# Run the application with Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "1", "--threads", "2", "--timeout", "30", "--max-requests", "100", "--max-requests-jitter", "10", "wsgi:app"] 