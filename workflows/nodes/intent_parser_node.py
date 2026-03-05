from workflows.agent_state import AgentState
from ...services import llm_service
from ..prompts import ACTIONPLANNERSYSTEMPROMPT
from ...schemas.action_schema import ActionSchema


def intent_parser_node(state: AgentState):

    llm = llm_service.llm.with_structured_output(ActionSchema)

    if not state["user_input_text"]:
        raise ValueError("User input text is empty")

    messages = [
        {
            "role": "system",
            "content": ACTIONPLANNERSYSTEMPROMPT
        },
        {
            "role": "user",
            "content": state["user_input_text"]
        }
    ]

    result: ActionSchema = llm.invoke(messages)

    if not result.action:
        raise ValueError("LLM failed to determine action")

    return {
        "action": result.action,
        "recipient_email": result.recipient_email,
        "datetime": result.datetime,
        "title": result.title,
        "description": result.description,
        "subject": result.subject,
        "body": result.body
    }