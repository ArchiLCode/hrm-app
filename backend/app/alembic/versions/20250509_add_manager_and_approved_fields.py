"""
add manager_id to Department and approved_by_manager_id to LeaveRequest

Revision ID: 20250509addmngrandapprflds
Revises: 20250508addhrtablesuserfields
Create Date: 2025-05-09 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20250509addmngrandapprflds'
down_revision = '20250508addhrtablesuserfields'
branch_labels = None
depends_on = None

def upgrade():
    # Добавить manager_id в department
    op.add_column('department', sa.Column('manager_id', postgresql.UUID(as_uuid=True), nullable=False))
    op.create_foreign_key('fk_department_manager_id_user', 'department', 'user', ['manager_id'], ['id'])

    # Добавить approved_by_manager_id в leaverequest
    op.add_column('leaverequest', sa.Column('approved_by_manager_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key('fk_leaverequest_approved_by_manager_id_user', 'leaverequest', 'user', ['approved_by_manager_id'], ['id'])

def downgrade():
    op.drop_constraint('fk_leaverequest_approved_by_manager_id_user', 'leaverequest', type_='foreignkey')
    op.drop_column('leaverequest', 'approved_by_manager_id')
    op.drop_constraint('fk_department_manager_id_user', 'department', type_='foreignkey')
    op.drop_column('department', 'manager_id')
