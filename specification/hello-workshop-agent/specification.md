# Specification: hello-workshop-agent

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-agent.md](../guidelines-agent.md) — Universal agent patterns
> - [guidelines-agent-python.md](../guidelines-agent-python.md) — Python implementation details
> - [guidelines-agent-skills.md](../guidelines-agent-skills.md) — Runtime skills patterns
> - [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) — MCP integration patterns

---

## Basic Setup

- [x] Read the project input (`product-requirements-document.md`, `intent.md`)
- [x] Bootstrap agent code in `assets/hello-workshop-agent/` using skill `sap-agent-bootstrap` (invoke from inside `assets/hello-workshop-agent/`, use copy commands — do NOT create files manually)
- [x] Install dependencies, validate the agent starts and responds at `/.well-known/agent.json`

---

## Runtime Skills

- [x] Create `assets/hello-workshop-agent/app/skills/workshop-guidance/SKILL.md` with:
  - YAML frontmatter: `name: workshop-guidance`, `description: Guides workshop participants through activities, answers questions, and provides step-by-step instructions`
  - Body: Instructions for greeting participants, answering workshop questions, providing agenda guidance, and escalating to facilitator when confidence is low
- [x] Delete the template runtime skill: `rm -rf assets/hello-workshop-agent/app/skills/template-skill/`

---

## Project-Specific Tasks

## Agent System Prompt

- [x] Update the agent system prompt in `assets/hello-workshop-agent/app/agent.py` (`@prompt_section`) to:
  - Identify the agent as a friendly workshop assistant named "Hello Workshop Agent"
  - Instruct the agent to greet participants warmly, by name or role when provided
  - Instruct the agent to answer workshop-related questions clearly and concisely
  - Instruct the agent to provide step-by-step guidance for workshop activities
  - Instruct the agent to escalate to the facilitator if it cannot answer confidently
  - Instruct the agent to never fabricate information — only respond based on what is known

## Greeting Capability (R1)

- [x] Implement a `greet_participant` tool in `assets/hello-workshop-agent/app/tools.py` (or equivalent tool file) that:
  - Accepts participant name and/or role as input
  - Returns a warm, personalized greeting message
  - Logs `M1.achieved: participant greeted successfully` on success
  - Logs `M1.missed: participant greeting did not complete` on failure
- [x] Register the tool with the agent graph

## Question & Answer Capability (R2)

- [x] Implement a `answer_question` tool that:
  - Accepts a participant question as input
  - Uses the workshop guidance skill to formulate an answer
  - Returns the answer or escalates to facilitator if confidence is low
  - Logs `M2.achieved: participant question answered` on success
  - Logs `M2.missed: question could not be answered, escalating` on miss
- [x] Register the tool with the agent graph

## Workshop Navigation Guidance (R3)

- [x] Implement a `provide_guidance` tool that:
  - Accepts a request for next steps or instructions
  - Returns contextual workshop guidance (e.g., current activity instructions, what comes next)
  - Logs `M3.achieved: workshop guidance provided` on success
  - Logs `M3.missed: guidance step not completed` on miss
- [x] Register the tool with the agent graph

## Session Completion (M4)

- [x] Implement session completion tracking:
  - When a participant signals end of session or satisfaction, log `M4.achieved: workshop session completed successfully`
  - If session ends abruptly (no confirmation), log `M4.missed: session ended without completion confirmation`

---

## Business Instrumentation

- [x] Implement business step instrumentation for each milestone (M1–M4) from the PRD: structured logging with pattern `[MILESTONE_ID].[achieved|missed]: [description]` and OpenTelemetry custom spans. See [guidelines-agent-python.md](../guidelines-agent-python.md) for Python-specific implementation.
- [x] Verify `auto_instrument()` is called at top of `main.py` before any AI framework imports

---

## MCP Tool Integration

> No SAP backend MCP integration required for this agent. Skip Path A and Path B.
> No `mcp-mock.json` generation needed (no MCP tools used).

---

## Testing

- [x] `conftest.py` only sets `IBD_TESTING=true`
- [x] Write unit tests in `assets/hello-workshop-agent/tests/`:
  - `test_greet_participant.py` — test the greeting tool
  - `test_answer_question.py` — test the Q&A tool
  - `test_provide_guidance.py` — test the guidance tool
- [x] Write one integration test executing end-to-end agent flow with mocked LLM responses
- [x] Run `pytest` from `assets/hello-workshop-agent/` — 38/38 tests passed
- [x] Verify `assets/hello-workshop-agent/app/agent.py` has exactly 5 decorated functions (confirmed: 5)
- [x] Run `pytest` again (no args) to generate final `test_report.json`
- [x] Verify `test_report.json` exists in `assets/hello-workshop-agent/`
