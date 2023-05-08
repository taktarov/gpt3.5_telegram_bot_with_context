FROM python:3.11-slim-buster
WORKDIR /travelradarbot
COPY requirements.txt /travelradarbot/
RUN pip install -r requirements.txt
COPY . /travelradarbot
CMD python app.py