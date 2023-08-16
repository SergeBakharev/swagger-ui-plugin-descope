import type { SwaggerUIPlugin } from "swagger-ui"

import DescopeAuthorizationPopup from "./descopeAuthorizationPopup";

export const SwaggerUiDescopePlugin: SwaggerUIPlugin = (system: any) => {
    return {
    components: {
        authorizationPopup: DescopeAuthorizationPopup
    },
    
  }
}
  
if (typeof window !== "undefined") {
(window as any)["SwaggerUiDescopePlugin"] = SwaggerUiDescopePlugin;
}
