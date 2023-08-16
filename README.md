# swagger-ui-plugin-descope
Plugin for swagger-ui to replace the AuthorizationPopup with a Descope login


## Demo
[<img src="https://img.youtube.com/vi/xkxRsis0mBg/maxresdefault.jpg" width="50%">](https://www.youtube.com/watch?v=xkxRsis0mBg)


## Usage
Download the swagger-ui-plugin-descope.js release add it to your app

To your Swagger-UI web page add the following:

```html
<script src="https://unpkg.com/@descope/web-component@2.8.1/dist/index.js"></script>
<script src="https://unpkg.com/@descope/web-js-sdk@1.3.9/dist/index.umd.js"></script>
<script src="<your server>/swagger-ui-plugin-descope.js"></script>
<script>
    const descope_sdk = Descope({{ projectId: '< your descope projectId>', persistTokens: true, autoRefresh: true }});
</script>
```

On the swagger-ui configuration add the parameters:
```html
"descopeProjectId": "< your descope projectId>",
"descopeFlowId": "< your flow id >",
"plugins": [SwaggerUiDescopePlugin],
requestInterceptor: (req) => { req.headers['Authorization'] = 'bearer ' + descope_sdk.getSessionToken(); return req; },
```

Feel free to modify the requestInterceptor to suit how your api expects the session token. In the above snippet the token is passed as a authorization bearer.

Here is a complete example of the Swagger-ui config used in the demo:
```html
<script>

    document.addEventListener("DOMContentLoaded", function() {
    const ui = SwaggerUIBundle({
        url: '/openapi.json',
    "dom_id": "#swagger-ui",
"layout": "BaseLayout",
"deepLinking": true,
"showExtensions": true,
"showCommonExtensions": true,
"descopeProjectId": "P2TsMEQkHlw0hCN9GJrldp9SKRFT",
"descopeFlowId": "sign-in-swagger",
"plugins": [SwaggerUiDescopePlugin],
requestInterceptor: (req) => { req.headers['Authorization'] = 'bearer ' + descope_sdk.getSessionToken(); return req; },
    presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
    })
    })</script>
```
