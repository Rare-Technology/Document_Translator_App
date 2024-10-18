FROM python:3.11-slim

WORKDIR /app/Document_Translator_App

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone the repository
RUN git clone https://github.com/Rare-Technology/Document_Translator_App.git .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Install msal explicitly
RUN pip3 install --no-cache-dir msal

# Make output directory in the container
RUN mkdir -p /app/Document_Translator_App/output_files

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Create a startup script
RUN echo '#!/bin/bash\n\
streamlit run translator.py --server.enableCORS false --server.enableXsrfProtection false --server.baseUrlPath="/"\n\
' > /app/start.sh && chmod +x /app/start.sh

# Use the startup script as the entry point
ENTRYPOINT ["/app/start.sh"]