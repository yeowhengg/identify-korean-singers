FROM python:3.10.0-alpine
WORKDIR /code
COPY ./main/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
WORKDIR /code/main/backend
