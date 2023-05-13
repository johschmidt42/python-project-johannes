import json
from pathlib import Path

from fastapi.openapi.utils import get_openapi

from example_app.app import app

FOLDER_PATH = Path(__file__).parent.absolute()
ROOT_PATH = FOLDER_PATH.parent.absolute()
DOCS_PATH = ROOT_PATH / "docs"


def create_openapi_json() -> None:
    with open(file=DOCS_PATH / "openapi.json", mode="w") as f:
        openapi: dict = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            routes=app.routes,
        )
        json.dump(obj=openapi, fp=f)


if __name__ == "__main__":
    create_openapi_json()
