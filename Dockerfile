FROM python:3.11

# On installe les certificats et les outils pour que le réseau sorte bien
RUN apt-get update && apt-get install -y \
    build-essential \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Mise à jour de pip
RUN pip install --no-cache-dir --upgrade pip

# Copie des fichiers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# IMPORTANT : On dit à Hugging Face qu'on utilise le port standard
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_SERVER_PORT=7860
EXPOSE 7860

# On s'assure que les logs s'affichent en temps réel
ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]