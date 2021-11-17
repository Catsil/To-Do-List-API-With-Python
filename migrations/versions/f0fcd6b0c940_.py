"""empty message

Revision ID: f0fcd6b0c940
Revises: 991a94b1e5b7
Create Date: 2021-11-15 10:13:52.736834

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f0fcd6b0c940'
down_revision = '991a94b1e5b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item', sa.String(length=250), nullable=False),
    sa.Column('done', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('label', mysql.VARCHAR(length=250), nullable=False),
    sa.Column('done', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False),
    sa.Column('_is_active', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False),
    sa.CheckConstraint('(`_is_active` in (0,1))', name='user_chk_2'),
    sa.CheckConstraint('(`done` in (0,1))', name='user_chk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('task')
    # ### end Alembic commands ###