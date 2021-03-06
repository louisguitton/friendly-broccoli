"""user added username

Revision ID: 0369d1ab987d
Revises: 0a4de562ee04
Create Date: 2018-06-25 22:16:31.375767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0369d1ab987d'
down_revision = '0a4de562ee04'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('username', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.drop_index('ix_user_name', table_name='user')
    op.create_index(op.f('ix_user_name'), 'user', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_name'), table_name='user')
    op.create_index('ix_user_name', 'user', ['name'], unique=1)
    op.drop_index(op.f('ix_user_username'), table_name='user')
    with op.batch_alter_table('user') as bop:
        bop.drop_column('username')
    # ### end Alembic commands ###
