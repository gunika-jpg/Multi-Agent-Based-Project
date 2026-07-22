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

# welcome page
from frontend.home import render_home_page

# main AI workflow
from Agents.workflow import run_pipeline

# 1. Page Configuration (overall look and behaviour of website)
st.set_page_config(
    page_title="ShopWise - AI Compare",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Track whether the user has entered the app
if "entered_app" not in st.session_state:
    st.session_state.entered_app = False

# Apply custom styling
inject_custom_css()

# Show home page before entering the app
if not st.session_state.entered_app:
    render_home_page()
    st.stop()

# Display the app header
render_header()

# Initialize session state variables
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

# Store the final AI response
if "final_response" not in st.session_state:
    st.session_state.final_response = ""

# Render sidebar filters
query, budget, brand_filter, search_clicked = render_sidebar_filters()

# Run the AI workflow
def run_agents(query_val, budget_val, brand_filter_val, progress_placeholder):
    
    # Update agent status
    st.session_state.agent_status["comparison"] = "running"
    st.session_state.agent_status["recommendation"] = "running"
    st.session_state.agent_status["response"] = "running"

    
    # Display progress tracker
    progress_placeholder.empty()
    with progress_placeholder:
        render_progress_tracker(st.session_state.agent_status)
    time.sleep(0.4)  

    # Execute the AI pipeline
    result = run_pipeline(
        query=query_val,
        budget=budget_val,
        brand_filter=brand_filter_val,
        weights=None,
    )

    # Store the workflow results
    st.session_state.products = result.get("products", [])
    st.session_state.comparison_data = result.get("comparison_data", {})
    st.session_state.recommendations = result.get("recommendations", [])
    st.session_state.errors = result.get("errors", [])
    st.session_state.final_response = result.get("final_response", "")

    # Update agent status
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


# Display search results header
if st.session_state.has_searched:
    st.markdown(f'# Results for :blue["{query}"]')
    st.markdown(
        '<div style="color: #64748b; font-size: 1rem; margin-top: -0.75rem; margin-bottom: 2rem;">AI-powered comparison across multiple e-commerce platforms.</div>',
        unsafe_allow_html=True
    )
progress_placeholder = st.empty()

# check user actions
trigger_search = False
trigger_filter = False

# detect a new search
if search_clicked:
    trigger_search = True
elif query != st.session_state.search_query and query.strip():
    trigger_search = True

# detect filter change
if not trigger_search:
    if budget != st.session_state.budget_limit:
        trigger_filter = True
    elif st.session_state.active_brand != st.session_state.last_active_brand:
        trigger_filter = True

# run the search workflow
if trigger_search:
    # save current search details
    st.session_state.search_query = query
    st.session_state.budget_limit = budget
    st.session_state.last_active_brand = st.session_state.active_brand
    st.session_state.has_searched = True
    st.session_state.errors = []
     
    # update agent status
    st.session_state.agent_status = {
        "search": "running",
        "comparison": "pending",
        "recommendation": "pending",
        "response": "pending"
    }

    # show progress tracker
    progress_placeholder.empty()
    with progress_placeholder:
        render_progress_tracker(st.session_state.agent_status)
        # run AI workflow
    run_agents(query, budget, brand_filter, progress_placeholder)
    st.session_state.agent_status["search"] = "completed"

    # update the progress tracker
    progress_placeholder.empty()
    with progress_placeholder:
        render_progress_tracker(st.session_state.agent_status)

elif trigger_filter:
    # save updated filters
    st.session_state.budget_limit = budget
    st.session_state.last_active_brand = st.session_state.active_brand

    #re run AI workflow
    run_agents(
        st.session_state.search_query,
        budget,
        brand_filter, 
        progress_placeholder
        )

    # update the progress tracker
    progress_placeholder.empty()
    with progress_placeholder:
        render_progress_tracker(st.session_state.agent_status)
else:
    # display current progress
    progress_placeholder.empty()
    with progress_placeholder:
        render_progress_tracker(st.session_state.agent_status)

# 9. Get results from session state
comparison_data = st.session_state.comparison_data
recommendations = st.session_state.recommendations

# Prepare products for display
by_source_groups = comparison_data.get("by_source", {})
display_products = []
for src_list in by_source_groups.values():
    display_products.extend(src_list)

# Sort display products by value score (highest value score first)
display_products.sort(key=lambda x: getattr(x, "value_score", 0.0), reverse=True)

matches_count = len(display_products)

# display search summary
st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)
m_col1, m_col2 = st.columns([8, 2])
with m_col1:
    st.markdown(f"#### {matches_count} MATCHES")
with m_col2:
    st.markdown("<p style='text-align: right; color: #64748b; font-size: 0.875rem; font-weight: 500; margin-top: 0.25rem;'>Sorted by best value</p>", unsafe_allow_html=True)
st.markdown('<hr style="margin-top:-0.5rem; margin-bottom:1.5rem; border:0; border-top:1.5px solid #f1f5f9;"/>', unsafe_allow_html=True)

# Display product cards
if matches_count > 0:
    best_value_prod = comparison_data.get("best_value")
    best_value_url = best_value_prod.url if best_value_prod else None

    # show products in rows of three
    for i in range(0, len(display_products), 3):
        row_products = display_products[i:i+3]
        cols = st.columns(3)
        for idx, p in enumerate(row_products):
            with cols[idx]:
                is_bv = (best_value_url and p.url == best_value_url)
                render_product_card(p, is_best_value=is_bv)
else:
    st.info("No matching products found within the specified budget or brand filter. Try widening your criteria!")

# display AI recommendation
if recommendations:
    st.markdown("<div style='margin-top:2.5rem;'></div>", unsafe_allow_html=True)
    render_recommendation_section(recommendations[0])
