"""create users table

Revision ID: 8692a4dc38af
Revises: 
Create Date: 2026-10-05 15:44:09.831498

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '8692a4dc38af'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id BIGSERIAL PRIMARY KEY,

            name VARCHAR(150) NOT NULL,

            email VARCHAR(255) NOT NULL,

            password_hash TEXT NOT NULL,

            role VARCHAR(20) NOT NULL,

            is_active BOOLEAN NOT NULL DEFAULT TRUE,

            failed_login_attempts INTEGER NOT NULL DEFAULT 0,

            locked_until TIMESTAMPTZ NULL,

            last_login_at TIMESTAMPTZ NULL,

            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

            CONSTRAINT users_email_key
                UNIQUE (email),

            CONSTRAINT users_role_check
                CHECK (
                    role IN (
                        'owner',
                        'management',
                        'administrator',
                        'teacher',
                        'student'
                    )
                )
        );
        """
    )


def downgrade():
    op.execute(
        """
        DROP TABLE IF EXISTS users;
        """
    )