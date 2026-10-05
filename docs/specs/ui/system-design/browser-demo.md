---
status: current
system: ui
requirements:
  - REQ-UI-BROWSER-DEMO-001
---

# Browser demo design

## Ownership and isolation

The UI owns the demo transport and fixtures under `apps/web/lib/browser-demo`.
The backend and real agent adapters remain unchanged.
`mode.ts` limits installation to the dedicated build or explicit development entry point.
`src/main.tsx` waits for demo installation before it loads the application boot payload.

## Transport and state

`install.ts` replaces browser fetch and WebSocket transport for demo requests.
The worker owns seeded data, request dispatch, and simulated session events.
Browser storage retains demo changes. Reset restores the seed without changing real application storage.
Unsupported routes remain explicit errors rather than false success responses.

## Application capabilities

`scenario.ts` supplies repositories, sessions, histories, approval requests, questions, plans, and pull-request comments.
The file fixtures expose repository-specific trees and changed-file contents.
The worker simulates task progress through tool events and an idle review state.
Workflow modules provide editable workflow data, templates, synchronization, and transfer operations.
The system runtime supplies database, disk, and storage data through the current typed contracts.
These modules implement criteria .2 through .7 without a separate UI.

## Release distribution

`scripts/browser-demo/build-web-demo.sh` builds the SPA under `/browser-demo/app/`.
Relative output paths resolve from the repository root. Absolute paths remain unchanged.
The release workflow packages the bundle, enforces the 25 MiB compressed limit, and publishes its SHA-256 checksum.
The landing repository consumes this archive separately. Criteria .1 and .8 cover installation and distribution.

## Verification

Worker, scenario, workflow, system-runtime, and installation tests exercise the simulated protocol and seed data.
Typecheck catches changes to shared response contracts. Translation checks cover the development entry-point action.
The production build checks worker bundling and the public base path.
Local browser inspection remains necessary to confirm rendered interactions across desktop and phone layouts.
