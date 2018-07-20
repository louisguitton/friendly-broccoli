"""user model with auth0

Revision ID: 2e7fda0c949e
Revises: 66b5da6e431d
Create Date: 2018-07-16 15:19:57.103076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e7fda0c949e'
down_revision = '66b5da6e431d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('auth0_id', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_user_auth0_id'), 'user', ['auth0_id'], unique=True)
    op.add_column('user', sa.Column('headline', sa.Text(), nullable=True))
    op.add_column('user', sa.Column('industry', sa.Text(), nullable=True))
    op.add_column('user', sa.Column('summary', sa.Text(), nullable=True))


    op.add_column('user', sa.Column('created_at', sa.DateTime(), nullable=True))

    op.drop_index(op.f('ix_user_linkedin_handle'), table_name='user')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    with op.batch_alter_table('user') as bop:
        bop.alter_column('username', new_column_name='nickname')
        bop.alter_column('linkedin_handle', new_column_name='linkedin_url')
        bop.alter_column('last_seen', new_column_name='last_login')
        bop.drop_column('password_hash')
        bop.add_column(sa.Column('picture', sa.Text(), nullable=True))
    op.create_index(op.f('ix_user_linkedin_url'), 'user', ['linkedin_url'], unique=True)
    op.create_index(op.f('ix_user_nickname'), 'user', ['nickname'], unique=True)



def downgrade():
    op.drop_index(op.f('ix_user_linkedin_url'), table_name='user')
    op.drop_index(op.f('ix_user_nickname'), table_name='user')
    op.drop_index(op.f('ix_user_auth0_id'), table_name='user')
    with op.batch_alter_table('user') as bop:
        bop.drop_column('auth0_id')
        bop.drop_column( 'headline')
        bop.drop_column( 'industry')
        bop.drop_column( 'summary')
        bop.drop_column( 'created_at')
        bop.alter_column( 'nickname', new_column_name='username')
        bop.alter_column( 'linkedin_url', new_column_name='linkedin_handle')
        bop.alter_column( 'last_login', new_column_name='last_seen')
        bop.drop_column('picture')
        bop.add_column(sa.Column('password_hash', sa.String(length=128), nullable=True))
    op.create_index(op.f('ix_user_linkedin_handle'), 'user', ['linkedin_handle'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)

