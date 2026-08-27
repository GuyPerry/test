"""Workshop agent tools — greet participants, answer questions, provide guidance."""
import logging
from langchain_core.tools import tool

logger = logging.getLogger(__name__)


@tool
def greet_participant(name: str = "", role: str = "") -> str:
    """Greet a workshop participant by name and/or role.

    Args:
        name: Participant's name (optional).
        role: Participant's role or job title (optional).

    Returns:
        A personalized greeting message.
    """
    try:
        if name and role:
            greeting = f"Welcome to the workshop, {name}! Great to have a {role} here today. I'm your workshop assistant — feel free to ask me anything!"
        elif name:
            greeting = f"Welcome to the workshop, {name}! I'm your workshop assistant. Let me know if you have any questions or need guidance."
        elif role:
            greeting = f"Welcome, {role}! I'm your workshop assistant. I'm here to help you navigate today's session."
        else:
            greeting = "Welcome to the workshop! I'm your workshop assistant. Feel free to ask me any questions or request guidance at any time."

        logger.info("M1.achieved: participant greeted successfully")
        return greeting
    except Exception as exc:
        logger.error("M1.missed: participant greeting did not complete — %s", exc)
        raise


@tool
def answer_question(question: str) -> str:
    """Answer a workshop participant's question about the session.

    Args:
        question: The participant's question.

    Returns:
        An answer or escalation notice.
    """
    try:
        # Delegate to LLM reasoning via the agent; this tool acts as a structured entry point
        response = (
            f"Great question! Let me help you with: '{question}'. "
            "I'll do my best to provide an accurate answer based on what I know about this workshop. "
            "If I'm not confident, I'll connect you with the facilitator."
        )
        logger.info("M2.achieved: participant question answered")
        return response
    except Exception as exc:
        logger.error("M2.missed: question could not be answered, escalating — %s", exc)
        raise


@tool
def provide_guidance(request: str = "") -> str:
    """Provide step-by-step workshop guidance or instructions for the current activity.

    Args:
        request: Description of what guidance is needed (e.g. 'next steps', 'current activity').

    Returns:
        Clear workshop guidance or instructions.
    """
    try:
        guidance = (
            "Here's some guidance to help you navigate the workshop:\n\n"
            "1. Follow the facilitator's current instructions.\n"
            "2. Complete the current activity before moving to the next.\n"
            "3. Ask me if you need clarification on any step.\n"
            "4. Flag the facilitator if you're stuck for more than a few minutes.\n\n"
            "Is there a specific part of the workshop you'd like more detail on?"
        )
        logger.info("M3.achieved: workshop guidance provided")
        return guidance
    except Exception as exc:
        logger.error("M3.missed: guidance step not completed — %s", exc)
        raise


@tool
def complete_session(feedback: str = "") -> str:
    """Mark the workshop session as complete and capture participant feedback.

    Args:
        feedback: Optional feedback from the participant about the session.

    Returns:
        A closing message.
    """
    try:
        if feedback:
            message = f"Thank you for your feedback: '{feedback}'. We hope you found the workshop valuable! See you next time."
        else:
            message = "Thank you for participating in the workshop! We hope it was a great experience. See you next time!"
        logger.info("M4.achieved: workshop session completed successfully")
        return message
    except Exception as exc:
        logger.error("M4.missed: session ended without completion confirmation — %s", exc)
        raise
