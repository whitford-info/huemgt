FROM python:3.10

WORKDIR /hbridge
COPY . .
RUN pip install -q -r requirements.txt
RUN pip install .
WORKDIR /app
COPY ./app .


CMD ["python", "main.py"]