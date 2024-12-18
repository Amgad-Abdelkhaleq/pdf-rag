# Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose ports for FastAPI and Streamlit
EXPOSE 8000 8501

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run both FastAPI and Streamlit
CMD ["sh", "-c", "python main.py & streamlit run src/ui/streamlit_app.py"]