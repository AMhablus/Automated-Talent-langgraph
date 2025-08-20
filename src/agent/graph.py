from langgraph.graph import START, StateGraph, END
from IPython.display import Image, display
from src.agent.nodes import prescreening_analysis, skills_analysis, router1, router2, interview, phone_screen, reject
from src.agent.state import SharedState


builder = StateGraph(SharedState)


builder.add_node("prescreening_analysis", prescreening_analysis)
builder.add_node("skills_analysis", skills_analysis)
builder.add_node("interview", interview)
builder.add_node("phone_screen", phone_screen)
builder.add_node("reject", reject)  

builder.add_edge(START, "prescreening_analysis")
builder.add_conditional_edges("prescreening_analysis", router1, {
    "skills_analysis": "skills_analysis",
    "reject": "reject"
})
builder.add_conditional_edges("skills_analysis", router2, {
    "Interview": "interview",
    "Phone Screen": "phone_screen",
    "Rejected": "reject"
})
builder.add_edge("reject", END)
builder.add_edge("interview", END)
builder.add_edge("phone_screen", END)
graph = builder.compile()


display(Image(graph.get_graph().draw_mermaid_png()))