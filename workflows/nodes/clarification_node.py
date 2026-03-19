from workflows.agent_state import AgentState
from ..prompts import CLARIFICATIONSYSTEMPRMPT
from services.llm_service import llm
from utils.logger_config import CustomLogger
from utils import GLOBAL_LOGGER


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

    logger = GLOBAL_LOGGER.bind("clarification_node")

    missing_fields = state.get('missing_fields')
    if not missing_fields:
        logger.error('error there is no missing field')
        raise ValueError('there is no missing fields')
    
    logger.info('missing fields:', missing_fields=missing_fields)

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

    logger.info('the question from the llm to the user about the missing fields',extra={"respone": result.content})

    return {"agent_response" : result.content}


if __name__ == '__main__':
    state = AgentState()
    state['error'] = "missing fields: recipient_email, title"
    result = clarification_node(state)
    print(result)