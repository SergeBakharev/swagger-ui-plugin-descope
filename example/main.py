from typing import Annotated

from fastapi import FastAPI, Security
from fastapi.staticfiles import StaticFiles
import uvicorn
from descope import DescopeClient

from fastapi_descope import descope_get_swagger_ui_html, auth_scheme_bearer


# TODO: move to env var
PROJECT_ID = "P2TsMEQkHlw0hCN9GJrldp9SKRFT"

app = FastAPI(docs_url=None)
app.mount("/js", StaticFiles(directory="js"), name="js")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return descope_get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_ui_plugins=["SwaggerUiDescopePlugin"],
        swagger_ui_parameters={"descopeProjectId": PROJECT_ID, "descopeFlowId": "sign-up-or-in"},
    )

# init the DescopeClient
descope_client = DescopeClient(PROJECT_ID)


@app.get("/open")
def root():
    return {"message": "Hello this api doesn't require auth"}


@app.get("/protected")
def protected_api(session_token: Annotated[str, Security(auth_scheme_bearer)]):
    """An example of an API that requires authentication"""
    return {"message": "You are authenticated"}


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "main:app",
        reload=True  # reload the app as the code changes
    )


if __name__ == "__main__":
    main()

