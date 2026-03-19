from workflows.agent_state import AgentState
from services.email_service import email_service

from utils import GLOBAL_LOGGER
from utils.logger_config import CustomLogger


# …existing code…

def email_node(state: AgentState):
    logger = GLOBAL_LOGGER.bind(module='email_node')

    action = state.get("action", "")
    # return unless action is one of the expected ones
    if action not in ("CREATE_EVENT_AND_SEND_EMAIL", "SEND_EMAIL_ONLY"):
        return state
    
    try:

        email_service.send_email(
            recipient=state.get("recipient_email"),
            subject=state.get("subject", "Appointment Scheduled"),
            body=state.get("body", f"You have an appointment at {state.get('datetime')}")
        )

        logger.info('email sent successfully', extra={"email": state.get("subject", "Appointment Scheduled")})

        return {"email_result": "email sent success fully "}
    except Exception as e:
        logger.error('email sent failed', error=e)
        state["email_result"] = 'email sent failed'
        return {"error":e}

    

# …existing code…


if __name__ == '__main__':
    state = AgentState()
    state["action"] = "CREATE_EVENT_AND_SEND_EMAIL"
    state["recipient_email"]='ellamebrahtom1995@gmail.com'
    state['datetime'] = 'tommorow 4 oclock'
    email_node(state)



