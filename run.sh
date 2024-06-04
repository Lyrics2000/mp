#!/usr/bin/env bash
set -e
python manage.py migrate --noinput

#python property_manager.py collectstatic —-noinput
# first remove the collect static folder
rm -rf static
echo yes | python manage.py collectstatic

echo yes | python manage.py makemigrations

echo yes | python manage.py migrate


DJANGO_PROJECT_DIR="."
DJANGO_MANAGE_PY="${DJANGO_PROJECT_DIR}/manage.py"
SUPERUSER_USERNAME="admin"
SUPERUSER_EMAIL="admin@example.com"
SUPERUSER_PASSWORD="1234"

# Check if superuser already exists
existing_superuser=$(${DJANGO_MANAGE_PY} shell -c "from django.contrib.auth.models import User; print(User.objects.filter(username='${SUPERUSER_USERNAME}').exists())")

if [ "${existing_superuser}" == "False" ]; then
    # Create superuser
    ${DJANGO_MANAGE_PY} createsuperuser --noinput --username=${SUPERUSER_USERNAME} --email=${SUPERUSER_EMAIL}
    ${DJANGO_MANAGE_PY} shell -c "from django.contrib.auth.models import User; user=User.objects.get(username='${SUPERUSER_USERNAME}'); user.set_password('${SUPERUSER_PASSWORD}'); user.save()"
    echo "Superuser '${SUPERUSER_USERNAME}' created successfully."
else
    echo "Superuser '${SUPERUSER_USERNAME}' already exists."
fi



# python manage.py runserver 0.0.0.0:8078
exec gunicorn --bind=0.0.0.0:8078 config.wsgi --workers=5 --log-level=info --log-file=---access-logfile=- --error-logfile=- --timeout 30000 --reload