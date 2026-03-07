from services.llm_service import llm
from prompts import RESPONSESYSTEMPROMPT


def response_node(state):
    """
    Generates a natural response describing the result of the workflow.
    """

    summary_data = {
        "action": state.get("action"),
        "recipient_email": state.get("recipient_email"),
        "datetime": state.get("datetime"),
        "title": state.get("title"),
        "description": state.get("description"),
        "error": state.get("error"),
        "calendar_event": state.get("calendar_event_result"),
        "email_result": state.get("email_result"),
    }

    messages = [
        {"role": "system", "content": RESPONSESYSTEMPROMPT},
        {
            "role": "user",
            "content": f"Task result data: {summary_data}"
        }
    ]

    result = llm.invoke(messages)

    return {
        "response": result.content
    }