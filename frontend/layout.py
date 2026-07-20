import streamlit as st
from typing import Tuple, Dict, Any

def render_sidebar_filters() -> Tuple[str, float, str, bool]:
    """Renders the left sidebar filter panel according to the reference UI.
    
    Returns:
        Tuple[str, float, str, bool]: (query, budget, brand_filter, search_clicked)
    """
    with st.sidebar:
        # Filter section title
        st.markdown('<div class="filter-panel-title">⚙️ FILTERS</div>', unsafe_allow_html=True)
        
        # 1. Product Search Input
        st.markdown('**Product search**')
        query = st.text_input(
            "Product search",
            placeholder="Macbook Air M4",
            label_visibility="collapsed"
        )
        
        st.markdown("<div style='margin-bottom:1.5rem;'></div>", unsafe_allow_html=True)
        
        # 2. Budget Slider
        # Retrieve current slider state
        current_budget = st.session_state.get("budget_limit", 30000.0)
        st.markdown(f'**Budget &bull; up to ₹{int(current_budget):,}**')
        budget = st.slider(
            "Budget limit",
            min_value=5000,
            max_value=1000000,
            value=int(current_budget),
            step=5000,
            label_visibility="collapsed"
        )
        # Helper text for range
        st.markdown(
            '<div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#94a3b8; margin-top:-0.25rem; margin-bottom:1.5rem;">'
            '<span>₹5k</span><span>₹1000k</span>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown("### 🛒 Search Sources")

        sources = [
            "Amazon",
            "Flipkart",
            "Croma",
            "Reliance Digital",
        ]

        for source in sources:
            st.markdown(f"✅ {source}")

        st.caption("More retailers coming soon...")

        st.markdown("<div style='margin-bottom:1.5rem;'></div>", unsafe_allow_html=True)
        
        
        # 4. Search with AI Button
        st.markdown('<div class="ai-search-container">', unsafe_allow_html=True)
        search_clicked = st.button("✨ Search with AI", key="ai_search_btn")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<div style='margin-bottom:1.5rem;'></div>", unsafe_allow_html=True)
        
        # Subtext below filter panel
        st.markdown(
            '<div style="font-size:0.75rem; color:#94a3b8; line-height:1.4; text-align:center;">'
            'Results are aggregated live from Amazon, Flipkart and other retailers.'
            '</div>',
            unsafe_allow_html=True
        )
        
    # Return inputs, translating "All brands" to empty string for Comparison Agent
    return query, float(budget), "", search_clicked