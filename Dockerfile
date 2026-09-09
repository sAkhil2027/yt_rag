FROM python:3.11-slim

# Prevent Python from buffering logs and disable ChromaDB telemetry
ENV PYTHONUNBUFFERED=1 \
    PORT=7860 \
    ANONYMOUS_TELEMETRY=False

WORKDIR /code

# Create non-root user required by Hugging Face Spaces (UID 1000)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Install dependencies
COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy application files
COPY --chown=user:user . .

# Expose default Hugging Face Spaces port
EXPOSE 7860

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
