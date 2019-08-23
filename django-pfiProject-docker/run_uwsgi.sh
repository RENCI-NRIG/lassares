#!/usr/bin/env bash

source /code/pfiProject/.env
python manage.py makemigrations
python manage.py showmigrations
python manage.py migrate
#python manage.py createsuperuser --username admin --email komal.thareja@gmail.com --noinput
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'komal.thareja@gmail.com', '$ADMIN_PWD')" | python manage.py shell
python manage.py collectstatic --noinput
#create db view
echo -e "CREATE VIEW drf_data_testdatav_model AS SELECT fid AS id, device_id, timestamp, job_id, chem_id FROM drf_data_testdata_model;\nCREATE VIEW drf_data_timestamp_model AS SELECT timestamp as id, timestamp as label FROM drf_data_testdata_model;\nCREATE VIEW drf_data_jobid_model AS SELECT DISTINCT job_id as id, job_id as label FROM drf_data_testdata_model;" | python manage.py dbshell

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
