FROM python:3.9.4-alpine

# set work directory
WORKDIR /usr/src/script

# copy requirements file
COPY ./requirements.txt /usr/src/app/requirements.txt

# RUN mkdir /app && cd app

RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
    libressl-dev libffi-dev gcc musl-dev python3-dev \
    postgresql-dev bash \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /usr/src/app/requirements.txt \
    && rm -rf /root/.cache/pip

# copy project
COPY . /usr/src/script

CMD ["python", "generate_testdata.py"]