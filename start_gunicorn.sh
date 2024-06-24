#!/bin/bash
cd /var/www/vhosts/aleliz.xyz/flask.aleliz.xyz
pipenv run gunicorn run:app