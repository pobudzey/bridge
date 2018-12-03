"""images

Revision ID: da8894903541
Revises: 148b64848a9a
Create Date: 2018-11-29 14:56:04.724820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da8894903541'
down_revision = '148b64848a9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('image_filename', sa.String(), nullable=True))
    op.add_column('post', sa.Column('image_url', sa.String(), nullable=True))
    op.create_foreign_key(None, 'post', 'group', ['group_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_column('post', 'image_url')
    op.drop_column('post', 'image_filename')
    # ### end Alembic commands ###