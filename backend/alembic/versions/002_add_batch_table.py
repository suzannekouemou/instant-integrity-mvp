"""Add batch table and update sample/result

Revision ID: 002
Revises: 001
Create Date: 2025-11-24

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    # Create batches table
    op.create_table(
        'batches',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('total_samples', sa.Integer(), nullable=False),
        sa.Column('processed_count', sa.Integer(), server_default='0'),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('NOW()')),
        sa.CheckConstraint("status IN ('pending', 'processing', 'complete', 'failed')", name='ck_batch_status')
    )
    
    op.create_index('idx_batches_user_id', 'batches', ['user_id'])
    op.create_index('idx_batches_status', 'batches', ['status'])
    
    # Add batch_id to samples
    op.add_column('samples', sa.Column('batch_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('batches.id', ondelete='SET NULL'), nullable=True))
    op.create_index('idx_samples_batch_id', 'samples', ['batch_id'])
    
    # Add new columns to results
    op.add_column('results', sa.Column('preprocessing_params', postgresql.JSONB(), nullable=True))
    op.add_column('results', sa.Column('pca_variance_explained', sa.Float(), nullable=True))

def downgrade():
    op.drop_column('results', 'pca_variance_explained')
    op.drop_column('results', 'preprocessing_params')
    op.drop_index('idx_samples_batch_id', 'samples')
    op.drop_column('samples', 'batch_id')
    op.drop_index('idx_batches_status', 'batches')
    op.drop_index('idx_batches_user_id', 'batches')
    op.drop_table('batches')
