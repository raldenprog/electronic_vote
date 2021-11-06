"""users table

Revision ID: 6968eb20f90f
Revises: 
Create Date: 2021-11-06 23:27:21.786427

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6968eb20f90f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('user_name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id_user')
    )
    op.create_index(op.f('ix_user_user_name'), 'user', ['user_name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_user_name'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###