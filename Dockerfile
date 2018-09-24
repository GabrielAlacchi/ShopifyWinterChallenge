FROM python:3.5

ADD requirements.txt /app/
WORKDIR /app/

RUN pip install -r requirements.txt

ADD . /app/

RUN python manage.py migrate
RUN python manage.py loaddata shop_api/fixtures/*.json

CMD python manage.py runserver 0.0.0.0:80
