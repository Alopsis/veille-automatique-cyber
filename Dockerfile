FROM python:3.9-slim

# Installez bash pour la gestion de l'environnement virtuel
RUN apt-get update && apt-get install -y bash

# Créez et définissez le répertoire de travail
WORKDIR /app

# Copiez le fichier requirements.txt et le reste des fichiers de l'application
COPY requirements.txt ./
COPY . .

# Exposez le port de l'application
EXPOSE 5000

# Démarrez l'application
CMD ["python", "app.py"]
