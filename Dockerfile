FROM ubuntu
FROM python:3.11

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -U pip
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app
EXPOSE 3000
CMD python ./index.py

ENTRYPOINT [ "python" ]

CMD ["main.py"]