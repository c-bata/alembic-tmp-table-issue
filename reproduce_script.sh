#!/bin/bash
set -eux

rm alembic.db || true

alembic upgrade 90823bd3809e

alembic upgrade head | true

echo ".tables" | sqlite3 alembic.db

