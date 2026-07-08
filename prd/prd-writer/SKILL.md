---
name: prd-writer
description: Write Product Requirements Documents (PRDs) and Technical Design Documents (TDDs). Use this skill whenever the user explicitly asks to write a PRD or TDD, or asks to document requirements for a project. PRDs are written as zero-ambiguity Markdown files designed to drive autonomous Claude Code CLI execution. Always use this skill — never wing it — when producing any PRD or TDD artifact.
---

# PRD Writer

PRDs here are **executable specifications**, not traditional product docs. The target reader is Claude Code CLI running in one-shot autonomous mode (`--permission-mode auto`). Every requirement must be unambiguous enough that an AI agent can implement it without follow-up questions.

---

## Output Format

- **File**: `PRD.md` (Markdown, delivered as a downloadable file)
- **Tone**: Direct, precise, imperative voice ("The system shall...", "Claude Code must...")
- **Length**: As long as necessary for zero ambiguity — never truncate for brevity
- **No placeholders**: Every section must be fully populated. If something is unknown, flag it explicitly as `⚠️ OPEN QUESTION:` to resolve before running Claude Code.

---

## Required Sections (in order)

### 1. Overview / Executive Summary
- What is being built, for whom, and why
- The core value proposition in 2–4 sentences
- Deployment target (e.g., AWS us-west-2, Azure, local)
- Primary persona / end user

### 2. Goals & Non-Goals
**Goals**: Bulleted list of what success looks like — measurable where possible.
**Non-Goals**: Explicit list of what is out of scope. This is as important as Goals — it prevents Claude Code from over-building.

### 3. User Stories / Personas
- Define 1–3 primary personas with role, context, and motivation
- Write user stories in `As a [persona], I want to [action] so that [outcome]` format
- Include acceptance criteria for each story

### 4. Functional Requirements
This is the most critical section. Write at the level of **individual behaviors**, not features.

Rules:
- Number every requirement (FR-001, FR-002, etc.)
- Each requirement = one atomic, testable behavior
- Use imperative: "The application shall...", "When X occurs, the system must..."
- Include error states, edge cases, and empty states explicitly
- If a UI component is involved, describe its exact behavior (validation rules, disabled states, loading states)
- No vague language: never use "appropriate", "reasonable", "as needed", "etc."

### 5. Technical Requirements / Stack
Always pre-populate the standard stack below and flag any deviations:

**Frontend**
- Vue 3 + TypeScript (Composition API, `<script setup>`)
- Vuetify 3 (Material Design component library)
- Pinia for state management
- Vue Router for navigation

**Backend / Infrastructure**
- AWS CDK (TypeScript) for all infrastructure-as-code
- Node.js Lambda functions (TypeScript) or Python Lambda, depending on context
- API Gateway (REST or HTTP API — specify which)
- DynamoDB or S3 (specify access patterns)
- Amazon S3 Vectors for vector storage if RAG is involved (not OpenSearch Serverless)

**AI / LLM**
- Amazon Bedrock — Claude via **inference profiles only** (never direct model IDs, never direct Anthropic API)
- Default inference profile: `us.anthropic.claude-sonnet-4-5` (or specify if different)
- Bedrock Knowledge Bases if RAG is required

**Deviations**: If the project uses a different stack (e.g., Azure, Python frontend, different LLM), call it out explicitly with `⚠️ DEVIATION:` and explain why.

### 6. API / Data Model
- Define all API endpoints: method, path, request shape, response shape, error codes
- Define all data models / DynamoDB schemas: partition key, sort key, attributes, access patterns
- Use TypeScript interface syntax for type definitions
- Include any external APIs being called (auth, format, rate limits)

### 7. UI/UX Notes
- Describe key screens / views and their layout intent
- Call out any specific Vuetify components to use
- Note any loading/skeleton states, empty states, or error states that must be handled
- If a design mockup or wireframe exists, reference it; otherwise describe the layout in plain language

### 8. CI/CD & Quality Gates
Always include these five non-negotiable standards — no exceptions:

1. **Linting**: ESLint configured and passing with zero errors (`npm run lint`)
2. **Test Coverage**: Minimum 80% coverage with 100% of tests passing (`npm run test`)
3. **TypeScript Strict**: `tsc --noEmit` passes with zero errors (strict mode enabled)
4. **GitHub Actions**: CI pipeline configured — runs lint, type-check, and tests on every push/PR
5. **Bedrock Inference Profiles**: All Claude API calls use Bedrock inference profiles — never direct model IDs, never direct Anthropic API keys in deployed code

### 9. Out of Scope
Explicit list of features, integrations, or behaviors that are **not** being built in this version. This is Claude Code's guardrail — it prevents scope creep during autonomous execution.

---

## TDD (Technical Design Document) Mode

When the user asks for a TDD instead of (or in addition to) a PRD:

- Add a **System Architecture** section with a component diagram described in text (or Mermaid if helpful)
- Add a **Sequence Diagrams** section for the 2–3 most complex flows
- Expand the API / Data Model section with implementation notes (not just contracts)
- Add an **Infrastructure Diagram** section describing the CDK stack topology
- Add a **Security Considerations** section (IAM roles, least privilege, secrets management)

---

## Before Writing: Clarify First

If the request is missing critical information, ask before writing — don't assume:

- What is the deployment target / cloud provider?
- Who is the end user (internal team, client demo, production)?
- Does it use AI/LLM features? If so, what model and use case?
- Is there an existing codebase to extend, or greenfield?
- What is the timeline / MVP scope?

If context is already in the conversation or in memory, use it — don't ask redundant questions.

---

## Quality Check Before Delivering

Before presenting the PRD file, verify:

- [ ] Every section is fully populated (no `TBD` unless flagged as `⚠️ OPEN QUESTION`)
- [ ] Functional requirements are numbered and atomic
- [ ] Stack section reflects the defaults above or flags deviations
- [ ] All 5 CI/CD quality gates are present
- [ ] No vague language remains
- [ ] Out of Scope section prevents obvious over-building
