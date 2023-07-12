FROM python:3.8

WORKDIR /app

ADD . /app/

EXPOSE 3000

COPY .env /app

COPY ./requirements/development.txt /app

RUN pip install -r ./requirements/development.txt --no-cache-dir

COPY . /app

RUN python manage.py migrate

RUN python manage.py createsuperuser

RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('jembi_admin', 'camerooniol@jembi.org', 'password123')" | python manage.py shell



ENTRYPOINT ["python3"]

CMD ["manage.py", "runserver", "0.0.0.0:3000"]
