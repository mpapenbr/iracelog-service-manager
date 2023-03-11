"""prepare for go migration

Revision ID: 5bae79740add
Revises: e8ef1f454564
Create Date: 2023-03-11 17:30:38.035943

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '5bae79740add'
down_revision = 'e8ef1f454564'
branch_labels = None
depends_on = None


def upgrade():
    # preparations for the go-replacment: simulate an already executed go migration
    op.create_table('schema_migrations',
                    sa.Column('version', sa.Integer(), nullable=False),
                    sa.Column('dirty', sa.Boolean(), nullable=False),
                    sa.PrimaryKeyConstraint('version')
                    )
    op.execute("insert into schema_migrations (version,dirty) values (1,false)")


def downgrade():
    op.drop_table('schema_migrations')
