FROM python:3.14-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt -i https://mirror-pypi.runflare.com/simple
COPY  ./core .