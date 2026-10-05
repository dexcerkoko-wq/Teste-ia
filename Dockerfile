FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wine \
    wine64 \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe -q && \
    wine python-3.11.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 && \
    rm python-3.11.0-amd64.exe

RUN wine pip install pyinstaller

RUN pip install flask

WORKDIR /app
COPY app.py .

CMD ["python", "app.py"]
