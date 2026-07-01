#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Create a Noomo Motion Vite React project skeleton.")
    parser.add_argument("target_dir")
    parser.add_argument("--name", default="noomo-motion-site")
    parser.add_argument("--title", default="Noomo Motion Site")
    args = parser.parse_args()

    root = Path(args.target_dir).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)

    package = {
        "name": args.name,
        "version": "0.1.0",
        "private": True,
        "type": "module",
        "scripts": {
            "dev": "vite --host 0.0.0.0",
            "build": "vite build",
            "preview": "vite preview --host 0.0.0.0",
        },
        "dependencies": {
            "@gsap/react": "latest",
            "@react-three/drei": "latest",
            "@react-three/fiber": "latest",
            "gsap": "latest",
            "lenis": "latest",
            "lucide-react": "latest",
            "react": "latest",
            "react-dom": "latest",
            "three": "latest",
        },
        "devDependencies": {
            "@vitejs/plugin-react": "latest",
            "vite": "latest",
        },
    }

    write(root / "package.json", json.dumps(package, indent=2) + "\n")
    write(root / "index.html", f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{args.title}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
""")
    write(root / "vite.config.js", """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
""")
    write(root / "src/main.jsx", """import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import './styles.css'

createRoot(document.getElementById('root')).render(<App />)
""")
    write(root / "src/App.jsx", """export default function App() {
  return <main className=\"app\">Noomo Motion project ready.</main>
}
""")
    write(root / "src/styles.css", """html, body, #root {
  margin: 0;
  min-height: 100%;
}

body {
  font-family: Inter, ui-sans-serif, system-ui, sans-serif;
}
""")
    (root / "src/components").mkdir(parents=True, exist_ok=True)
    (root / "src/motion").mkdir(parents=True, exist_ok=True)
    (root / "src/data").mkdir(parents=True, exist_ok=True)
    (root / "public/assets/generated").mkdir(parents=True, exist_ok=True)
    write(root / "MOTION_BRIEF.md", f"# {args.title} Motion Brief\n\nDraft during generation.\n")


if __name__ == "__main__":
    main()

