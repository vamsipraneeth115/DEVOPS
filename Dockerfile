# Multi-stage Docker build for disease prediction application

# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application files
COPY app.py .
COPY train.py .
COPY requirements.txt .
COPY data ./data

# Create data directory
RUN mkdir -p data

# Train the model during build so the runtime image is self-contained.
RUN python train.py

# Set PATH to use local pip packages
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8502
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8502/_stcore/health || exit 1

# Expose port
EXPOSE 8502

# Default command runs the Streamlit app
CMD ["streamlit", "run", "app.py"]
