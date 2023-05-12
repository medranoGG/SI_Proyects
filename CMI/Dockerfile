FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP run.py
ENV DEBUG True

COPY requirements.txt .

# install python dependencies
RUN apt-get update && \
    apt-get install -y wkhtmltopdf

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pandas
RUN pip install db-sqlite3
RUN pip install matplotlib
RUN pip install pdfkit
#RUN pip install graphviz

COPY env.sample .env

COPY . .

RUN flask db init
RUN flask db migrate
RUN flask db upgrade
RUN flask gen_api

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "--timeout", "120", "run:app"]
