"""empty message

Revision ID: 826edc851eb0
Revises: 238b4ca6541f
Create Date: 2018-11-10 11:01:44.205914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '826edc851eb0'
down_revision = '238b4ca6541f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'dislikes')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('dislikes', sa.INTEGER(), nullable=True))
    # ### end Alembic commands ###
