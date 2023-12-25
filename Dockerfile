FROM python:3.10-slim
WORKDIR reports/
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
VOLUME reports/volumes/:/modules/apps/word/merged
ENTRYPOINT ["sh", "app.sh"]