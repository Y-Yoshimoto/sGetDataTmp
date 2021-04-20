# build
FROM python:3.8
# https://hub.docker.com/r/library/python
LABEL  maintainer "y.yoshimoto"
# pip
COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt && pip freeze > requirements.lock
RUN mkdir /code
COPY ./code/* /code/
WORKDIR /code
#CMD [ "flask", "run", "--host=0.0.0.0"]
CMD [ "flask", "run", "--host=0.0.0.0", "--debugger", "--reload"]
#CMD [ "tail", "-f", "/dev/null"]