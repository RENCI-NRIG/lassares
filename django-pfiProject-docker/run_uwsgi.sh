#!/usr/bin/env bash

source /code/pfiProject/.env
python manage.py makemigrations
python manage.py showmigrations
python manage.py migrate
#python manage.py createsuperuser --username admin --email komal.thareja@gmail.com --noinput
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'komal.thareja@gmail.com', '$ADMIN_PWD')" | python manage.py shell
python manage.py collectstatic --noinput
#create db view
echo -e "SELECT SETVAL('meas_web_measurement_id_seq', 99);\nUPDATE meas_web_measurement SET id = DEFAULT;\nCREATE VIEW drf_measurement AS SELECT id AS fid, bore_id, job_id, device_id, chemical_id, concentration, (date + time)::timestamp AS timestamp, status, comment, geom FROM meas_web_measurement;\nCREATE VIEW drf_timestamp AS SELECT (date + time)::timestamp AS id, (date + time)::timestamp AS label FROM meas_web_measurement;\nCREATE VIEW drf_jobid AS SELECT DISTINCT job_id as id, job_id as label FROM meas_web_measurement;" | python manage.py dbshell

if [[ "${USE_DOT_VENV}" -eq 1 ]]; then
    if [[ "${RUN_ROOT}" -eq 1 ]]; then
        uwsgi --virtualenv ./.venv --ini pfiProject_uwsgi.ini
    else
        uwsgi --uid ${UWSGI_UID-1000} --gid ${UWSGI_GID:-1000}  --virtualenv ./.venv --ini pfiProject_uwsgi.ini
    fi
else
    if [[ "${RUN_ROOT}" -eq 1 ]]; then
        uwsgi --virtualenv ./venv --ini pfiProject_uwsgi.ini
    else
        uwsgi --uid ${UWSGI_UID:-1000} --gid ${UWSGI_GID:-1000}  --virtualenv ./venv --ini pfiProject_uwsgi.ini
    fi
fi
