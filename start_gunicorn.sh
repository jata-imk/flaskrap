#!/bin/bash
chmod +x /var/www/vhosts/aleliz.xyz/flask.aleliz.xyz/start_gunicorn.sh
cd /var/www/vhosts/aleliz.xyz/flask.aleliz.xyz
python3.10 -m pipenv run shell
echo 'Iniciando servidor de gunicorn'
pipenv run gunicorn -w 4 --forwarded-allow-ips="127.0.0.1" --proxy-allow-from="127.0.0.1" run:app