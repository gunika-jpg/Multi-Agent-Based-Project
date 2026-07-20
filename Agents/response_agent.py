<<<<<<< HEAD
from Services.groq_service import GroqService


def response_agent(state):

    recommendations = state.get("recommendations", [])
    budget = state.get("budget", 0)

    if not recommendations:
        return {
            "ai_response": "No products found."
        }

    groq = GroqService()

    top_product = recommendations[0]
    alternatives = recommendations[1:]

    comparison = groq.generate_comparison_summary(
        recommendations,
        budget
    )

    response = groq.generate_recommendation(
        top_product,
        alternatives
    )

    return {
        "comparison_summary": comparison,
        "ai_response": response
    }
=======
"""
Response Agent — Member 1

Responsibility: take the ranked `recommendations` (from Member 4's
Recommendation Agent) and `comparison_data` (from the Comparison Agent) and
produce one clean markdown string — state["final_response"] — for the
frontend to display with st.markdown(...).

Uses Services/groq_service.py for a natural-language narrative when
GROQ_API_KEY is configured. Otherwise falls back to a deterministic summary
built from the score breakdowns the Recommendation Agent already computed
(the "why" field), so the app never breaks just because no LLM key is set.

Input state keys read:
    recommendations  : List[Dict]
    comparison_data  : Dict

Output state keys written:
    final_response : str
    agent_status   : Dict
"""
from typing import Any, Dict, List

from utils.logger import setup_logger
from utils.config import get_settings

logger = setup_logger("ResponseAgent")


def _deterministic_summary(top: Dict, alternatives: List[Dict], comparison_data: Dict) -> str:
    lines = [
        f"## {top.get('rank_label', 'Best pick')}: {top.get('name')}",
        f"**Price:** \u20b9{top.get('price', 0):,.0f}  |  "
        f"**Rating:** {top.get('rating')}\u2b50  |  **Source:** {top.get('source')}",
        f"\n{top.get('why', '')}",
    ]

    if comparison_data:
        cheapest = comparison_data.get("cheapest")
        highest_rated = comparison_data.get("highest_rated")
        if cheapest:
            lines.append(f"\n- Cheapest overall: {cheapest.get('name')} at \u20b9{cheapest.get('price', 0):,.0f}")
        if highest_rated:
            lines.append(f"- Highest rated: {highest_rated.get('name')} ({highest_rated.get('rating')}\u2b50)")

    if alternatives:
        lines.append("\n### Other good options")
        for alt in alternatives[:3]:
            lines.append(
                f"- {alt.get('name')} \u2014 \u20b9{alt.get('price', 0):,.0f} "
                f"({alt.get('rating')}\u2b50, {alt.get('source')})"
            )

    return "\n".join(lines)


def response_agent_node(state: Dict[str, Any]) -> Dict[str, Any]:
    recommendations = state.get("recommendations", [])
    comparison_data = state.get("comparison_data", {})
    errors = list(state.get("errors", []))
    agent_status = state.get("agent_status", {}).copy()
    agent_status["response"] = "running"

    if not recommendations:
        agent_status["response"] = "completed"
        return {
            "final_response": "No products matched your search. Try a different query, budget, or brand filter.",
            "agent_status": agent_status,
        }

    top, alternatives = recommendations[0], recommendations[1:]
    settings = get_settings()

    final_response = None
    if settings.GROQ_API_KEY:
        try:
            from Services.groq_service import GroqService
            from utils.validators import Product

            valid_fields = Product.model_fields
            top_product = Product(**{k: v for k, v in top.items() if k in valid_fields})
            alt_products = [
                Product(**{k: v for k, v in a.items() if k in valid_fields})
                for a in alternatives[:3]
            ]
            final_response = GroqService().generate_recommendation(top_product, alt_products)
            logger.info("Response Agent used Groq for narrative generation")
        except Exception as e:
            logger.error(f"Groq narrative generation failed, falling back to template: {e}")
            errors.append(f"Groq narrative failed: {e}")

    if not final_response:
        final_response = _deterministic_summary(top, alternatives, comparison_data)

    agent_status["response"] = "completed"
    logger.info("Response Agent completed successfully")

    return {"final_response": final_response, "agent_status": agent_status, "errors": errors}
>>>>>>> 87781e54869ecb82d7616c3ef400468d33171105
