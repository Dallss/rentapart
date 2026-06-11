FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=rentapart.settings

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

CMD ["sh", "-c", "\
python manage.py migrate && \
python manage.py seed_listings && \
python manage.py seed_mandaue_listings && \
python manage.py seed_lapu_lapu_listings && \
python manage.py seed_landlord && \
python manage.py backfill_city_place_ids && \
gunicorn rentapart.wsgi:application --bind 0.0.0.0:$PORT"]