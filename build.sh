#!/usr/bin/env bash
set -o errexit

export PYTHON_VERSION=3.11.7

pip install --upgrade pip
pip install -r requirements.txt
