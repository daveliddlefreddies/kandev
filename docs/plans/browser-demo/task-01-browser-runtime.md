---
id: "01-browser-runtime"
title: "Browser runtime and release compatibility"
status: in_progress
wave: 1
depends_on: []
plan: "plan.md"
requirements:
  - REQ-UI-BROWSER-DEMO-001
acceptance_criteria:
  - AC-UI-BROWSER-DEMO-001.1
  - AC-UI-BROWSER-DEMO-001.2
  - AC-UI-BROWSER-DEMO-001.3
  - AC-UI-BROWSER-DEMO-001.4
  - AC-UI-BROWSER-DEMO-001.5
  - AC-UI-BROWSER-DEMO-001.6
  - AC-UI-BROWSER-DEMO-001.7
  - AC-UI-BROWSER-DEMO-001.8
system_design:
  - ../../specs/ui/system-design/browser-demo.md
---

# Task 01: Browser runtime and release compatibility

## Summary and scope

Retain the browser demo behavior and adapt its fixtures and release steps to current `main`.
Include transport installation, scenario data, workspace responses, workflow operations, system data, and release assets.
Exclude production backend changes, real agent execution, and external integration connections.

## Acceptance

- Demo fixtures satisfy current shared types and pass focused protocol tests.
- The release workflow retains upstream verification and publishes a size-checked demo archive with its checksum.
- Both associated PRs have no rebase conflicts and pass their available CI gates.

## ASCII UI preview

Use [UI-01 in the plan](plan.md#ui-01-demo-task-session) for the task session and its phone composition.
The existing task, plan, workspace, and terminal controls remain authoritative. Criteria .2, .3, and .7 apply.

## Files and dependencies

- `apps/web/lib/browser-demo/`: transport, seed data, and simulated runtime modules.
- `apps/web/src/main.tsx`: installation before boot.
- Task and settings components: ready icons and the development entry-point action.
- Locale catalogs: translated entry-point labels.
- `.github/workflows/release.yml` and `scripts/browser-demo/`: archive distribution.
- Landing PR #169: separate archive consumption and deployment.

## Verification

Run from the repository root:

```bash
pnpm --dir apps/web exec vitest run lib/browser-demo components/task/task-item-ready.test.tsx components/settings/system/feature-toggles-settings.test.tsx
pnpm --dir apps/web typecheck
pnpm --dir apps/web lint
pnpm --dir apps/web i18n:check
pnpm --dir apps/web i18n:ratchet
python3 .github/scripts/release-workflow-contract_test.py
python3 .github/scripts/lint-action-pinning.py
./scripts/browser-demo/build-web-demo.sh /tmp/kandev-browser-demo
git diff --check
```

## Results

The October 5 rebase removed conflicts in both repositories.
Focused verification passed 54 tests across 10 files. Typecheck, translation checks, and 48 release-workflow tests passed.
The demo production build passed and produced a 13,576,609-byte compressed archive, below the 25 MiB limit.
Landing passed 117 tests and its combined production build. Its fresh Cloudflare Pages check passed.
Kandev full-suite CI and local lint remain pending at this revision. No local demo server started during this rebase.
