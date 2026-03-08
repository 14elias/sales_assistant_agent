from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, SystemMessage
from .agent_state import AgentState
from nodes import (
    email_node,
    clarification_node,
    intent_parser_node,
    calendar_node,
    response_node,
    validation_node,
)




class SchedulingGraph:
    """
    Graph orchestrator responsible for coordinating the
    end-to-end workflow of the AI scheduling assistant.

    Responsibilities:
        - Register graph nodes
        - Define state transitions
        - Enforce execution order
        - Handle conditional branching

    Execution Flow:
        1. Convert speech to text (optional)
        2. Parse user intent using LLM
        3. Validate required fields
        4. Request clarification if necessary
        5. Create calendar event
        6. Send confirmation email
        7. Generate final response

    Design Principles:
        - Deterministic execution
        - LLM used only for reasoning, not tool execution
        - Calendar event must succeed before email is sent
        - Email retries up to 3 times before failure response

    This class builds and compiles the LangGraph workflow.
    """
    
    def __init__(self, state: AgentState, model):
        self.state = state
        self.memory = MemorySaver()
    
    def build(self):
        def validation_router(state):

            if state.get("error"):
                return "clarification"

            return "calendar"
        
        builder = StateGraph(AgentState)

        builder.add_node("intent_parser", intent_parser_node)

        builder.add_node("validation", validation_node)

        builder.add_node("clarification", clarification_node)

        builder.add_node("calendar", calendar_node)

        builder.add_node("email", email_node)

        builder.add_node("response", response_node)

        #building the edges

        builder.set_entry_point("intent_parser")

        builder.add_edge("intent_parser", "validation")

        builder.add_conditional_edges(
            "validation",
            validation_router,
            {
                "clarification": "clarification",
                "calendar": "calendar"
            }
        )

        builder.add_edge("clarification", "intent_parser")

        builder.add_edge("calendar", "email")

        builder.add_edge("email", "response")

        builder.add_edge("response", END)

        graph = builder.compile(
            checkpointer=self.memory,
            interrupt_before=["clarification"]
        )

        return graph
    
scheduling_graph =SchedulingGraph()
graph = scheduling_graph.build()

if __name__ == "__main__":
    state = AgentState()
    workflow = SchedulingGraph(state)

    graph = workflow.build()
    
    result = graph.invoke(
        {
            "user_input_text": "schedule meeting tomorrow at 3pm"
        }
    )
