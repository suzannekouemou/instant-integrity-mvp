Speckit Slash Commands – Usage Guide

Date: 2025-11-23

Purpose
- This guide explains the available Speckit slash commands configured in this repository under .github/prompts and .github/agents, their purpose, prerequisites, typical flow, inputs/outputs, and cross-links to the artifacts they produce.

Where the commands live
- Prompts (command triggers): .github/prompts/
- Agents (behavior specs): .github/agents/

Key prerequisites (used by several commands)
- Scripts referenced by agents (do not modify here):
  - .specify/scripts/bash/check-prerequisites.sh
  - .specify/scripts/bash/create-new-feature.sh
  - .specify/scripts/bash/setup-plan.sh
  - .specify/scripts/bash/update-agent-context.sh
- Constitution: .specify/memory/constitution.md

General usage notes
- Run commands in the repository context (e.g., as slash commands in the agent-enabled chat, or via your automations).
- Many agents require existing feature artifacts (spec.md, plan.md, tasks.md). If missing, they will instruct you to run the prerequisite command first.
- Arguments: Each command accepts free-form text after the slash (shown as $ARGUMENTS in agents). Use concise, relevant context.

Commands overview

1) /speckit.specify
- Purpose: Create or update a feature specification from a natural language description.
- Prompt: .github/prompts/speckit.specify.prompt.md
- Agent: .github/agents/speckit.specify.agent.md
- Prereqs:
  - Will call create-new-feature.sh to create/check out a feature branch and initialize spec files.
  - Uses .specify/templates/spec-template.md internally (managed by scripts).
- Inputs:
  - Natural language feature description (after the command).
- Outputs (written):
  - specs/<number>-<short-name>/spec.md
  - specs/<number>-<short-name>/checklists/requirements.md (quality checklist)
- Notes:
  - Limits [NEEDS CLARIFICATION] markers to max 3.
  - Handoffs: Can route to /speckit.plan and /speckit.clarify.

2) /speckit.clarify
- Purpose: Ask up to 5 targeted questions to resolve ambiguities in the spec and encode answers into the spec.
- Prompt: .github/prompts/speckit.clarify.prompt.md
- Agent: .github/agents/speckit.clarify.agent.md
- Prereqs:
  - Existing feature spec. Runs check-prerequisites.sh to locate FEATURE_DIR and FEATURE_SPEC.
- Inputs:
  - Optional context to guide what to focus on.
- Outputs (written):
  - Updates FEATURE_SPEC (adds Clarifications section and integrates resolutions into correct sections).
- Notes:
  - One question at a time; maximum 5 per session.
  - Should run before /speckit.plan when possible.

3) /speckit.plan
- Purpose: Create an implementation plan and design artifacts from the spec and constitution.
- Prompt: .github/prompts/speckit.plan.prompt.md
- Agent: .github/agents/speckit.plan.agent.md
- Prereqs:
  - setup-plan.sh; requires an existing spec and constitution.
- Outputs (written):
  - plan.md, research.md, data-model.md, contracts/, quickstart.md (per workflow)
- Handoffs:
  - /speckit.tasks (Create Tasks)
  - /speckit.checklist (Create Checklist)

4) /speckit.tasks
- Purpose: Generate an actionable tasks.md organized by phases and user stories.
- Prompt: .github/prompts/speckit.tasks.prompt.md
- Agent: .github/agents/speckit.tasks.agent.md
- Prereqs:
  - check-prerequisites.sh; typically needs plan.md and spec.md; may leverage data-model.md, contracts/, research.md, quickstart.md if present.
- Outputs (written):
  - tasks.md with strict checklist format (- [ ] T### ...)
- Handoffs:
  - /speckit.analyze (consistency analysis)
  - /speckit.implement (execute tasks)

5) /speckit.analyze
- Purpose: Read-only cross-artifact consistency and quality analysis across spec.md, plan.md, tasks.md.
- Prompt: .github/prompts/speckit.analyze.prompt.md
- Agent: .github/agents/speckit.analyze.agent.md
- Prereqs:
  - check-prerequisites.sh with --require-tasks; requires tasks.md.
- Outputs (console/report only):
  - Markdown analysis report (no file writes): inconsistencies, duplicates, coverage, constitution alignment, next actions.

6) /speckit.checklist
- Purpose: Generate a “unit tests for requirements” checklist for a chosen domain (e.g., api, security, performance, ux).
- Prompt: .github/prompts/speckit.checklist.prompt.md
- Agent: .github/agents/speckit.checklist.agent.md
- Prereqs:
  - check-prerequisites.sh; needs FEATURE_DIR; reads spec/plan/tasks for context.
- Outputs (written):
  - FEATURE_DIR/checklists/<domain>.md (creates a new file each run unless appending to existing domain file)
- Notes:
  - These test requirements quality, not implementation behavior.

7) /speckit.implement
- Purpose: Execute the implementation per tasks.md, performing repository changes and tracking progress.
- Prompt: (no separate prompt file; invoked via agent)
- Agent: .github/agents/speckit.implement.agent.md
- Prereqs:
  - check-prerequisites.sh with --require-tasks; reads tasks.md, plan.md, and optionally data-model.md, contracts/, research.md, quickstart.md.
  - May check checklist completion before proceeding.
- Outputs (written):
  - Code changes per tasks; updates checklist boxes in tasks.md as [X] when completed.
- Notes:
  - Enforces execution order and parallelization rules from tasks.md.

8) /speckit.constitution
- Purpose: Provide or reference the project constitution used as the non-negotiable guideline.
- Prompt: .github/prompts/speckit.constitution.prompt.md
- Agent: .github/agents/speckit.constitution.agent.md
- Outputs:
  - Read/echo of .specify/memory/constitution.md context (no writes expected).

9) /speckit.implement (aux) and other utilities
- Additional prompts exist mapping to the above workflows. If a prompt file is a stub (contains only agent: <name>), consult the corresponding agent.*.md for behavior.

10) /speckit.taskstoissues (if enabled)
- Purpose: Convert tasks in tasks.md to GitHub Issues (depends on automation environment).
- Prompt: .github/prompts/speckit.taskstoissues.prompt.md
- Agent: .github/agents/speckit.taskstoissues.agent.md (if present)
- Notes:
  - May require a token/permission in CI; consult your automation setup.

Recommended end-to-end flow
- Start: /speckit.specify → (optional) /speckit.clarify → /speckit.plan → /speckit.tasks → /speckit.analyze → /speckit.checklist (as needed) → /speckit.implement

Troubleshooting
- If a command errors about missing prerequisites, run the indicated previous command. The check-prerequisites.sh script outputs JSON with FEATURE_DIR and key paths; ensure it’s available and executable.
- When passing arguments with quotes, escape single quotes as 'I'\''m' or prefer double quotes: "I'm".

References
- Agents: .github/agents/
- Prompts: .github/prompts/
- Planning artifacts: specs/001-phase1-backend/
