from typing import Optional, Tuple

import jwt
import uvicorn
from azure.identity import DefaultAzureCredential
from fastapi import APIRouter, FastAPI, routing, status
from fastapi.openapi.models import OAuthFlowAuthorizationCode, OAuthFlows
from fastapi.params import Depends
from fastapi.security import OAuth2
from pydantic import BaseModel
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    SimpleUser,
)
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection

from example_app import __version__

router = APIRouter(prefix="/api", tags=["Users"])


class PayLoad(BaseModel):
    token: str


@router.post(path="/decode", status_code=status.HTTP_200_OK)
def decode_token(body: PayLoad) -> dict:
    """
    Decodes token.
    """

    decoded_token = jwt.decode(jwt=body.token, options={"verify_signature": False})

    return decoded_token


@router.post(path="/managed-identity-token", status_code=status.HTTP_200_OK)
def get_managed_identity_token(client_id: str) -> dict:
    """
    Gets a token from the managed identity.
    """
    credential = DefaultAzureCredential()

    token = credential.get_token(client_id)
    access_token = token.token

    decoded_token = jwt.decode(jwt=access_token, options={"verify_signature": False})
    decoded_token["token"] = access_token

    return decoded_token


class AuthMiddleware(AuthenticationBackend):
    """
    Implementation for middleware for starlette AuthenticationBackend
    """

    async def authenticate(
        self, request: HTTPConnection
    ) -> Optional[Tuple[AuthCredentials, SimpleUser]]:
        """
        Authenticate a request (HTTPConnection).
        If authentication is successful, defining a user instance (BaseUser)
        It authentication fails, AuthenticationError is thrown, defining a user instance (UnauthenticatedUser)
        """

        if "Authorization" not in request.headers:
            return

        try:
            # decode the token
            authorization: str = request.headers["Authorization"]
            token: str = authorization.split(" ")[1]
            decoded_token: dict = jwt.decode(
                token,
                options={"verify_signature": False},
            )
            name: str = decoded_token["name"]
            scopes: str = decoded_token["scp"]
            user: SimpleUser = SimpleUser(username=name)

            return AuthCredentials(scopes), user

        except Exception as ex:
            msg: str = "Could not authenticate!"
            raise AuthenticationError(msg, ex)


tenant_id: str = "5d65bff5-aca6-4063-9d75-44a22ca02ddf"
client_id: str = "acbbe6b8-12a4-4534-987b-11a79c7c7a30"
authorization_url: str = (
    f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize"
)
token_url: str = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"


def oauth2():
    scopes: dict = {f"api://{client_id}/user_impersonation": "user_impersonation"}

    authorization_code_flow: OAuthFlowAuthorizationCode = OAuthFlowAuthorizationCode(
        authorizationUrl=authorization_url, tokenUrl=token_url, scopes=scopes
    )

    return OAuth2(
        flows=OAuthFlows(authorizationCode=authorization_code_flow),
        scheme_name="OAuth2",
        description="description",
        auto_error=True,
    )


# app
app: FastAPI = FastAPI(
    title="Johannes Project App",
    description="A description of the Johannes Project App",
    version=__version__,
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": "true",
        "clientId": client_id,
        "appName": "johannes-app-service-auth-app",
    },
    swagger_ui_parameters={"displayRequestDuration": True},
)

# based on
# https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/

app.add_middleware(
    middleware_class=AuthenticationMiddleware,
    backend=AuthMiddleware(),
)


def get_routers() -> routing.APIRouter:
    router = APIRouter()

    router.include_router(router, dependencies=[Depends(oauth2())])

    return router


app.include_router(get_routers())

if __name__ == "__main__":
    uvicorn.run(app="app:app", host="localhost", port=9000, reload=True)
