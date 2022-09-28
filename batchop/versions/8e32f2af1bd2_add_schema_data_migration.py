"""Add schema & data migration

Revision ID: 8e32f2af1bd2
Revises: 90823bd3809e
Create Date: 2022-09-28 18:53:34.158951

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = '8e32f2af1bd2'
down_revision = '90823bd3809e'
branch_labels = None
depends_on = None

foo_table = table(
    'foo',
    column('foo_id', sa.Integer),
    column('bar', sa.String),
)


def upgrade() -> None:
    # Workaround for the problem
    # bind = op.get_bind()
    # inspector = sa.inspect(bind)
    # if "_alembic_tmp_foo" in inspector.get_table_names():
    #     op.drop_table("_alembic_tmp_trial_values")

    # Schema Migration
    with op.batch_alter_table("foo") as batch_op:
        batch_op.alter_column(
            "bar",
            nullable=True,
        )

    # Write a data migration here like the following pattern.
    # https://alembic.sqlalchemy.org/en/latest/cookbook.html#conditional-migration-elements
    ...
    raise Exception("An exception is raised during the data migration")


def downgrade() -> None:
    pass
