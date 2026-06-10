from litestar import Litestar
from app.core.db_config import db_plugin
from app.repository import location_repository
from app.api.v1.location_controller import LocationController


app = Litestar(
    route_handlers=[
        LocationController,
    ],
    plugins=[db_plugin],
    debug=True
)