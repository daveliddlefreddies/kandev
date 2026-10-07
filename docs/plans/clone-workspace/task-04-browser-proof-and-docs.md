---
id: "04-browser-proof-and-docs"
title: "Prove browser behavior and document cloning"
status: done
wave: 4
depends_on:
  - 03-responsive-clone-flow
plan: "plan.md"
requirements:
  - REQ-WORKSPACES-CLONE-001
  - REQ-WORKSPACES-CLONE-002
  - REQ-WORKSPACES-CLONE-003
acceptance_criteria:
  - AC-WORKSPACES-CLONE-001.1
  - AC-WORKSPACES-CLONE-001.2
  - AC-WORKSPACES-CLONE-001.3
  - AC-WORKSPACES-CLONE-001.4
  - AC-WORKSPACES-CLONE-001.5
  - AC-WORKSPACES-CLONE-001.6
  - AC-WORKSPACES-CLONE-001.7
  - AC-WORKSPACES-CLONE-002.4
  - AC-WORKSPACES-CLONE-003.1
  - AC-WORKSPACES-CLONE-003.2
  - AC-WORKSPACES-CLONE-003.3
  - AC-WORKSPACES-CLONE-003.4
  - AC-WORKSPACES-CLONE-003.5
system_design:
  - ../../specs/workspaces/system-design/clone-workspace.md
---

# Task 04: Prove browser behavior and document cloning

## Summary

Prove the complete desktop and phone clone flow through the production API and
UI. Publish concise instructions with actual copy boundaries only after the
feature works, then update this package's execution and specification statuses.

## In scope

- Apply `/e2e` and `/mobile-parity`; seed disposable source configuration through
  existing API fixtures, then clone through the UI without mocking success.
- Verify copied repository/workflow settings and GitHub PR/issue defaults via
  settings/dashboard DOM, reload persistence, empty history, and source isolation.
- Add phone coverage for the real drawer, cancel/focus, draft retention, pending
  double-tap guard, failure retry, long content, 44px targets and no page overflow.
- Arm HTTP/WS causal waits before actions. Use actual backend clone response to
  correlate the new ID. Keep shared fixture mutation cleanup explicit.
- Use full-store backend tests from Task 02 for security/rollback; do not expose
  tokens to browser fixtures or add artificial API-failure mocks as encryption proof.
- Apply `/docs-maintainer`: update the workspace portion of
  `docs/public/tasks-and-workflows.md`, and search root README/screenshots for
  conflicting claims. Keep walkthrough copy as a short how-to within that page.
- Record each task-defined command/result and compare final behavior with all
  requirement IDs before promoting paired drafts and marking the plan implemented.

## Out of scope

Broad local QA/review/verify passes, new screenshots or videos, performance
benchmarks, commits, pushes, PR creation, and unrelated E2E cleanup.

## Acceptance

1. Desktop and phone tests complete cloning with real persistence, show copied
   query defaults for both kinds after entry/reload, and prove no source mutation
   or task/session history copying.
2. Rendered phone checks match UI-02/UI-03, preserve form state across viewport
   changes, meet touch/containment/focus requirements, and handle failure retry.
   Unsupported sources have no executable clone action.
3. Public instructions describe actual includes/exclusions, credential reuse
   and personal sign-in, while all work orders record exact results and the
   requirement/design statuses accurately describe implementation.

## ASCII UI preview

Use the combined [UI preview](plan.md#ascii-ui-preview). Browser proof covers
001.7 and 003.1-.5, including the following structural checkpoints:

```text
UI-01 desktop | dialog then target overview
| From: source | Name [copy name] | Summary/exclusions |
|                                [Cancel] [Clone]    |
              -> cloned workspace settings overview

UI-02 phone | inset drawer, one internal scroll owner
    +-----------------------------------+
    | Clone workspace                   |
    | From: source                      |
    | Name [copy name               ]   |
    | Copy summary/exclusions (scroll)  |
    | [Cancel]              [Clone]     |
    +-----------------------------------+

UI-03 shared form | retry after definite failure
| Name [unchanged draft] | Error | [Cancel] [Clone] |
```

Check actual control bounding boxes, safe-area padding, focused cancellation,
and scroll owner. ASCII spacing is illustrative; labels are localized.

## Verification

Run from the repository root. Managed E2E builds fresh web/backend assets and
uses one worker per shard; run projects sequentially and confirm test discovery.

```bash
(cd apps/web && pnpm e2e:run --project chromium tests/settings/workspace-clone.spec.ts)
(cd apps/web && pnpm e2e:run --project mobile-chrome tests/settings/mobile-workspace-clone.spec.ts)
(cd apps/web && pnpm exec eslint e2e/tests/settings/workspace-clone.spec.ts e2e/tests/settings/mobile-workspace-clone.spec.ts)
node --test scripts/validate-public-docs.test.mjs
node scripts/validate-public-docs.mjs
python3 scripts/list-docs.py validate
python3 scripts/lint-spec-files.test.py
python3 scripts/lint-spec-files.py --all
git diff --check
```

Invoke `.github/scripts/pr-docs.cjs`'s exported `validateCoverage` with the
actual changed-file list and the plan/work-order/requirement/design contents
to check local delivery traceability without publishing a GitHub status.
If a product failure requires a fix, rerun its affected task-defined check;
do not substitute a broad suite for the focused evidence.

## Files likely touched

- `apps/web/e2e/tests/settings/workspace-clone.spec.ts` (new).
- `apps/web/e2e/tests/settings/mobile-workspace-clone.spec.ts` (new).
- `apps/web/e2e/helpers/workspace-clone.ts` (new only if shared setup warrants it).
- `apps/web/e2e/helpers/api-client.ts` only for necessary reusable fixture methods.
- `docs/public/tasks-and-workflows.md`.
- `docs/plans/clone-workspace/plan.md` and work-order Results/status fields.
- `docs/specs/workspaces/requirements/clone-workspace.md` and
  `docs/specs/workspaces/system-design/clone-workspace.md` lifecycle fields.

## Dependencies

Tasks 01-03 complete. Test design follows the packet from the first TDD pass;
this work order supplies final production-build browser evidence, not a broad audit.

## Risks

GitHub default queries differ from saved default views; seed and verify both.
Phone/project selection can silently omit tests. `e2eReset` does not restore
every shared configuration row, so prefer disposable workspaces and cleanup.

## Parallelism

`sequential`

## Inputs

- [Requirements](../../specs/workspaces/requirements/clone-workspace.md).
- [Design](../../specs/workspaces/system-design/clone-workspace.md).
- Workspace settings switcher E2E pattern, GitHub settings/default-query fixtures,
  causal wait helpers, and mobile drawer geometry tests.

## Results

Final production-build browser checks passed on 2026-10-08 (Europe/Lisbon):

- Desktop: 2/2 passed in 15.9s, log `/tmp/kandev-run.e2e.q9GAq44M.log`.
- Phone: 2/2 passed in 16.9s, log `/tmp/kandev-run.e2e.5jZD6k00.log`.
- Both flows create through the real API, read back copied repositories/workflows,
  preserve GitHub PR/issue defaults across reload, prove empty task history and
  source isolation, and leave the globally active workspace unchanged.
- Desktop covers cancel/focus and draft retention across phone/desktop resize.
  Phone covers inset-sheet geometry, 44px controls, no horizontal overflow,
  explicit secret/sign-in exclusions, blank-name blocking, cancel/focus, one
  pending POST and recovery after a definite failure.

After a reported machine interruption, browser projects ran sequentially in host
mode under a 3 GB memory cap, no swap, a two-core CPU quota and one worker. The
cause of the interruption was not established. Fresh web/backend/plugin artifacts
were built within the same resource limits before the final runs. Commands from
the repository root (with the installed Go/Node/pnpm on `PATH`):

```bash
systemd-run --user --scope --quiet --collect -p MemoryMax=3G -p MemorySwapMax=0 -p CPUQuota=200% pnpm --dir apps/web e2e:run --host --no-build --project chromium tests/settings/workspace-clone.spec.ts
systemd-run --user --scope --quiet --collect -p MemoryMax=3G -p MemorySwapMax=0 -p CPUQuota=200% pnpm --dir apps/web e2e:run --host --no-build --project mobile-chrome tests/settings/mobile-workspace-clone.spec.ts
```

Public clone instructions now describe the shipped includes/exclusions,
credential reuse, unchanged active selection and ambiguous-request recovery.
Public-document validation passed (62 tests and 47 pages); catalog validation,
36 specification-linter tests and all-file specification lint passed. Actual
changed-file documentation coverage accepts all four work orders with no errors.
Tracked and untracked whitespace checks passed. Requirements are now `active`,
the design `current`, and the plan `implemented`. Changes were uncommitted at
the implementation checkpoint; the subsequent user continuation starts commit
delivery with normal hooks.

### Compact Clone action refinement

The user-requested card refinement replaces the labeled button with a ghost
copy icon and localized tooltip. Phone placement moves into the title row.
After rebuilding the web assets, the same bounded, sequential host commands
above passed again:

- Desktop: 2/2 passed in 12.2s, log `/tmp/kandev-run.e2e.uEuTZz4V.log`.
  Assertions cover the 28px square action, tooltip, 44px size below the 768px
  breakpoint and 28px size at/above it, alongside real cloning and resize.
- Phone: 2/2 passed in 16.9s, log `/tmp/kandev-run.e2e.JfM4PPSE.log`.
  Assertions cover a square target of at least 44px aligned with the title,
  plus the existing real clone, sheet containment, cancellation and retry flow.

The focused desktop size regression failed against the old wide button before
the implementation changed. The public procedure and durable UI previews now
identify the compact copy icon. Screenshot publication remains a delivery step
outside this implementation work order.
