
DDL_CREAR_SP_DISTANCE = """
CREATE OR REPLACE FUNCTION calculate_distance_sp(lat1 FLOAT, lon1 FLOAT, lat2 FLOAT, lon2 FLOAT)
RETURNS FLOAT AS $$
BEGIN
    RETURN ST_Distance(
        ST_SetSRID(ST_MakePoint(lon1, lat1), 4326)::geography,
        ST_SetSRID(ST_MakePoint(lon2, lat2), 4326)::geography
    );
END;
$$ LANGUAGE plpgsql;
"""

DDL_BORRAR_SP_DISTANCE = "DROP FUNCTION IF EXISTS calculate_distance_sp(FLOAT, FLOAT, FLOAT, FLOAT);"