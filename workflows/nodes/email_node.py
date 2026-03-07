from workflows.agent_state import AgentState
from services.email_service import email_service


# …existing code…

def email_node(state: AgentState):

    action = state.get("action", "")
    # return unless action is one of the expected ones
    if action not in ("CREATE_EVENT_AND_SEND_EMAIL", "SEND_EMAIL"):
        return state

    email_service.send_email(
        recipient=state.get("recipient_email"),
        subject=state.get("subject", "Appointment Scheduled"),
        body=state.get("body", f"You have an appointment at {state.get('datetime')}")
    )

    return state

# …existing code…


if __name__ == '__main__':
    state = AgentState()
    state["action"] = "CREATE_EVENT_AND_SEND_EMAIL"
    state["recipient_email"]='ellamebrahtom1995@gmail.com'
    state['datetime'] = 'tommorow 4 oclock'
    email_node(state)



