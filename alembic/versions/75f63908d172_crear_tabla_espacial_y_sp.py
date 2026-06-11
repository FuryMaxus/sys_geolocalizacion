from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import advanced_alchemy.types.guid
import geoalchemy2.types

# revision identifiers, used by Alembic.
revision: str = '75f63908d172'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    op.execute('CREATE EXTENSION IF NOT EXISTS postgis;')
    
    op.execute("""
        CREATE OR REPLACE FUNCTION calculate_distance_sp(lat1 FLOAT, lon1 FLOAT, lat2 FLOAT, lon2 FLOAT)
        RETURNS FLOAT AS $$
        BEGIN
            RETURN ST_Distance(
                ST_SetSRID(ST_MakePoint(lon1, lat1), 4326)::geography,
                ST_SetSRID(ST_MakePoint(lon2, lat2), 4326)::geography
            );
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.create_table('pets_locations',
    sa.Column('id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),
    sa.Column('pet_id', sa.Uuid(), nullable=False),
    sa.Column('coordinate', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, dimension=2, from_text='ST_GeomFromEWKT', name='geometry', nullable=False), nullable=False),
    sa.Column('sa_orm_sentinel', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_pets_locations'))
    )   
    op.create_index(op.f('ix_pets_locations_pet_id'), 'pets_locations', ['pet_id'], unique=False)

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP FUNCTION IF EXISTS calculate_distance_sp(FLOAT, FLOAT, FLOAT, FLOAT);")
    op.execute('DROP EXTENSION IF EXISTS postgis;')

    op.drop_index(op.f('ix_pets_locations_pet_id'), table_name='pets_locations')
    op.drop_table('pets_locations')