FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ADD . /code
WORKDIR /code
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt