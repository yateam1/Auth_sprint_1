"""empty message

Revision ID: e9edb5f3952a
Revises: 20140a07e2d7
Create Date: 2021-08-29 19:02:57.844707

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e9edb5f3952a'
down_revision = '20140a07e2d7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('social',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('provider', sa.String(length=50), nullable=False),
    sa.Column('token', sa.JSON(), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.drop_column('sessions', 'expired')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sessions', sa.Column('expired', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_table('social')
    # ### end Alembic commands ###