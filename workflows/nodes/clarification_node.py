from workflows.agent_state import AgentState
from ..prompts import CLARIFICATIONSYSTEMPRMPT
from services.llm_service import llm


def clarification_node(state: AgentState) -> AgentState:
    """
    Handles missing required information by requesting clarification
    from the user.

    Trigger Condition:
        Executed when `state["missing_fields"]` is not empty.

    Behavior:
        - Identifies which required fields are missing.
        - Generates a natural-language clarification question.
        - Waits for user response.
        - Updates `parsed_action` with new information.
        - Clears missing_fields when resolved.

    Example:
        If `datetime` is missing, the system may ask:
        "What time should I schedule the meeting?"

    Returns:
        Updated AgentState with new information filled in.

    Important:
        This node does not call external APIs.
        It only resolves incomplete input before execution proceeds.
    """

    missing_fields = state.get('error')
    if not missing_fields:
        raise ValueError('there is no missing fields')
    
    messages = [
        {
            "role": "system",
            "content": CLARIFICATIONSYSTEMPRMPT
        },
        {
            "role": "user",
            "content": missing_fields
        }
    ]
    result = llm.invoke(messages)

    return result.content


if __name__ == '__main__':
    state = AgentState()
    state['error'] = "missing fields: recipient_email, title"
    result = clarification_node(state)
    print(result)