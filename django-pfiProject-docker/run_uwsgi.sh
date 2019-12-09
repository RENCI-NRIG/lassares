#!/usr/bin/env bash

source /code/pfiProject/.env
python manage.py makemigrations
python manage.py showmigrations
python manage.py migrate
#python manage.py createsuperuser --username admin --email komal.thareja@gmail.com --noinput
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'jmpmcmanus@gmail.com', '$ADMIN_PWD')" | python manage.py shell
python manage.py collectstatic --noinput
#create db view
echo -e "SELECT SETVAL('meas_web_mscnt_id_seq', 99);\nUPDATE meas_web_mscnt SET id = DEFAULT;\nCREATE VIEW drf_mscnt AS SELECT id AS id, job_id, bore_id, instrument, chemical_id, measurement_value, units, (date + time)::timestamp AS timestamp, status, comment, geom FROM meas_web_mscnt;\nCREATE VIEW drf_mscnt_timestamp AS SELECT (date + time)::timestamp AS id, (date + time)::timestamp AS label FROM meas_web_mscnt;\nCREATE VIEW drf_mscnt_jobid AS SELECT DISTINCT job_id as id, job_id as label FROM meas_web_mscnt;\nSELECT SETVAL('meas_web_gcmv_id_seq', 99);\nUPDATE meas_web_gcmv SET id = DEFAULT;\nCREATE VIEW drf_gcmv AS SELECT id AS id, job_id, bore_id, instrument, chemical_id, measurement_value, units, (date + time)::timestamp AS timestamp, status, comment, geom FROM meas_web_gcmv;\nCREATE VIEW drf_gcmv_timestamp AS SELECT (date + time)::timestamp AS id, (date + time)::timestamp AS label FROM meas_web_gcmv;\nCREATE VIEW drf_gcmv_jobid AS SELECT DISTINCT job_id as id, job_id as label FROM meas_web_gcmv;"|python manage.py dbshell

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
