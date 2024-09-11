#!/bin/bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
