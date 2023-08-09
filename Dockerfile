FROM python:3.10-slim
WORKDIR report_exp/
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . word-creator
CMD ["python3", "word-creator/app.py"]