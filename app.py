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
from frontend.helpers import generate_mock_products
from Agents.comparison_agent import comparison_agent
from Agents.recommendation_agent import recommendation_agent
from Services.amazon_service import AmazonService
from frontend.home import render_home_page

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

# 5. Render Sidebar Filters (Native sidebar widgets)
query, budget, brand_filter, search_clicked = render_sidebar_filters()

def run_agents(products, budget_val, brand_filter_val, progress_placeholder):
    """Run Comparison and Recommendation Agents sequentially with progress updates."""
    # Reset status for agents
    st.session_state.agent_status["comparison"] = "running"
    st.session_state.agent_status["recommendation"] = "pending"
    st.session_state.agent_status["response"] = "pending"
    
    progress_placeholder.empty()
    with progress_placeholder:
        render_progress_tracker(st.session_state.agent_status)
    time.sleep(0.4) # Aesthetic animation delay
    
    # Assemble Comparison Agent State
    state = {
        "products": [p.copy() for p in products],
        "brand_filter": brand_filter_val,
        "budget": budget_val,
        "comparison_data": {},
        "recommendations": [],
        "agent_status": st.session_state.agent_status,
        "errors": []
    }
    
    # Execute Comparison Agent
    comp_out = comparison_agent(state)
    state.update(comp_out)
    
    st.session_state.agent_status["comparison"] = "completed"
    st.session_state.agent_status["recommendation"] = "running"
    
    progress_placeholder.empty()
    with progress_placeholder:
        render_progress_tracker(st.session_state.agent_status)
    time.sleep(0.4) # Aesthetic animation delay
    
    # Execute Recommendation Agent
    rec_out = recommendation_agent(state)
    state.update(rec_out)
    
    st.session_state.agent_status["recommendation"] = "completed"
    st.session_state.agent_status["response"] = "completed"
    
    # Store results in Session State
    st.session_state.comparison_data = state.get("comparison_data", {})
    st.session_state.recommendations = state.get("recommendations", [])
    st.session_state.errors = state.get("errors", [])

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
        
    # Search via AmazonService
    service = AmazonService()
    try:
        raw_products = service.search(query)
    except Exception as e:
        raw_products = []
        st.session_state.errors.append(f"SerpAPI search failed: {e}")
        
    # Fallback to smart mockup products if SerpAPI returned nothing (e.g. key missing)
    if not raw_products:
        raw_products = generate_mock_products(query)
        
    # Normalize product objects to dicts
    products = []
    for p in raw_products:
        if hasattr(p, "model_dump"):
            products.append(p.model_dump())
        elif isinstance(p, dict):
            products.append(p)
            
    st.session_state.products = products
    st.session_state.agent_status["search"] = "completed"
    
    # Run comparison and recommendation agents
    run_agents(products, budget, brand_filter, progress_placeholder)
    
    # Finalize progress cards
    progress_placeholder.empty()
    with progress_placeholder:
        render_progress_tracker(st.session_state.agent_status)

elif trigger_filter:
    # Update filters in state
    st.session_state.budget_limit = budget
    st.session_state.last_active_brand = st.session_state.active_brand
    
    # Run agents using existing cached products (fast response)
    run_agents(st.session_state.products, budget, brand_filter, progress_placeholder)
    
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
