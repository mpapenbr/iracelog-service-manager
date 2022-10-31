"""compute pit lane length

Revision ID: e8ef1f454564
Revises: c4e9b7f26c5d
Create Date: 2022-10-31 10:53:52.298031

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e8ef1f454564'
down_revision = 'c4e9b7f26c5d'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
update track set data=data || jsonb_set(data, '{pit}', data->'pit'||jsonb_build_object('lane', 
case 
when data->'pit'->'exit' > data->'pit'->'entry' then ((data->'pit'->'exit')::decimal - (data->'pit'->'entry')::decimal)*(data->'trackLength')::decimal
else (1-(data->'pit'->'entry')::decimal + (data->'pit'->'exit')::decimal)*(data->'trackLength')::decimal
end
))
where (data->'pit'->'entry')::numeric != 0 and (data->'pit'->'exit')::numeric != 0

    """)
    pass


def downgrade():
    pass
