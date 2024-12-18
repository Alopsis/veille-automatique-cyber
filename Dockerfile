FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt ./
COPY . .
EXPOSE 5000
CMD ["python", "script.py"]
