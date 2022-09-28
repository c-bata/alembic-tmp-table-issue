# alembic-tmp-table-issue

## Step to reproduce

Setup

```
$ python3.9 -m venv venv
$ source venv/bin/activate
$ pip install alembic sqlalchemy
```

Create `foo` table

```
$ alembic upgrade 90823bd3809e
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 90823bd3809e, create foo table
```

Run a schema migration and a data migration like the following:

```
def upgrade() -> None:
    # Schema Migration
    with op.batch_alter_table("foo") as batch_op:
        batch_op.alter_column(
            "bar",
            nullable=True,
        )

    # Data Migration
    raise Exception("An exception is raised during data migration")
```

The script raises `Exception(...)` deliberately after quit from the `batch_alter_table("foo")` context manager.
So the `alembic upgrade head` will be failed like the following:

```
$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 90823bd3809e -> 8e32f2af1bd2, Add schema & data migration
Traceback (most recent call last):
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/bin/alembic", line 8, in <module>
    sys.exit(main())
  ...
  File "/Users/c-bata/sandbox/alembic-sandbox/batchop/versions/8e32f2af1bd2_add_schema_data_migration.py", line 35, in upgrade
    raise Exception("An exception is raised during data migration")
Exception: An exception is raised during data migration
```

This is expected behavior. However, it cannot re-execute this script since there is `_alembic_tmp_foo` table, which is n temporary table for the batch migration.

```
$ sqlite3 alembic.db
SQLite version 3.37.0 2021-12-09 01:34:53
Enter ".help" for usage hints.
sqlite> .tables
_alembic_tmp_foo  alembic_version   foo
```

```
$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 90823bd3809e -> 8e32f2af1bd2, Add schema & data migration
Traceback (most recent call last):
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 1900, in _execute_context
    self.dialect.do_execute(
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/lib/python3.10/site-packages/sqlalchemy/engine/default.py", line 736, in do_execute
    cursor.execute(statement, parameters)
sqlite3.OperationalError: table _alembic_tmp_foo already exists

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/bin/alembic", line 8, in <module>
    sys.exit(main())
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/lib/python3.10/site-packages/alembic/config.py", line 590, in main
    CommandLine(prog=prog).main(argv=argv)
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/lib/python3.10/site-packages/alembic/config.py", line 584, in main
    self.run_cmd(cfg, options)
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/lib/python3.10/site-packages/alembic/config.py", line 561, in run_cmd
    fn(
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/lib/python3.10/site-packages/alembic/command.py", line 322, in upgrade
    script.run_env()
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/lib/python3.10/site-packages/alembic/script/base.py", line 569, in run_env
    util.load_python_file(self.dir, "env.py")
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/lib/python3.10/site-packages/alembic/util/pyfiles.py", line 94, in load_python_file
    module = load_module_py(module_id, path)
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/lib/python3.10/site-packages/alembic/util/pyfiles.py", line 110, in load_module_py
    spec.loader.exec_module(module)  # type: ignore
  File "<frozen importlib._bootstrap_external>", line 883, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/Users/c-bata/sandbox/alembic-sandbox/batchop/env.py", line 79, in <module>
    run_migrations_online()
  File "/Users/c-bata/sandbox/alembic-sandbox/batchop/env.py", line 73, in run_migrations_online
    context.run_migrations()
  File "<string>", line 8, in run_migrations
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/lib/python3.10/site-packages/alembic/runtime/environment.py", line 853, in run_migrations
    self.get_context().run_migrations(**kw)
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/lib/python3.10/site-packages/alembic/runtime/migration.py", line 623, in run_migrations
    step.migration_fn(**kw)
  File "/Users/c-bata/sandbox/alembic-sandbox/batchop/versions/8e32f2af1bd2_add_schema_data_migration.py", line 28, in upgrade
    with op.batch_alter_table("foo") as batch_op:
  File "/Users/c-bata/.pyenv_x64/versions/3.10.4/lib/python3.10/contextlib.py", line 142, in __exit__
    next(self.gen)
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/lib/python3.10/site-packages/alembic/operations/base.py", line 381, in batch_alter_table
    impl.flush()
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/lib/python3.10/site-packages/alembic/operations/batch.py", line 159, in flush
    batch_impl._create(self.impl)
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/lib/python3.10/site-packages/alembic/operations/batch.py", line 448, in _create
    op_impl.create_table(self.new_table)
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/lib/python3.10/site-packages/alembic/ddl/impl.py", line 354, in create_table
    self._exec(schema.CreateTable(table))
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/lib/python3.10/site-packages/alembic/ddl/impl.py", line 195, in _exec
    return conn.execute(construct, multiparams)
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 1380, in execute
    return meth(self, multiparams, params, _EMPTY_EXECUTION_OPTS)
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/lib/python3.10/site-packages/sqlalchemy/sql/ddl.py", line 80, in _execute_on_connection
    return connection._execute_ddl(
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 1472, in _execute_ddl
    ret = self._execute_context(
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 1943, in _execute_context
    self._handle_dbapi_exception(
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 2124, in _handle_dbapi_exception
    util.raise_(
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/lib/python3.10/site-packages/sqlalchemy/util/compat.py", line 208, in raise_
    raise exception
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 1900, in _execute_context
    self.dialect.do_execute(
  File "/Users/c-bata/sandbox/alembic-sandbox/venv/lib/python3.10/site-packages/sqlalchemy/engine/default.py", line 736, in do_execute
    cursor.execute(statement, parameters)
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) table _alembic_tmp_foo already exists
[SQL:
CREATE TABLE _alembic_tmp_foo (
	foo_id INTEGER NOT NULL,
	bar VARCHAR(512),
	PRIMARY KEY (foo_id)
)

]
(Background on this error at: https://sqlalche.me/e/14/e3q8)
```
