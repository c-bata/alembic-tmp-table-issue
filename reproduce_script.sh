#!/bin/bash
set -eux

rm alembic.db || true
alembic upgrade head | true
echo ".tables" | sqlite3 alembic.db
