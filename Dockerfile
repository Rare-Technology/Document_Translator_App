FROM python:3.11-slim

WORKDIR /app/Document_Translator_App

RUN apt-get update && apt-get install -y \
    pip install msal \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/Rare-Technology/Document_Translator_App.git .

RUN pip3 install -r requirements.txt

# make output directory in the container
RUN mkdir -p /app/Document_Translator_App/output_files

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "translator.py"]