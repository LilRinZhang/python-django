FROM python:3.11.4
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir /django_test
WORKDIR /django_test
ADD requirements.txt /django_test
RUN pip install --upgrade pip && pip install -r requirements.txt