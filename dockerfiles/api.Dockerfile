FROM python:3.9.5-buster

LABEL maintainer="ohseok158@gmail.com"

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV TZ Asia/Seoul
ENV PYTHONPATH /wantedlab_backend

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && date

COPY requirements.txt /wantedlab_backend/requirements.txt
RUN pip3 install -r /wantedlab_backend/requirements.txt

COPY sources /wantedlab_backend/sources
ENV PYTHONUNBUFFERED=TRUE
WORKDIR /wantedlab_backend

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "sources.app:app"]