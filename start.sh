#!/bin/bash
export FLASK_APP=api.py:app
export FLASK_ENV=development
python3 -m flask run --host=0.0.0.0
