from workflows.agent_state import AgentState


def validation_node(state: AgentState):

    action = state.get("action")

    if action == "CREATE_EVENT_AND_SEND_EMAIL":

        required = ["recipient_email", "datetime", "title","subject", "body"]

    elif action == "CREATE_EVENT_ONLY":

        required = ["datetime", "title"]

    elif action == "SEND_EMAIL_ONLY":

        required = ["recipient_email", "subject", "body"]

    else:
        return {"error": "Unknown action"}

    missing = [field for field in required if not state.get(field)]
    final_missing = ','.join(missing)

    if missing:
        return {"error": f"Missing fields: {final_missing}"}

    return {}