FROM python:3.10

LABEL maintainer="diego@capyba.com"

ARG requirements_file="requirements/production.txt"

ENV PYTHONUNBUFFERED 1

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements /app/requirements

WORKDIR /app

RUN pip install --upgrade pip && pip install -r $requirements_file

COPY . /app

# Build operations
RUN STAGE=build ENVKEY_DISABLE_AUTOLOAD=1 python manage.py collectstatic --noinput

# Determines whether the process running is active, running and healthy.
HEALTHCHECK CMD ["curl", "--fail", "http://localhost:8000", "||", "exit 1"]

EXPOSE 80

CMD ["uwsgi", "--http=0.0.0.0:80", "--module=conf.wsgi"]
