FROM python:3.10.0-alpine3.15
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY src src
EXPOSE 9000
HEALTHCHECK --interval=30s --timeout=30s --start-period=30s --retries=5 \
    CMD curl -f http://localhost/health || exit 1
ENTRYPOINT ["python3", "./src/app.py"]