FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000:5000
COPY . .

CMD ["gunicorn", "--workers=2", "-b 0.0.0.0:5000", "wsgi:app"]