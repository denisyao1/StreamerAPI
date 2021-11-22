#!/bin/sh
python -m flask db upgrade
python api.py
