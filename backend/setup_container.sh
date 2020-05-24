#!/usr/bin/env bash

apt-get update && apt-get install -y \
    python3-pip postgresql-client postgresql-contrib

pip install --upgrade pip
pip install -r requirements/base.txt
pip install -r requirements/development.txt
chmod +x /app/runserver.sh