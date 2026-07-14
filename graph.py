from langgraph.graph import StateGraph, END
from typing import TypedDict

from agents import (
    triage_agent,
    booking_specialist
)

from tools import get_all_bookings

from langgraph.checkpoint.sqlite import SqliteSaver


# ============================
# STATE DEFINITION
# ============================

class SchedulerState(TypedDict):
    message: str
    response: str
    route: str



# ============================
# AGENT NODES
# ============================

def triage_node(state):

    result = triage_agent(
        state["message"]
    )

    state["route"] = result["route"]

    return state



def booking_node(state):

    response = booking_specialist(
        state["message"]
    )

    state["response"] = response

    return state



def general_node(state):

    state["response"] = (
        "Hello 👋\n\n"
        "I am SchedulAI 🤖\n\n"
        "I can help you:\n"
        "• Check available slots\n"
        "• Book appointments\n"
        "• Manage previous bookings"
    )

    return state



def history_node(state):

    bookings = get_all_bookings()


    if not bookings:

        state["response"] = (
            "📭 No previous bookings found."
        )


    else:

        latest = bookings[-1]


        state["response"] = (
            "📅 Previous Booking Found\n\n"
            f"Date: {latest['date']}\n"
            f"Time: {latest['time']}\n"
            f"Email: {latest['email']}"
        )


    return state



# ============================
# LANGGRAPH WORKFLOW
# ============================


workflow = StateGraph(
    SchedulerState
)



workflow.add_node(
    "triage",
    triage_node
)


workflow.add_node(
    "booking",
    booking_node
)


workflow.add_node(
    "general",
    general_node
)


workflow.add_node(
    "history",
    history_node
)



workflow.set_entry_point(
    "triage"
)



def route_logic(state):

    message = state["message"].lower()


    if "previous" in message or "history" in message:
        return "history"


    return state["route"]



workflow.add_conditional_edges(
    "triage",
    route_logic,
    {
        "booking": "booking",
        "general": "general",
        "history": "history"
    }
)



workflow.add_edge(
    "booking",
    END
)


workflow.add_edge(
    "general",
    END
)


workflow.add_edge(
    "history",
    END
)



# ============================
# SQLITE MEMORY
# ============================


memory_connection = sqlite3 = SqliteSaver.from_conn_string(
    "scheduler_memory.db"
)


scheduler_graph = workflow.compile()



# ============================
# RUN FUNCTION
# ============================


def run_scheduler(message, thread_id):

    result = scheduler_graph.invoke(

        {
            "message": message,
            "response": "",
            "route": ""
        },

        config={
            "configurable": {
                "thread_id": thread_id
            }
        }

    )

    return result["response"]