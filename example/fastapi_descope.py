from fastapi import Request, HTTPException, Security, Depends
from typing import Annotated, Any
from fastapi.security import APIKeyCookie, HTTPBearer
from fastapi.openapi.docs import swagger_ui_default_parameters
import json
from typing import Any, Dict, Optional

from fastapi.encoders import jsonable_encoder
from starlette.responses import HTMLResponse

from descope import (
    SESSION_COOKIE_NAME,
    AuthException,
)



def descope_get_swagger_ui_html(
    *,
    openapi_url: str,
    title: str,
    swagger_js_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
    swagger_css_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    swagger_favicon_url: str = "https://fastapi.tiangolo.com/img/favicon.png",
    oauth2_redirect_url: Optional[str] = None,
    init_oauth: Optional[Dict[str, Any]] = None,
    swagger_ui_parameters: Optional[Dict[str, Any]] = None,
    swagger_ui_plugins: Optional[list[str]] = None,
) -> HTMLResponse:
    current_swagger_ui_parameters = swagger_ui_default_parameters.copy()
    if swagger_ui_parameters:
        current_swagger_ui_parameters.update(swagger_ui_parameters)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link type="text/css" rel="stylesheet" href="{swagger_css_url}">
    <link rel="shortcut icon" href="{swagger_favicon_url}">
    <script src="https://unpkg.com/@descope/web-component@2.8.1/dist/index.js"></script>
    <script src="https://unpkg.com/@descope/web-js-sdk@1.3.9/dist/index.umd.js"></script>
    <title>{title}</title>
    </head>
    <body>
    <div id="swagger-ui">
    </div>
    <script>
      const descope_sdk = Descope({{ projectId: '{swagger_ui_parameters.get('descopeProjectId')}', persistTokens: true, autoRefresh: true }});
      </script>
    <script type="module" src="./js/swagger-ui-plugin-descope.js"></script>
    <script src="{swagger_js_url}"></script>
    <!-- `SwaggerUIBundle` is now available on the page -->
    <script>

    document.addEventListener("DOMContentLoaded", function() {{
    const ui = SwaggerUIBundle({{
        url: '{openapi_url}',
    """

    for key, value in current_swagger_ui_parameters.items():
        html += f"{json.dumps(key)}: {json.dumps(jsonable_encoder(value))},\n"

    if swagger_ui_plugins:  # needs to be a literal not a str, thus can't use current_swagger_ui_parameters
        html += f"\"plugins\": [{', '.join(swagger_ui_plugins)}],\n"

    if oauth2_redirect_url:
        html += f"oauth2RedirectUrl: window.location.origin + '{oauth2_redirect_url}',"
    
    html += "requestInterceptor: (req) => { req.headers['Authorization'] = 'bearer ' + descope_sdk.getSessionToken(); return req; },"

    html += """
    presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
    })"""

    if init_oauth:
        html += f"""
        ui.initOAuth({json.dumps(jsonable_encoder(init_oauth))})
        """

    html += """
    })</script>

    </body>
    </html>
    """
    return HTMLResponse(html)


auth_scheme_cookie = APIKeyCookie(name=SESSION_COOKIE_NAME)
auth_scheme_bearer = HTTPBearer()


def descope_cookie_auth(request: Request, session_token: Annotated[str, Security(APIKeyCookie(name=SESSION_COOKIE_NAME))]):
    cookies = request.cookies.copy()
    session_token = cookies.get(SESSION_COOKIE_NAME, "")
    if not session_token: 
        raise HTTPException(detail="Access denied", status_code=401)
    try:
        jwt_response = descope_client.validate_session(session_token)
    except AuthException as exception:
        raise HTTPException(detail="Access denied", status_code=401) from exception


# TODO
# def descope_cookie_auth_refresh(request: Request, session_token: Annotated[str, Security(APIKeyCookie(name=SESSION_COOKIE_NAME))], refresh_token: Annotated[str, Security(APIKeyCookie(name=REFRESH_SESSION_COOKIE_NAME))]):
#     cookies = request.cookies.copy()
#     session_token = cookies.get(SESSION_COOKIE_NAME, None)
#     refresh_token = cookies.get(REFRESH_SESSION_COOKIE_NAME, None)
#     if not (session_token and refresh_token):  # both session and refresh tokens need to be present
#         raise HTTPException(detail="Access denied", status_code=401)
#     try:
#         jwt_response = descope_client.validate_and_refresh_session(
#             session_token, refresh_token
#         )
#     except AuthException as exception:
#         raise HTTPException(detail="Access denied", status_code=401) from exception
    
#     if jwt_response.get(COOKIE_DATA_NAME, None):
#         print(f"{jwt_response[SESSION_TOKEN_NAME]}, {jwt_response[COOKIE_DATA_NAME]}")
#         # refresh their tokens via cookie
#         response.set_cookie(SESSION_TOKEN_NAME, jwt_response[SESSION_TOKEN_NAME])
#         response.set_cookie(COOKIE_DATA_NAME, jwt_response[COOKIE_DATA_NAME])
#         return {"message": "You are authenticated"}

def descope_bearer_auth(session_token: Annotated[str, Security(HTTPBearer())]):
    try:
        jwt_response = descope_client.validate_session(session_token.credentials)
    except AuthException as exception:
        raise HTTPException(detail="Access denied", status_code=401) from exception
    return jwt_response


# check both
async def descope_cookie_or_apibearer_check(cookie_result=Depends(auth_scheme_cookie), bearer_result=Depends(auth_scheme_bearer)):
    if not (cookie_result or bearer_result):
        raise Exception