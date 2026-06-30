FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy project files (README.md is required by pyproject's `readme = "README.md"`)
COPY pyproject.toml README.md ./
COPY backend/ ./backend/

# Install Python dependencies using uv.
# Pull PyTorch from the CPU-only index so we don't download ~5GB of CUDA/NVIDIA
# wheels (this NER service runs on CPU). torch resolves from the pytorch index;
# everything else falls through to PyPI.
RUN cd /app && uv pip install --system \
    --index-url https://download.pytorch.org/whl/cpu \
    --extra-index-url https://pypi.org/simple \
    -e .

# Set working directory to backend
WORKDIR /app/backend

# Expose port
EXPOSE 8000

# Health check (urllib is stdlib; `requests` is not a dependency)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
