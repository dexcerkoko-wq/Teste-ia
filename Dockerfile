FROM python:3.11-slim

RUN dpkg --add-architecture i386 && \
    apt-get update && apt-get install -y \
    wine \
    wine32 \
    wine64 \
    wget \
    cabextract \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

ENV WINEPREFIX=/root/.wine
ENV WINEDEBUG=-all
ENV DISPLAY=:0

RUN wineboot --init

RUN pip install flask pyinstaller
RUN pip install mcp[cli] flask pyinstaller

WORKDIR /app
COPY app.py .

CMD ["python", "app.py"]
