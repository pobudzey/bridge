"""images uploading

Revision ID: 2809f500ab18
Revises: b66113129c02
Create Date: 2018-11-24 13:54:03.304680

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2809f500ab18'
down_revision = 'b66113129c02'
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
