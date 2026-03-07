from workflows.agent_state import AgentState
from services.calendar_service import service

from workflows.agent_state import AgentState
from services.calendar_service import service

def calendar_node(state: AgentState):
    action = state.get('action')

    if action not in ("CREATE_EVENT_AND_SEND_EMAIL", "SEND_EMAIL"):
        return state

    # use get() so missing keys don’t raise
    title = state.get("title", "Appointment")
    description = state.get("description", "")
    datetime_str = state.get("datetime")  # you might want to validate this separately

    event = service.create_event(
        title=title,
        description=description,
        datetime_str=datetime_str
    )

    state["event"] = event

    return state


if __name__ == '__main__':
    state = AgentState()
    state['action'] = "CREATE_EVENT_AND_SEND_EMAIL"
    state["datetime"] = 'today 4 oclock'
    # title/description are optional now – the defaults will be used
    calendar_node(state)
    print('success – created', state.get("event"))