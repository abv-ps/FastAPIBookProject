#!/bin/bash
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 7000 --reload
