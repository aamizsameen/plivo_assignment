FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt


EXPOSE 5000

ENV FLASK_ENV=production

CMD ["python", "app5.py"]
