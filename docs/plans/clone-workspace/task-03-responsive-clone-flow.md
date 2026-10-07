---
id: "03-responsive-clone-flow"
title: "Add desktop and phone clone controls"
status: done
wave: 3
depends_on:
  - 02-atomic-clone-api
plan: "plan.md"
requirements:
  - REQ-WORKSPACES-CLONE-003
acceptance_criteria:
  - AC-WORKSPACES-CLONE-003.1
  - AC-WORKSPACES-CLONE-003.2
  - AC-WORKSPACES-CLONE-003.3
  - AC-WORKSPACES-CLONE-003.4
  - AC-WORKSPACES-CLONE-003.5
system_design:
  - ../../specs/workspaces/system-design/clone-workspace.md
---

# Task 03: Add desktop and phone clone controls

## Summary

Add workspace card actions and a shared clone form with desktop Dialog and
phone Drawer presentations. The name draft, submission logic, source ID,
response merge, and error handling remain shared.

## In scope

- Add typed `cloneWorkspaceAction` with encoded source path/name request and
  explicit errors. Preserve current ordinary creation behavior.
- Expose a visible accessible Clone card action for manageable supported
  sources; prevent the whole-card overlay from intercepting that action.
- Add localized copy-name suggestion, copy summary/exclusions, validation,
  pending state, cancel/focus return and error recovery without automatic POST retry.
- Guard synchronous double submission, merge using latest store state and the
  shared DTO mapper, deduplicate WS/HTTP arrivals, navigate to target overview,
  and preserve globally active workspace selection.
- Keep form draft above responsive branches; phone uses a short inset Drawer,
  single bounded scroll owner, safe areas and 44px controls. Apply `/mobile-parity`.
- Add keys to English and six complete real locale catalogs, generating the
  Traditional Chinese pair through `i18n:zh-hant`. Use `/tdd` for logic tests.

## Out of scope

Backend policy changes, active workspace switching, generic workspace settings
redesign, broad control sizing changes, or arbitrary configuration selection UI.

## Acceptance

1. Hook/action tests prove no request on invalid/unsupported source or blank
   name, one request on rapid clicks, retained draft on failure/resize, and an
   explicit uncertain-result check-list path.
2. Success merges once into current store state, retains existing projected
   scopes/visibility and concurrent workspace changes, navigates to the clone's
   overview, and leaves `activeId` unchanged.
3. Dialog/Drawer match UI-01/UI-02/UI-03 structure and localized copy, with real
   browser proof in Task 04 before this work package can be marked implemented.

## ASCII UI preview

Excerpt of [full preview](plan.md#ascii-ui-preview), covering 003.1-.5:

```text
UI-01 desktop | workspace card and clone dialog
| Team tools [Active] | Resources | [copy] | > |
+--------------------------------------------+
| Clone workspace                         X  |
| From: Team tools                           |
| Name [Team tools (copy)                  ] |
| Copy summary + exclusions                  |
|                        [Cancel] [Clone]    |
+--------------------------------------------+

UI-02 phone | card action opens inset bottom drawer
| Team tools [Active]              [copy]  > |
| Resources                                 |
    +-----------------------------------+
    | Clone workspace                   |
    | From: Team tools                  |
    | Name [Team tools (copy)        ]   |
    | Copy summary + exclusions         |
    | [Cancel]              [Clone]     |
    +-----------------------------------+

UI-03 shared form | failure retains draft
| Name [preserved draft                    ] |
| Could not clone. Try again.                |
|                        [Cancel] [Clone]    |
```

Labels are illustrative locale-key output. Pending keeps one form and disables
submission; uncertain network failure uses list-check wording. Phone geometry
follows `components/task/mobile/mobile-picker-sheet.tsx`; the footer clears the
safe area and only overflow content scrolls. Resize preserves shared draft.

## Verification

Fresh worktree prerequisite: `(cd apps && pnpm install --frozen-lockfile)` once
if dependencies are missing. Run all blocks from the repository root.

```bash
(cd apps/web && pnpm exec vitest run app/actions/workspaces.test.ts app/settings/workspace/use-workspace-clone.test.ts)
(cd apps/web && pnpm exec eslint app/actions/workspaces.ts app/settings/workspace/workspaces-page-client.tsx app/settings/workspace/workspace-clone-dialog.tsx app/settings/workspace/use-workspace-clone.ts)
(cd apps/web && pnpm run typecheck)
(cd apps/web && pnpm run i18n:zh-hant)
(cd apps/web && pnpm run i18n:check)
(cd apps/web && pnpm run i18n:ratchet)
git diff --check
```

Task 04 owns targeted managed production-build browser verification.

## Files likely touched

- `apps/web/app/actions/workspaces.ts` and `workspaces.test.ts`.
- `apps/web/app/settings/workspace/workspaces-page-client.tsx`.
- `apps/web/app/settings/workspace/workspace-clone-dialog.tsx` (new).
- `apps/web/app/settings/workspace/use-workspace-clone.ts` and `.test.ts` (new).
- `apps/web/lib/types/http.ts` if a named request type is useful.
- `apps/web/src/locales/{en,pt-pt,zh-cn,zh-hk,zh-tw,ja,ko}/workspaces.json`.
- Generated pseudo-locale artifacts only through the existing i18n scripts.

## Dependencies

Task 02 public clone API and standard post-commit event projection.

## Risks

Workspace cards contain an absolute overlay link. Response handlers capturing
an old `items` array can lose concurrent list changes. Remounting responsive
branches can lose draft/focus, and untranslated copy-name suggestions can
escape JSX-only scanning.

## Parallelism

`sequential`

## Inputs

- [Requirements](../../specs/workspaces/requirements/clone-workspace.md), 003.
- [Design](../../specs/workspaces/system-design/clone-workspace.md), responsive form and state.
- Existing workspace list, `mapWorkspaceItem`, workspace scopes/selectors,
  `settingsActionClassName`, Dialog/Drawer and mobile picker primitives.

## Results

24 targeted frontend tests passed. Scoped eslint and TypeScript checks passed. Traditional Chinese and pseudo catalogs regenerated; i18n:check and i18n:ratchet passed. Desktop/mobile browser evidence belongs to Task 04.

The final localized form summary explicitly excludes repository secrets and
keeps personal GitHub sign-in separate. All seven language catalogs and pseudo
were regenerated/checked; the phone browser test verifies this summary.

User-requested visual refinement: replace the prominent labeled card button
with a ghost copy icon beside navigation. Use the shared square icon size
(28px desktop; at least 44px on phones/coarse pointers), a localized tooltip
and workspace-specific accessible name. Phone placement stays in the title
row, without a dedicated action row. Existing responsive clone flow tests
now assert desktop dimensions and phone square-target/header alignment.

The compact icon revision passed scoped ESLint and TypeScript checks. The first
TypeScript attempt exhausted its 2 GB heap; a sequential retry passed with a
3 GB heap under a 4 GB process cap. No application code changed for the retry.
Task 04 records the fresh desktop/phone browser evidence.
