"""empty message

Revision ID: 02979a3f9480
Revises: 6a29055eb9a0
Create Date: 2016-03-01 17:30:52.044074

"""

# revision identifiers, used by Alembic.
revision = '02979a3f9480'
down_revision = '6a29055eb9a0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('my_profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=80), nullable=True),
    sa.Column('last_name', sa.String(length=80), nullable=True),
    sa.Column('nickname', sa.String(length=80), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nickname')
    )
    op.create_index(u'ix_my_profile_email', 'my_profile', ['email'], unique=True)
    op.drop_table(u'myprofile')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table(u'myprofile',
    sa.Column(u'id', sa.INTEGER(), nullable=False),
    sa.Column(u'first_name', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.Column(u'last_name', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.Column(u'nickname', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.Column(u'email', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint(u'id', name=u'myprofile_pkey')
    )
    op.drop_index(u'ix_my_profile_email', table_name='my_profile')
    op.drop_table('my_profile')
    ### end Alembic commands ###
