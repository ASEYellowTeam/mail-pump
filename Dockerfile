FROM python:3.6
MAINTAINER Yellow Team ytbeepbeep@gmail.com
ADD ./ ./
RUN pip install -r requirements.txt
CMD celery worker -A mailpump.mailpump -B
