from pathlib import Path

from agents.crud.models.generation_context import GenerationContext


class FrontendInstaller:
    """
    Instala la estructura base React + Vite + TypeScript.
    """

    METADATA_KEY = "frontend_installed"


    def install(
        self,
        context: GenerationContext,
    ) -> None:

        if context.get_metadata(self.METADATA_KEY, False):
            return


        frontend = (
            context.project.source_path
            / "frontend"
        )

        frontend.mkdir(
            parents=True,
            exist_ok=True,
        )


        files = {

            "package.json": """
{
  "name": "generated-frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build"
  },
  "dependencies": {
    "axios": "^1.7.0",
    "bootstrap": "^5.3.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "react-router-dom": "^6.28.0"
  },
  "devDependencies": {
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.0",
    "typescript": "^5.6.0",
    "vite": "^5.4.0"
  }
}
""",

            "index.html": """
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Generated App</title>
</head>

<body>

<div id="root"></div>

<script type="module" src="/main.tsx"></script>

</body>
</html>
""",

            "main.tsx": """
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

ReactDOM
.createRoot(
    document.getElementById("root")!
)
.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
""",

            ".env": """
VITE_API_URL=http://127.0.0.1:8000
""",

            "config/api.ts": """
export const API_URL =
    import.meta.env.VITE_API_URL ||
    "http://127.0.0.1:8000";
""",

            "vite.config.ts": """
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
    plugins:[
        react()
    ]
});
""",

            "tsconfig.json": """
{
 "compilerOptions":{
   "target":"ES2020",
   "useDefineForClassFields":true,
   "lib":["ES2020","DOM","DOM.Iterable"],
   "allowJs":false,
   "skipLibCheck":true,
   "esModuleInterop":true,
   "allowSyntheticDefaultImports":true,
   "strict":true,
   "module":"ESNext",
   "moduleResolution":"Bundler",
   "resolveJsonModule":true,
   "jsx":"react-jsx"
 }
}
"""
        }


        for name, content in files.items():

            file = frontend / name

            file.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            if not file.exists():

                file.write_text(
                    content.strip(),
                    encoding="utf-8"
                )


        context.set_metadata(
            self.METADATA_KEY,
            True,
        )

        print("✓ Frontend React/Vite instalado")
