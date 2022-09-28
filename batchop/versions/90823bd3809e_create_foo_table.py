"""create foo table

Revision ID: 90823bd3809e
Revises: 
Create Date: 2022-09-28 18:44:44.079887

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import table, column


# revision identifiers, used by Alembic.
revision = '90823bd3809e'
down_revision = None
branch_labels = None
depends_on = None

foo_table = table(
    'foo',
    column('foo_id', sa.Integer),
    column('bar', sa.String),
)


def upgrade() -> None:
    # Create table
    op.create_table(
        "foo",
        sa.Column("foo_id", sa.Integer(), nullable=False),
        sa.Column("bar", sa.String(length=512), nullable=False),
        sa.PrimaryKeyConstraint("foo_id"),
    )

    # Insert Dummy Data
    op.bulk_insert(
        foo_table,
        [
            {'bar': 'data 1'},
            {'bar': 'data 2'},
            {'bar': 'data 3'},
        ]
    )


def downgrade() -> None:
    op.drop_table("foo")
