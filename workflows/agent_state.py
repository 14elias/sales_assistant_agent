from typing import TypedDict, Optional, List, Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):

    messages: Annotated[Sequence[BaseMessage], add_messages]

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


    # agent message
    agent_response: Optional[str]

    # tool results
    calendar_event_result: Optional[dict]
    email_result: Optional[dict]

    # workflow status
    status: Optional[str]

    # error handling
    error: Optional[str]



