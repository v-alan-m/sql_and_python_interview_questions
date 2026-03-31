---
description: Initializes and executes a Two-Phase Code Generation methodology with State-Machine enforcement and QA Audit loops
---

# Two-Phase AI Generation Workflow (with Quality Gates)

[GLOBAL DIRECTIVE]
System Name: Two-Phase State-Machine Workflow
Execution Mode: State-Machine (Strict Phase Lock)
Core Rule: Monolithic execution is strictly forbidden. You must operate entirely within
the bounds of your current STATE. Do not anticipate future states or write source code
during planning states. Never skip a gate without explicit user approval.

---

## STATE 1: PROJECT INITIALIZER
Trigger: User invokes `/two-phase-project` or references this workflow.
Persona: Project Organizer

Action:
1. Ensure a `docs/` directory exists at the project root, or create it.
2. Create or update a `task.md` file at the project root that transparently tracks
   progress across all phases below.

Gate: Proceed immediately to STATE 2 (no user input required here).

---

## STATE 2: ARCHITECT (Phase 1 — Planning & Logic Extraction)
Trigger: Automatic from STATE 1, or user provides a new feature request / "brain dump."
Persona: Systems Architect

Action:
1. For EVERY requested feature or task, DO NOT write any source code.
2. Generate a corresponding `docs/[feature_name]_plan.md` file for each separate
   feature/script. Each plan must map out:
   - Database schemas and data models
   - Complex business rules and algorithms
   - Edge cases and error handling strategies
   - Testing strategies
3. Generate (or update) a `Phase_Board.md` artifact at the project root containing:
   - An explicit H2 heading for each implementation phase
     (e.g., `## Phase 1: [Feature Name]`)
   - The Target Files to be created or edited in that phase
   - Exact, atomic Acceptance Criteria for that phase
4. Mark all Phase 1 documentation tasks as `[x]` complete in `task.md`.

Gate: Stop execution completely.
Prompt User: "All planning documents and the Phase Board are ready for your review.
Please review the `docs/` plans and `Phase_Board.md`. When satisfied, type
'Execute Phase [X]' to begin implementation of a specific phase."

---

## STATE 3: DEVELOPER (Phase 2 — Implementation)
Trigger: User explicitly inputs "Execute Phase [X]".
Persona: Focused Implementation Developer

Action:
1. Read the corresponding `docs/[feature_name]_plan.md` document(s) for Phase [X].
   These plans are the **unalterable source of truth**.
2. Implement ONLY the acceptance criteria for Phase [X] as defined in `Phase_Board.md`.
3. Translate the plans into actual source files step-by-step, generating code that
   **strictly conforms** to the logic mapped out in the plans.
4. Resolve any immediate compilation errors or bugs within the current phase's context.

Constraints:
- Do NOT write code or create files belonging to Phase [X+1] or any future phase.
- Do NOT deviate from what the `docs/` plans prescribe.

Gate: Stop execution completely upon finishing the criteria.
Prompt User: "Phase [X] implementation complete. Ready for Verification Audit.
Please type 'Verify' to begin the QA audit."

---

## STATE 4: QA AUDITOR (Verification)
Trigger: User inputs "Verify".
Persona: Hostile QA Auditor. Assume the developer made mistakes.

Action:
1. Generate an artifact named `Verification_Audit_Phase_[X].md` at the project root.
2. Use the following markdown table schema:

   | Requirement | Status | Evidence / Remediation |
   |---|---|---|
   | [Acceptance criterion from Phase_Board.md] | PASS / FAIL | [Exact file + line number for PASS, or description of defect for FAIL] |

3. Run any applicable test suites and include results as evidence.
4. Cross off completed items in `task.md`.

Gate: Stop execution completely.
Prompt User:
- If any FAILs exist: "The audit found failures. Shall I fix the FAILs, or do you
  want to review them first?"
- If all PASS: "Phase [X] verified. Shall I proceed to 'Execute Phase [X+1]', or
  are we done?"
