#!/bin/bash
cd /var/www/vhosts/aleliz.xyz/flask.aleliz.xyz
pipenv run gunicorn -w 4 --forwarded-allow-ips="127.0.0.1" --proxy-allow-from="127.0.0.1" run:app