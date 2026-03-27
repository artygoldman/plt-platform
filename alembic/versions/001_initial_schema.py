"""Initial schema creation for Personal Longevity Team platform.

Revision ID: 001
Revises:
Create Date: 2026-03-27 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema."""

    # Enable required extensions
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.execute('CREATE EXTENSION IF NOT EXISTS "timescaledb"')
    op.execute('CREATE EXTENSION IF NOT EXISTS "vector"')

    # Create agents table
    op.create_table(
        'agents',
        sa.Column('id', sa.String(50), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('tier', sa.Integer(), nullable=False),
        sa.Column('specialty', sa.String(255), nullable=True),
        sa.Column('system_prompt', sa.Text(), nullable=False),
        sa.Column('model', sa.String(100), nullable=False, server_default='claude-sonnet-4-6'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('config', postgresql.JSON(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.func.gen_random_uuid()),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('date_of_birth', sa.Date(), nullable=False),
        sa.Column('sex', sa.String(20), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('subscription_tier', sa.String(50), nullable=False, server_default='premium'),
        sa.Column('timezone', sa.String(100), nullable=False, server_default='UTC'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=False)

    # Create user_profiles table
    op.create_table(
        'user_profiles',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.func.gen_random_uuid()),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('height_cm', sa.Numeric(precision=5, scale=1), nullable=True),
        sa.Column('weight_kg', sa.Numeric(precision=5, scale=1), nullable=True),
        sa.Column('blood_type', sa.String(10), nullable=True),
        sa.Column('allergies', postgresql.JSON(astext_type=sa.Text()), nullable=False, server_default='[]'),
        sa.Column('medications', postgresql.JSON(astext_type=sa.Text()), nullable=False, server_default='[]'),
        sa.Column('contraindications', postgresql.JSON(astext_type=sa.Text()), nullable=False, server_default='[]'),
        sa.Column('genetic_risks', postgresql.JSON(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.Column('goals', postgresql.JSON(astext_type=sa.Text()), nullable=False, server_default='[]'),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index('ix_user_profiles_user_id', 'user_profiles', ['user_id'], unique=False)

    # Create biomarkers table
    op.create_table(
        'biomarkers',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.func.gen_random_uuid()),
        sa.Column('time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('source', sa.String(50), nullable=False),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('marker_name', sa.String(100), nullable=False),
        sa.Column('value', sa.Numeric(precision=12, scale=4), nullable=False),
        sa.Column('unit', sa.String(30), nullable=False),
        sa.Column('reference_low', sa.Numeric(precision=12, scale=4), nullable=True),
        sa.Column('reference_high', sa.Numeric(precision=12, scale=4), nullable=True),
        sa.Column('optimal_low', sa.Numeric(precision=12, scale=4), nullable=True),
        sa.Column('optimal_high', sa.Numeric(precision=12, scale=4), nullable=True),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_biomarkers_time', 'biomarkers', ['time'], unique=False)
    op.create_index('ix_biomarkers_user_id', 'biomarkers', ['user_id'], unique=False)
    op.create_index('idx_biomarkers_user_marker', 'biomarkers', ['user_id', 'marker_name'], unique=False)
    op.create_index('idx_biomarkers_user_time', 'biomarkers', ['user_id', 'time'], unique=False)

    # Convert biomarkers to TimescaleDB hypertable
    op.execute("""
        SELECT create_hypertable('biomarkers', 'time', if_not_exists => TRUE)
    """)

    # Create digital_twin table
    op.create_table(
        'digital_twin',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.func.gen_random_uuid()),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('biological_age', sa.Numeric(precision=5, scale=1), nullable=True),
        sa.Column('chronological_age', sa.Numeric(precision=5, scale=1), nullable=True),
        sa.Column('dunedin_pace', sa.Numeric(precision=4, scale=2), nullable=True),
        sa.Column('longevity_score', sa.Integer(), nullable=True),
        sa.Column('healthspan_forecast_years', sa.Numeric(precision=5, scale=1), nullable=True),
        sa.Column('mortality_risk_score', sa.Numeric(precision=5, scale=3), nullable=True),
        sa.Column('systems_status', postgresql.JSON(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.Column('last_updated', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index('ix_digital_twin_user_id', 'digital_twin', ['user_id'], unique=False)

    # Create agent_sessions table
    op.create_table(
        'agent_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.func.gen_random_uuid()),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('trigger_type', sa.String(50), nullable=False),
        sa.Column('trigger_data', postgresql.JSON(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.Column('status', sa.String(20), nullable=False, server_default='running'),
        sa.Column('langgraph_thread_id', sa.String(255), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('total_tokens', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('total_cost_usd', sa.Numeric(precision=8, scale=4), nullable=False, server_default='0'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_agent_sessions_user_id', 'agent_sessions', ['user_id'], unique=False)

    # Create agent_decisions table
    op.create_table(
        'agent_decisions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.func.gen_random_uuid()),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('agent_id', sa.String(50), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('input_data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('output_data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('confidence', sa.Integer(), nullable=True),
        sa.Column('was_vetoed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('veto_reason', sa.Text(), nullable=True),
        sa.Column('vetoed_by', sa.String(50), nullable=True),
        sa.Column('approved_by', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('tokens_used', sa.Integer(), nullable=True),
        sa.Column('latency_ms', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['agent_id'], ['agents.id']),
        sa.ForeignKeyConstraint(['session_id'], ['agent_sessions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_agent_decisions_session_id', 'agent_decisions', ['session_id'], unique=False)
    op.create_index('ix_agent_decisions_agent_id', 'agent_decisions', ['agent_id'], unique=False)
    op.create_index('ix_agent_decisions_user_id', 'agent_decisions', ['user_id'], unique=False)

    # Create protocols table
    op.create_table(
        'protocols',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.func.gen_random_uuid()),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('status', sa.String(20), nullable=False, server_default='draft'),
        sa.Column('nutrition_plan', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('supplement_plan', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('fitness_plan', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('sleep_protocol', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('environment', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('medical_actions', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('valid_from', sa.Date(), nullable=True),
        sa.Column('valid_until', sa.Date(), nullable=True),
        sa.Column('approved_by', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['session_id'], ['agent_sessions.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_protocols_user_id', 'protocols', ['user_id'], unique=False)
    op.create_index('ix_protocols_session_id', 'protocols', ['session_id'], unique=False)

    # Create daily_contracts table
    op.create_table(
        'daily_contracts',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.func.gen_random_uuid()),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('protocol_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('contracts', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('completion_rate', sa.Numeric(precision=3, scale=2), nullable=False, server_default='0'),
        sa.Column('longevity_delta', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['protocol_id'], ['protocols.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_daily_contracts_user_id', 'daily_contracts', ['user_id'], unique=False)
    op.create_index('ix_daily_contracts_protocol_id', 'daily_contracts', ['protocol_id'], unique=False)
    op.create_index('ix_daily_contracts_date', 'daily_contracts', ['date'], unique=False)

    # Create user_files table
    op.create_table(
        'user_files',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.func.gen_random_uuid()),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('file_type', sa.String(50), nullable=False),
        sa.Column('original_name', sa.String(500), nullable=True),
        sa.Column('s3_key', sa.String(500), nullable=False),
        sa.Column('mime_type', sa.String(100), nullable=True),
        sa.Column('size_bytes', sa.BigInteger(), nullable=True),
        sa.Column('extracted_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('processed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_files_user_id', 'user_files', ['user_id'], unique=False)

    # Create supplement_inventory table
    op.create_table(
        'supplement_inventory',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.func.gen_random_uuid()),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('brand', sa.String(255), nullable=True),
        sa.Column('dosage_per_unit', sa.String(100), nullable=True),
        sa.Column('units_remaining', sa.Integer(), nullable=True),
        sa.Column('expiry_date', sa.Date(), nullable=True),
        sa.Column('auto_reorder', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_supplement_inventory_user_id', 'supplement_inventory', ['user_id'], unique=False)

    # Create knowledge_chunks table
    op.create_table(
        'knowledge_chunks',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.func.gen_random_uuid()),
        sa.Column('source', sa.String(100), nullable=False),
        sa.Column('source_id', sa.String(255), nullable=True),
        sa.Column('title', sa.Text(), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('category', sa.String(100), nullable=True),
        sa.Column('embedding', Vector(dim=1536), nullable=True),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_knowledge_chunks_source', 'knowledge_chunks', ['source'], unique=False)
    op.create_index('ix_knowledge_chunks_source_id', 'knowledge_chunks', ['source_id'], unique=False)
    op.create_index('ix_knowledge_chunks_category', 'knowledge_chunks', ['category'], unique=False)

    # Create IVFFlat index on embedding (for pgvector similarity search)
    op.execute("""
        CREATE INDEX idx_knowledge_chunks_embedding_ivfflat
        ON knowledge_chunks USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100)
    """)


def downgrade() -> None:
    """Downgrade database schema."""

    # Drop tables in reverse order (respecting foreign key constraints)
    op.drop_table('knowledge_chunks')
    op.drop_table('supplement_inventory')
    op.drop_table('user_files')
    op.drop_table('daily_contracts')
    op.drop_table('protocols')
    op.drop_table('agent_decisions')
    op.drop_table('agent_sessions')
    op.drop_table('digital_twin')
    op.drop_table('biomarkers')
    op.drop_table('user_profiles')
    op.drop_table('users')
    op.drop_table('agents')
