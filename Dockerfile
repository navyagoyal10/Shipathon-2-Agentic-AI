# Use a more stable Python base
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (CRITICAL for pptx/docx)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker caching
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Command to run the app
ENTRYPOINT ["streamlit", "run", "ps2.py", "--server.port=8501", "--server.address=0.0.0.0"]