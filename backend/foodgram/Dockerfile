FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram.wsgi"] 
CMD ["sh", "-c", "\
    python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    gunicorn --bind 0.0.0.0:8000 foodgram.wsgi"]