from langchain_core.messages import HumanMessage, SystemMessage

from ..agent_state import AgentState
from services import llm_service
from ..prompts import ACTIONPLANNERSYSTEMPROMPT
from schemas.action_schema import ActionSchema


from utils import GLOBAL_LOGGER

def intent_parser_node(state: AgentState):
    logger = GLOBAL_LOGGER.bind(module='intent_parser_node')

    history = state.get("messages", [])

    user_text = state.get("user_input_text")

    if not user_text:
        logger.info('User input text is empty')
        raise ValueError("User input text is empty")
    
    new_user_msg = HumanMessage(content=user_text)

    llm = llm_service.llm.with_structured_output(ActionSchema)

    llm_messages = [
        SystemMessage(content=ACTIONPLANNERSYSTEMPROMPT),
        *history,
        new_user_msg
    ]

    result: ActionSchema = llm.invoke(llm_messages)

    if not result.action:
        logger.error('LLM failed to determine action')
        raise ValueError("LLM failed to determine action")

    logger.info('the user input is parsed successfully', extra={"actions":result.action})

    return {
        "messages": [new_user_msg],
        "action": result.action,
        "recipient_email": result.recipient_email,
        "datetime": result.datetime,
        "title": result.title,
        "description": result.description,
        "subject": result.subject,
        "body": result.body
    }


if __name__ == '__main__':
    state = AgentState()
    state['user_input_text'] = 'schedule an appointment for tommorow 4 oclock and inform ella@gmail.com about the appointement '
    intent_parser_node(state)