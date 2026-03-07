from typing import TypedDict, Optional, List, Dict, Any


class AgentState(TypedDict):
    """
    Shared state object passed between all graph nodes.

    This state represents the full lifecycle of a single user request.
    Each node reads from and writes to this structure.

    Fields:
        system_prompt:
            The base instruction that controls LLM behavior.

        user_input_voice:
            Raw audio bytes received from the user (if voice input is used).

        user_input_text:
            Transcribed or directly provided text instruction.

        parsed_action:
            Structured JSON output returned by the LLM.
            Contains extracted fields such as action type, datetime,
            recipient email, title, and description.

        missing_fields:
            List of required fields not yet provided by the user.
            Used to trigger clarification logic.

        calendar_event_result:
            Response returned from Google Calendar API
            after successful event creation.

        email_result:
            Response returned from Gmail API
            after successful email delivery.

        error:
            Contains error message if any node fails.
            If populated, the workflow should terminate gracefully.
    """
    
    system_prompt: str

    user_input_voice: Optional[bytes]
    user_input_text: Optional[str]

    action: Optional[str]

    recipient_email: Optional[str]
    datetime: Optional[str]
    title: Optional[str]
    description: Optional[str]

    subject: Optional[str]
    body: Optional[str]

    missing_fields: List[str]

    calendar_event_result: Optional[dict]
    email_result: Optional[dict]

    error: Optional[str]



