#! /bin/bash

if [ -n "$VIRTUAL_ENV" ]; then
  deactivate
fi
rm -rf venv
virtualenv venv --no-site-packages
source venv/bin/activate
pip install -r requirements.txt
