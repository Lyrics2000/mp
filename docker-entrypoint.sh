# Collect static files
echo "Collect static files"
python ./manage.py collectstatic --noinput


# Apply database migrations
echo "Apply database migrations"
python ./manage.py makemigrations --noinput


# Apply database migrations
echo "Apply database migrations"
python ./manage.py migrate --noinput

# Start server
echo "Starting server"
python ./manage.py runserver 0.0.0.0:8190
# gunicorn -b 0.0.0.0 -p 8000 config.asgi:application




echo "Starting celery beat and worker"


# bash --rcfile <(echo '. ~/.bashrc; celery -A config worker --beat  django --loglevel=info')