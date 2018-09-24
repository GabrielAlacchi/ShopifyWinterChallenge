FROM python:3.5

ADD requirements.txt /app/
WORKDIR /app/

RUN pip install -r requirements.txt

ADD . /app/

CMD gunicorn shopify_challenge.wsgi
