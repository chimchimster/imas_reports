FROM python:3.10-slim
WORKDIR /reports/
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
RUN mkdir /reports/modules/apps/word/temp \
    && mkdir /reports/modules/apps/word/merged \
    && mkdir /reports/modules/apps/word/temp_templates \
    && mkdir /reports/modules/apps/word/temp_tables/results \
    && mkdir /reports/modules/apps/word/temp_tables/templates \
    && mkdir /reports/modules/apps/word/highcharts_temp_images

ENTRYPOINT ["sh", "app.sh"]