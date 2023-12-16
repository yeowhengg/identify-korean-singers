FROM python:3.10.0-alpine
WORKDIR /code
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
