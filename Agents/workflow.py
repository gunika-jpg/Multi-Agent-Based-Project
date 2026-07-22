from langgraph.graph import StateGraph, START, END

from Agents.graph_state import ProductComparisonState
from Agents.search_agent import search_agent_node
from Agents.comparison_agent import comparison_agent
from Agents.recommendation_agent import recommendation_agent
from Agents.response_agent import response_agent


def build_graph():
    graph = StateGraph(ProductComparisonState)

    graph.add_node("search", search_agent_node)
    graph.add_node("comparison", comparison_agent)
    graph.add_node("recommendation", recommendation_agent)
    graph.add_node("response", response_agent)

    graph.add_edge(START, "search")
    graph.add_edge("search", "comparison")
    graph.add_edge("comparison", "recommendation")
    graph.add_edge("recommendation", "response")
    graph.add_edge("response", END)

    return graph.compile()


# Compiled once at import time, reused for every request
compiled_graph = build_graph()


def run_pipeline(query: str, budget: float = 0, brand_filter: str = "", weights: dict = None) -> dict:
    """
    Main entry point for the Streamlit frontend (Member 5):

        from Agents.workflow import run_pipeline
        result = run_pipeline("wireless earbuds", budget=3000, brand_filter="boAt")
        st.markdown(result["final_response"])
        st.write(result["recommendations"])
        st.write(result["comparison_data"])
    """
    initial_state = {
        "query": query,
        "budget": budget,
        "brand_filter": brand_filter,
        "weights": weights or {},
        "products": [],
        "comparison_data": {},
        "recommendations": [],
        "agent_status": {
            "search": "pending",
            "comparison": "pending",
            "recommendation": "pending",
            "response": "pending",
        },
        "errors": [],
    }
    return compiled_graph.invoke(initial_state)


if __name__ == "__main__":
    result = run_pipeline("wireless earbuds", budget=3000)
    print("\n--- FINAL RESPONSE ---\n")
    print(result.get("final_response"))
    print("\n--- AGENT STATUS ---")
    print(result.get("agent_status"))
    if result.get("errors"):
        print("\n--- NOTES / ERRORS (non-fatal) ---")
        for e in result["errors"]:
            print(" -", e)
