import streamlit as st
import time
from frontend.styles import inject_custom_css
from frontend.components import (
    render_header, 
    render_progress_tracker, 
    render_product_card, 
    render_recommendation_section
)
from frontend.layout import render_sidebar_filters
# CHANGE 1: Removed obsolete imports:
#   - Agents.comparison_agent.comparison_agent
#   - Agents.recommendation_agent.recommendation_agent
#   - Services.amazon_service.AmazonService
#   - frontend.helpers.generate_mock_products
# These are no longer called directly from app.py — the new LangGraph
# pipeline (Agents/workflow.py) now owns search, fallback-mock-generation,
# comparison, recommendation, and response generation internally.
from frontend.home import render_home_page

# CHANGE 2: Import the single orchestration entry point for the new architecture.
from Agents.workflow import run_pipeline

# 1. Page Configuration (overall look and behaviour of websiite)
st.set_page_config(
    page_title="ShopWise - AI Compare",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session States
if "entered_app" not in st.session_state:
    st.session_state.entered_app = False

# 2. Inject CSS Styles to override native widget styling
inject_custom_css()

# Route to Welcome/Home page if not yet entered
if not st.session_state.entered_app:
    render_home_page()
    st.stop()

# 3. Render Top Navigation Bar (Native Streamlit columns)
render_header()

# 4. Initialize Session States
if "products" not in st.session_state:
    st.session_state.products = []
if "comparison_data" not in st.session_state:
    st.session_state.comparison_data = {}
if "recommendations" not in st.session_state:
    st.session_state.recommendations = []
if "agent_status" not in st.session_state:
    st.session_state.agent_status = {
        "search": "pending",
        "comparison": "pending",
        "recommendation": "pending",
        "response": "pending"
    }
if "search_query" not in st.session_state:
    st.session_state.search_query = ""
if "budget_limit" not in st.session_state:
    st.session_state.budget_limit = 30000.0
if "active_brand" not in st.session_state:
    st.session_state.active_brand = "All brands"
if "last_active_brand" not in st.session_state:
    st.session_state.last_active_brand = "All brands"
if "has_searched" not in st.session_state:
    st.session_state.has_searched = False
if "errors" not in st.session_state:
    st.session_state.errors = []
# CHANGE 3: New session state key to hold the Response Agent's markdown
# narrative (final_response), which the old pipeline never produced.
# We store it for potential future use, but we do NOT render it anywhere
# new, since the original UI never displayed a "final_response" block —
# per the "preserve existing UI exactly" requirement.
if "final_response" not in st.session_state:
    st.session_state.final_response = ""

# 5. Render Sidebar Filters (Native sidebar widgets)
query, budget, brand_filter, search_clicked = render_sidebar_filters()


def run_agents(query_val, budget_val, brand_filter_val, progress_placeholder):
    """
    CHANGE 4: Rewritten from the ground up.

    OLD BEHAVIOR: took a pre-fetched `products` list and ran only the
    comparison + recommendation agents against it (fast "filter-only" path).

    NEW BEHAVIOR: run_pipeline(query, budget, brand_filter, weights) is the
    single entry point into the LangGraph graph (Search -> Comparison ->
    Recommendation -> Response). It has no parameter for reusing
    previously-fetched products, so every call — including filter-only
    changes — now re-runs the full graph, including a fresh search.

    This is a deliberate, flagged behavior change (see explanation above
    the code): there is currently no cheaper "filter-only" path available
    without modifying workflow.py / graph_state.py, which was out of scope.

    We keep the same progress-tracker visuals as before, but since
    run_pipeline() is a single synchronous call with no intermediate
    callback, we can no longer animate each step turning "running" one at
    a time. We instead: mark all remaining steps "running" up front, render
    that, invoke the pipeline once, then adopt the real `agent_status`
    dict returned by the graph.
    """
    st.session_state.agent_status["comparison"] = "running"
    st.session_state.agent_status["recommendation"] = "running"
    st.session_state.agent_status["response"] = "running"

    progress_placeholder.empty()
    with progress_placeholder:
        render_progress_tracker(st.session_state.agent_status)
    time.sleep(0.4)  # Aesthetic animation delay (preserved from original)

    # CHANGE 5: Single call replaces the old manual
    # comparison_agent(state) -> recommendation_agent(state) sequence.
    result = run_pipeline(
        query=query_val,
        budget=budget_val,
        brand_filter=brand_filter_val,
        weights=None,
    )

    # CHANGE 6: Map the workflow's returned state dict onto the same
    # session_state keys the rest of app.py already expects, so the
    # downstream rendering code (sections 9-11) needs zero changes.
    st.session_state.products = result.get("products", [])
    st.session_state.comparison_data = result.get("comparison_data", {})
    st.session_state.recommendations = result.get("recommendations", [])
    st.session_state.errors = result.get("errors", [])
    st.session_state.final_response = result.get("final_response", "")

    # Adopt the graph's own agent_status if provided, otherwise mark all
    # steps completed manually as a safe fallback.
    returned_status = result.get("agent_status")
    if returned_status:
        st.session_state.agent_status = returned_status
    else:
        st.session_state.agent_status = {
            "search": "completed",
            "comparison": "completed",
            "recommendation": "completed",
            "response": "completed",
        }


# 6. Setup main content headers using Streamlit native colored markdown formatting
if st.session_state.has_searched:
    st.markdown(f'# Results for :blue["{query}"]')
    st.markdown(
        '<div style="color: #64748b; font-size: 1rem; margin-top: -0.75rem; margin-bottom: 2rem;">AI-powered comparison across multiple e-commerce platforms.</div>',
        unsafe_allow_html=True
    )
progress_placeholder = st.empty()

# 7. Check Actions and Triggers
trigger_search = False
trigger_filter = False

# Scraper trigger conditions
if search_clicked:
    trigger_search = True
elif query != st.session_state.search_query and query.strip():
    trigger_search = True

# Agent filter-only trigger conditions
if not trigger_search:
    if budget != st.session_state.budget_limit:
        trigger_filter = True
    elif st.session_state.active_brand != st.session_state.last_active_brand:
        trigger_filter = True

# 8. Execution Pipeline
if trigger_search:
    # Reset search and query parameters
    st.session_state.search_query = query
    st.session_state.budget_limit = budget
    st.session_state.last_active_brand = st.session_state.active_brand
    st.session_state.has_searched = True
    st.session_state.errors = []

    st.session_state.agent_status = {
        "search": "running",
        "comparison": "pending",
        "recommendation": "pending",
        "response": "pending"
    }

    progress_placeholder.empty()
    with progress_placeholder:
        render_progress_tracker(st.session_state.agent_status)

    # CHANGE 7: The old manual AmazonService() call + mock-fallback logic
    # + product normalization loop is removed entirely. The Search Agent
    # node inside the LangGraph pipeline (Agents/search_agent.py) already
    # performs the Amazon/Flipkart/Firecrawl calls, the mock fallback, and
    # dict normalization internally, and writes state["products"].
    # We simply delegate everything to run_agents(), which now calls
    # run_pipeline() and populates st.session_state from its result.
    run_agents(query, budget, brand_filter, progress_placeholder)

    st.session_state.agent_status["search"] = "completed"

    # Finalize progress cards
    progress_placeholder.empty()
    with progress_placeholder:
        render_progress_tracker(st.session_state.agent_status)

elif trigger_filter:
    # Update filters in state
    st.session_state.budget_limit = budget
    st.session_state.last_active_brand = st.session_state.active_brand

    # CHANGE 8: Filter-only path now also calls run_agents(), which invokes
    # run_pipeline() with the *existing* query but the new budget/brand.
    # See the ambiguity note above run_agents(): this now re-runs search
    # too, since run_pipeline() has no "reuse cached products" option.
    run_agents(st.session_state.search_query, budget, brand_filter, progress_placeholder)

    # Refresh progress cards
    progress_placeholder.empty()
    with progress_placeholder:
        render_progress_tracker(st.session_state.agent_status)
else:
    # Just render the existing progress state
    progress_placeholder.empty()
    with progress_placeholder:
        render_progress_tracker(st.session_state.agent_status)

# 9. Render the Results section
comparison_data = st.session_state.comparison_data
recommendations = st.session_state.recommendations

# Extract brand-filtered products
by_source_groups = comparison_data.get("by_source", {})
display_products = []
for src_list in by_source_groups.values():
    display_products.extend(src_list)

# Sort display products by value score descending (highest value score first)
display_products.sort(key=lambda x: x.get("value_score", 0.0), reverse=True)

matches_count = len(display_products)

# Matches header row using Streamlit columns
st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)
m_col1, m_col2 = st.columns([8, 2])
with m_col1:
    st.markdown(f"#### {matches_count} MATCHES")
with m_col2:
    st.markdown("<p style='text-align: right; color: #64748b; font-size: 0.875rem; font-weight: 500; margin-top: 0.25rem;'>Sorted by best value</p>", unsafe_allow_html=True)
st.markdown('<hr style="margin-top:-0.5rem; margin-bottom:1.5rem; border:0; border-top:1.5px solid #f1f5f9;"/>', unsafe_allow_html=True)

# 10. Display product grid using rows of 3 native Streamlit columns
if matches_count > 0:
    best_value_prod = comparison_data.get("best_value")
    best_value_url = best_value_prod.get("url") if best_value_prod else None

    # Render row-by-row
    for i in range(0, len(display_products), 3):
        row_products = display_products[i:i+3]
        cols = st.columns(3)
        for idx, p in enumerate(row_products):
            with cols[idx]:
                is_bv = (best_value_url and p.get("url") == best_value_url)
                render_product_card(p, is_best_value=is_bv)
else:
    st.info("No matching products found within the specified budget or brand filter. Try widening your criteria!")

# 11. Render the AI Recommendation Section using native layout
if recommendations:
    st.markdown("<div style='margin-top:2.5rem;'></div>", unsafe_allow_html=True)
    render_recommendation_section(recommendations[0])
