# Product Requirements Document (PRD)

**Title:** Hello Workshop Agent  
**Date:** 2026-08-16  
**Owner:** Workshop Facilitator  
**Solution Category:** AI Agent

## Product Purpose & Value Proposition

**Elevator Pitch:**  
A friendly AI agent that greets workshop participants, answers their questions, and guides them through the workshop — so facilitators can focus on content delivery instead of repetitive logistics.

**Expected Value:**  
Reduces facilitator overhead for common participant questioens; improves participant experience from the first interaction.

**Product Objectives:**
1. Greet workshop participants warmly and accurately.
2. Answer participant questions about the workshop agenda and activities.
3. Provide step-by-step guidance throughout the workshop session.

## Requirements

### Must-Have Requirements

**R1**: Participant Greeting

- **User Story**: As a workshop participant, I need the agent to greet me so that I feel welcomed and oriented.
- **Acceptance Criteria**: Given a participant initiates a session, when they introduce themselves, then the agent greets them by name or role.
- **Priority Rank**: 1

**R2**: Question & Answer

- **User Story**: As a workshop participant, I need to ask the agent questions so that I can get instant answers without interrupting the facilitator.
- **Acceptance Criteria**: Given a participant asks a question, when the agent processes it, then a relevant and accurate answer is returned.
- **Priority Rank**: 2

**R3**: Guided Workshop Navigation

- **User Story**: As a participant, I need the agent to provide instructions and next steps so that I can follow along with the workshop without confusion.
- **Acceptance Criteria**: Given a participant requests guidance, when the agent responds, then it provides clear and contextual next steps.
- **Priority Rank**: 3

## Solution Architecture

**Architecture Overview:**  
A pro-code Python AI agent running on SAP BTP, powered by SAP AI Core as the LLM runtime. The agent exposes a conversational interface, maintains session context, and responds to participant inputs.

**Key Components:**

- **AI Agent (Python)**: Core agent logic using A2A protocol, handles greetings, Q&A, and guidance.
- **SAP AI Core**: LLM runtime (GPT-4o via SAP Generative AI Hub).
- **Session Context Store**: In-memory context to retain participant session state.

### Agent Extensibility & Instrumentation

**Agent Extensibility:**
- The agent is designed with extension points to allow additional workshop topics, FAQ content, or integrations to be added in the future without restructuring the core logic.

**Business Step Instrumentation:**
- All key business steps are instrumented with structured log statements following the pattern: `[MILESTONE_ID].[achieved|missed]: [description]`
- Enables production monitoring and debugging of agent behavior.

### Automation & Agent Behaviour

**Automation Level:** Autonomous agent

**Actions the system performs without human approval:**
- Greeting participants
- Answering workshop questions
- Providing workshop guidance and next steps

**Actions that require human review:**
- Escalation to facilitator if the agent cannot answer a question confidently

**Model used:** GPT-4o via SAP Generative AI Hub (SAP AI Core)

**Guardrails & fail-safes:**
- If confidence is below threshold, escalate to facilitator.
- Agent only answers questions within the workshop scope.
- No personal data is stored beyond the active session.

## Milestones

### M1: Participant Greeted

- **Description**: The agent successfully greeted a workshop participant.
- **Achieved when**: Agent sends a greeting message to the participant.
- **Log on achievement**: `M1.achieved: participant greeted successfully`
- **Log on miss**: `M1.missed: participant greeting did not complete`

### M2: Question Answered

- **Description**: The agent answered a participant's question.
- **Achieved when**: Agent returns a response to a participant question.
- **Log on achievement**: `M2.achieved: participant question answered`
- **Log on miss**: `M2.missed: question could not be answered, escalating`

### M3: Guidance Provided

- **Description**: The agent delivered workshop instructions or next steps.
- **Achieved when**: Agent sends guidance content to a participant.
- **Log on achievement**: `M3.achieved: workshop guidance provided`
- **Log on miss**: `M3.missed: guidance step not completed`

### M4: Session Completed

- **Description**: Participant confirmed their interaction was helpful.
- **Achieved when**: Participant ends the session or confirms satisfaction.
- **Log on achievement**: `M4.achieved: workshop session completed successfully`
- **Log on miss**: `M4.missed: session ended without completion confirmation`
