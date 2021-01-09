FROM python:3.8.1-slim-buster
RUN mkdir code
COPY requirements.txt /code/requirements.txt
WORKDIR /code
RUN pip3 install -r requirements.txt
COPY . /code/
ENV PYTHONUNBUFFERED=1
WORKDIR /code
EXPOSE 5000
CMD python __init__.py