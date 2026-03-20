---
description: Create a concrete unit testing skill by inferring the target language, testing stack, and framework/domain context from the user request, selected context, and workspace.
argument-hint: Describe the target language, testing stack, build tool, layout, and optional domain/framework.
---

# Creating a Custom Unit Testing Skill

1. Review `AGENTS.md` and `unit-testing-skill-creator` skill before drafting a new unit testing skill.
2. If the editor selection contains an example block, treat it as the highest-priority source for conventions and defaults.
3. Infer as much context as possible from the user request, selected content, existing test files, the current workspace, and the surrounding codebase.
4. Derive concrete details from repository signals such as language files, build files, dependency manifests, and project layout.
5. Do not ask for information that can be inferred from the workspace or selected context. Ask the user only for missing information that would materially change the generated skill.
6. Infer the destination path from repository conventions, such as `.copilot/skills/`, `skills/`, or other equivalent directories.
7. Before creating the skill, present all resolved input values (per the `unit-testing-skill-creator` Inputs table) and the destination path for the user to confirm.
8. If the user does not confirm, clarify what is missing or incorrect, then re-infer as needed.
9. Create a concrete unit testing skill by calling `unit-testing-skill-creator` skill and output the result along with a brief summary of the inferred assumptions.
