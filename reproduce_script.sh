#!/bin/bash
set -eux

rm alembic.db || true

alembic upgrade 90823bd3809e
echo ".tables" | sqlite3 alembic.db
echo ".schema foo" | sqlite3 alembic.db

alembic upgrade head | true
echo ".tables" | sqlite3 alembic.db
echo ".schema foo" | sqlite3 alembic.db
echo "select * from foo;" | sqlite3 alembic.db

