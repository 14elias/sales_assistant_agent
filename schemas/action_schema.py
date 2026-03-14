from pydantic import BaseModel, Field
from typing import Optional, Literal


class ActionSchema(BaseModel):
    action: Literal[
        "CREATE_EVENT_AND_SEND_EMAIL",
        "CREATE_EVENT_ONLY",
        "SEND_EMAIL_ONLY",
        "GREETINGS"
    ]

    recipient_email: Optional[str] = None
    datetime: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None

    subject: Optional[str] = None
    body: Optional[str] = None