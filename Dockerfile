FROM python:3.10-slim
WORKDIR /reports/
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
RUN apt-get update && apt-get install -y cron
COPY . .
#RUN mkdir /reports/modules/apps/word/temp \
#    && mkdir /reports/modules/apps/word/merged \
#    && mkdir /reports/modules/apps/word/temp_templates \
#    && mkdir /reports/modules/apps/word/temp_tables/results \
#    && mkdir /reports/modules/apps/word/temp_tables/templates \
#    && mkdir /reports/modules/apps/word/highcharts_temp_images

RUN echo "0 0 * * * find /reports/modules/apps/word/merged/ -type d -exec rm -rf {} \;" | crontab -

ENTRYPOINT ["sh", "app.sh"]