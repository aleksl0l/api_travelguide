"""init

Revision ID: 1c93bbc64457
Revises: 
Create Date: 2018-09-01 14:09:39.243378

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1c93bbc64457'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'role',
        sa.Column('id_role', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(10), nullable=False)
    )
    op.create_table(
        'country',
        sa.Column('id_country', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(40), unique=True),
    )
    op.create_table(
        'towns',
        sa.Column('id_town', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(40), unique=True),
        sa.Column('description', sa.Text()),
        sa.Column('url_photo', sa.Text()),
        sa.Column('id_country', sa.Integer),
        sa.ForeignKeyConstraint(('id_country',), ['country.id_country'], ),
    )
    op.create_table(
        'users',
        sa.Column('id_user', sa.Integer, primary_key=True),
        sa.Column('public_id', sa.String(36)),
        sa.Column('name', sa.String(50)),
        sa.Column('password', sa.String(100)),
        sa.Column('id_role', sa.Integer),
        sa.ForeignKeyConstraint(('id_role',), ['role.id_role'], ),
    )
    op.create_table(
        'sights',
        sa.Column('id_sight', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('tag', sa.ARRAY(sa.Text())),
        sa.Column('cost', sa.REAL),
        sa.Column('id_town', sa.Integer),
        sa.ForeignKeyConstraint(('id_town',), ['towns.id_town'], ),
        sa.Column('cord_lat', sa.Integer),
        sa.Column('cord_long', sa.Integer),
        sa.Column('rating', sa.REAL),
        sa.Column('type_sight', sa.Text),
        sa.Column('urls', sa.ARRAY(sa.Text)),
        sa.Column('web_site', sa.Text),
        sa.Column('description', sa.Text),
        sa.Column('history', sa.Text),
        sa.Column('phone_number', sa.String(20))
    )
    op.create_table(
        'likes',
        sa.Column('id_like', sa.Integer, primary_key=True),

        sa.Column('id_user', sa.Integer),
        sa.ForeignKeyConstraint(('id_user',), ['users.id_user'], ),

        sa.Column('id_sight', sa.Integer),
        sa.ForeignKeyConstraint(('id_sight',), ['sights.id_sight'], ),
        sa.Column('value', sa.Integer),
    )
    op.create_unique_constraint("likes__uc_id_user_id_sight", "likes", ["id_user", "id_sight"])


def downgrade():
    op.drop_table('role')
    op.drop_table('country')
    op.drop_table('towns')
    op.drop_table('sights')
    op.drop_table('likes')