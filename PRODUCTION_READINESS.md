# Production readiness assessment

Status: **static browser prototype; deployment and browser-security validation required**.

## Current scope
This repository contains a self-contained HTML application. A root `index.html` entry point has been added on this hardening branch so GitHub Pages can serve it from the repository root.

## Release blockers
1. Validate HTML and all inline JavaScript in CI; test on current Chrome, Firefox, and mobile browsers.
2. Review all dynamic `innerHTML` assignments. Never interpolate user input, imported files, terminal commands, or AI output as HTML; use `textContent` or safe DOM construction.
3. Keep API keys out of committed files and explain that browser-stored keys are accessible to anyone using the same browser profile and may be exposed to injected scripts.
4. Add import/export schema validation, backup recovery, storage quota handling, and destructive-action confirmation.
5. Document external CDN/API dependencies, data flows, browser permissions, and known limitations.
6. Add accessibility, keyboard, reduced-motion, and offline behavior tests.

## Release gate
A successful syntax check is not a security audit or browser compatibility certification. Complete the above reviews and perform a manual cross-browser smoke test before calling this production-ready.
