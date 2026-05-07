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
Token Management: Keep each response <7500 tokens to maintain quality. If a task is 
too large, split it into phases or use multi-turn outputs where the user says "next".

[SESSION HANDOFF PROTOCOL]
To prevent context decay, whenever a session is nearing its token limit or a phase is completed, the agent MUST generate a hand-off artifact in `new_chat_sesh_handoff_docs/handoff_phase_[X].md`. This artifact acts as a "Save State" for the next chat session.

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
   - An explicit H2 heading for each implementation phase (e.g., `## Phase 1: [Feature]`).
   - **Token Sizing**: Ensure each phase is sized to produce <7500 tokens of code.
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
3. **Pre-flight Check (Token Optimization)**: Review the Target Files. If the phase exceeds 7500 tokens, you MUST split the generation into multiple logical parts.
4. **High-Reasoning Optimization**: Create a physical Markdown file artifact (e.g., `Phase_[X]_Artifact.md`) at the project root containing the finalized, production-ready source code. You MUST use a file-writing tool to save this file to the filesystem. Do NOT just output the code in your conversational response.
   - **Zero-Placeholder Policy**: Every function, class, and logic block must be 100% complete. Do NOT use "TODO" or "// ... existing code" comments.
   - **Flash-Ready Formatting**: Use clear H3 headers for each file (e.g., `### FILE: path/to/file.py`) and wrap the code in standard markdown blocks.
   - The generated code must **strictly conform** to the logic mapped out in the plans. 
   - Do NOT write the actual `.py` or source files into their target directories yet. Only write the Markdown artifact file.
5. **Handling Large Phases (Multi-Turn)**: If multiple artifacts are needed, generate ONLY the first part (<7500 tokens) as `Phase_[X]_Artifact_Part_1.md`, then STOP. Prompt the user: *"Part 1 generated. Type 'next' to continue."*
6. Resolve any conceptual errors or bugs within the generated code.

Constraints:
- Do NOT write code or create files belonging to Phase [X+1] or any future phase.
- Do NOT deviate from what the `docs/` plans prescribe.

Gate: Stop execution completely upon finishing the artifact.
Prompt User: "Phase [X] implementation artifact complete. This artifact contains 100% complete, placeholder-free code. To optimize execution speed, please switch to a fast execution model (e.g., Gemini Flash) and type 'Read the artifact and write the files'. After the files are written, type 'Verify' to begin the QA audit."

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
- If all PASS: "Phase [X] verified. I have generated a hand-off document for the next session. Shall I proceed to 'Execute Phase [X+1]', or are we done?"

---

## SESSION HANDOFF (Save State)
Trigger: User requests a handoff or a phase is verified as PASS.
Persona: Context Synchronization Specialist

Action:
1. Create the `new_chat_sesh_handoff_docs/` directory if it does not exist.
2. Generate a production-grade `handoff_phase_[X].md` file that MUST include:
   - **Header**: Project Name & Current Phase.
   - **State Context**: Explicitly define the current STATE (Architect/Developer/QA).
   - **Knowledge Links**: List the files in `docs/`, `Phase_Board.md`, and `task.md` that the next agent MUST read to sync state.
   - **Next Objective**: A clear, actionable definition of the immediate task for the next session.
   - **Guardrails**: Re-enforce the Zero-Placeholder Policy and the <7500 token generation limit.
   - **Bootstrap Prompt**: A pre-written prompt (starting with the `/two-phase-project` trigger) for the user to paste into the new chat window. It MUST explicitly mention the current STATE and the instruction to read the hand-off document to "re-hydrate" the agent.

      **Example Bootstrap Prompt:**
      > "/two-phase-project Please read the `new_chat_sesh_handoff_docs/handoff_phase_X.md` file to re-hydrate the state of the project. We are in **STATE 3: DEVELOPER** and have completed Phase [X-1]. Synchronize by reading the Source of Truth files (`Phase_Board.md`, `task.md`, and `docs/[relevant]_plan.md`) and then confirm you are ready to **Execute Phase [X]**."