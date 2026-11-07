FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    NLTK_DATA=/usr/share/nltk_data \
    DJANGO_DB_PATH=/app/var/db.sqlite3

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY nlp/__init__.py nlp/resources.py nlp/
RUN python -c "from nlp.resources import ensure_nltk_data; ensure_nltk_data('$NLTK_DATA')"

COPY . .

RUN DJANGO_SECRET_KEY=build-only python manage.py train_topic_model \
 && DJANGO_SECRET_KEY=build-only python manage.py collectstatic --noinput \
 && useradd --create-home --uid 1000 app \
 && mkdir -p /app/var \
 && chown -R app:app /app/var

USER app
EXPOSE 8000

ENTRYPOINT ["sh", "docker-entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120", "--access-logfile", "-"]
