FROM python:3.9
WORKDIR /code
COPY requirements.txt /code
RUN pip3 install -r requirements.txt
COPY . /code
CMD python manage.py makemigrations && python manage.py migrate
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000