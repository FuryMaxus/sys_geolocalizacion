"""add_radius_search_sp

Revision ID: f4bc8b039a3f
Revises: 75f63908d172
Create Date: 2026-06-10 20:31:17.177774

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4bc8b039a3f'
down_revision: Union[str, Sequence[str], None] = '75f63908d172'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        CREATE OR REPLACE FUNCTION get_pets_in_radius_sp(lat FLOAT, lon FLOAT, radius_meters FLOAT)
        RETURNS TABLE (pet_id UUID, distance FLOAT) AS $$
        BEGIN
            RETURN QUERY
            SELECT 
                pl.pet_id,
                ST_Distance(
                    pl.coordinate::geography, 
                    ST_SetSRID(ST_MakePoint(lon, lat), 4326)::geography
                ) AS distance
            FROM pets_locations pl
            WHERE ST_DWithin(
                pl.coordinate::geography, 
                ST_SetSRID(ST_MakePoint(lon, lat), 4326)::geography, 
                radius_meters
            )
            ORDER BY distance ASC;
        END;
        $$ LANGUAGE plpgsql;
    """)

def downgrade():
    op.execute("DROP FUNCTION IF EXISTS get_pets_in_radius_sp(FLOAT, FLOAT, FLOAT);")
