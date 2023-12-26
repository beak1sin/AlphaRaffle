#!/bin/sh
. /root/.virtualenvs/AlphaRaffle_env/bin/activate
echo "############# virtualenvs ON #############"
python /usr/local/share/docker-server/AlphaRaffle/manage.py makemigrations
echo "############# makemigrations OK #############"
python /usr/local/share/docker-server/AlphaRaffle/manage.py migrate
echo "############# migrate OK #############"
python /usr/local/share/docker-server/AlphaRaffle/manage.py collectstatic --noinput
echo "############# collectstatic OK #############"
# killall -9 uwsgi
# echo "############# KILL OK #############"
# uwsgi --ini /usr/local/share/AlphaRaffle/AlphaRaffle_uwsgi.ini &
# echo "############# START OK (BackGround) ############"
deactivate
echo "############# virtualenvs OFF #############"
#tail -111f /usr/local/share/AlphaRaffle/logs/uwsgi.log
