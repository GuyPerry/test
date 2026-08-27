# Hello Workshop Agent

Hello Workshop Agent — an interactive AI agent to greet, guide, and assist participants during workshops.

## Business challenge

Workshop facilitators and participants need a friendly, intelligent agent that can greet attendees, answer questions about the workshop agenda, provide guidance, and assist with common workshop interactions — reducing friction and improving the overall workshop experience.

## Key Milestones

1. **Participant Greeted** — Agent successfully greets a workshop participant by name or role.
2. **Question Answered** — Agent responds accurately to a participant's question about the workshop.
3. **Guidance Provided** — Agent delivers relevant workshop instructions or next steps.
4. **Session Completed** — Participant confirms their interaction with the agent was helpful.

## Business Architecture (RBA)

### End-to-End Process

Learning & Development / Workshop Facilitation

### Process Hierarchy

```
Corporate (Governance)
└── Learning & Development
    └── Workshop Facilitation
        └── Participant Onboarding
            └── Greet participants
            └── Provide agenda and instructions
        └── Knowledge Assistance
            └── Answer participant questions
            └── Guide through workshop activities
```

### Summary

The Hello Workshop Agent maps to the learning and development domain, specifically supporting workshop facilitation by automating participant greeting and guidance activities.

## Fit Gap Analysis

| Requirement (business) | Standard asset(s) found | API ORD ID | MCP Server ORD ID | MCP Server Version | Data Product ORD ID | Gap? | Notes / assumptions |
| ---------------------- | ----------------------- | ---------- | ----------------- | ------------------ | ------------------- | ---- | ------------------- |
| Greet workshop participants | No standard SAP product | — | — | — | — | Yes | Custom AI agent required |
| Answer workshop questions | No standard SAP product | — | — | — | — | Yes | LLM-based reasoning needed |
| Provide workshop guidance | No standard SAP product | — | — | — | — | Yes | Agent with context retention |
| Track participant interactions | No standard SAP product | — | — | — | — | Yes | Custom logic required |

### Key findings

- No standard SAP product covers workshop facilitation agent use cases out of the box.
- A pro-code Python AI agent is the most suitable approach for open-ended participant interaction.
- The agent will use LLM-based reasoning to handle dynamic participant questions.
- SAP AI Core will be used as the LLM runtime on SAP BTP.
- No external MCP servers are required for this use case.
- The solution is self-contained with no complex SAP system integrations needed.

## Recommendations

### Hello Workshop Agent — AI-Powered Workshop Assistant

#### Executive Summary

A lightweight AI agent that greets and guides workshop participants.

#### Recommended Solution

A pro-code Python AI agent deployed on SAP BTP using SAP AI Core as the LLM backbone. The agent greets participants, answers questions about the workshop, and provides step-by-step guidance throughout the session.

#### Recommended solution category

AI Agent

#### Intent fit
90%
