FROM python:3.8

WORKDIR /app

ADD . /app/

EXPOSE 8000

COPY ./requirements/development.txt /app

RUN pip install -r ./requirements/development.txt --no-cache-dir

COPY . /app

ENTRYPOINT ["python3"]

CMD ["manage.py", "runserver", "0.0.0.0:8000"]
