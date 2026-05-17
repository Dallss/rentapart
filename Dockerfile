FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN DJANGO_SETTINGS_MODULE=rentapart.settings SECRET_KEY=dummy python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "rentapart.wsgi:application", "--bind", "0.0.0.0:8000"]