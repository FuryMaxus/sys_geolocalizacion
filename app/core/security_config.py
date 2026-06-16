import os
from dotenv import load_dotenv
from litestar.security.jwt import OAuth2PasswordBearerAuth, Token
from litestar.connection import ASGIConnection



load_dotenv()

async def retrieve_user_handler(token: Token, connection: ASGIConnection) -> dict:
    return {
        "email": token.sub,
        "rol": token.extras.get("rol", "ROL_USUARIO")
    }
s

jwt_auth = OAuth2PasswordBearerAuth[dict](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=os.environ.get("SECRET_KEY", "clave_secreta_secretita_:)"),
    token_url="http://localhost:8085/bff/auth/ingreso", 
    exclude=["/schema", "/docs", "/schema/swagger", "/schema/elements"]
)