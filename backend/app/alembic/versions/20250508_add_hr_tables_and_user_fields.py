"""add role, employee to user; add Department, Employee, TimeSheet, LeaveRequest tables

Revision ID: 20250508addhrtablesuserfields
Revises: 1a31ce608336
Create Date: 2025-05-08 12:30:00.000000
"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
import uuid

# revision identifiers, used by Alembic.
revision = '20250508addhrtablesuserfields'
down_revision = '1a31ce608336'
branch_labels = None
depends_on = None

def upgrade():
    # Добавить поле role в user
    op.add_column('user', sa.Column('role', sa.String(length=50), nullable=True))

    # Таблица department
    op.create_table(
        'department',
        sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('name', sa.String(length=100), nullable=False, unique=True, index=True),
        sa.Column('description', sa.String(length=255)),
    )

    # Таблица employee
    op.create_table(
        'employee',
        sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('user.id'), unique=True, nullable=False),
        sa.Column('department_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('department.id'), nullable=False),
        sa.Column('position', sa.String(length=100), nullable=False),
        sa.Column('hire_date', sa.Date(), nullable=False),
        sa.Column('phone', sa.String(length=20)),
        sa.Column('salary', sa.Float()),
        sa.Column('is_active', sa.Boolean(), default=True),
    )

    # Таблица timesheet
    op.create_table(
        'timesheet',
        sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('employee_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('employee.id'), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('check_in', sa.DateTime()),
        sa.Column('check_out', sa.DateTime()),
    )

    # Таблица leaverequest
    op.create_table(
        'leaverequest',
        sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('employee_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('employee.id'), nullable=False),
        sa.Column('leave_type', sa.String(length=20), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, default='pending'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

def downgrade():
    op.drop_table('leaverequest')
    op.drop_table('timesheet')
    op.drop_table('employee')
    op.drop_table('department')
    op.drop_column('user', 'role')
