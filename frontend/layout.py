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
            placeholder="Search products...",
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
            '<div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#94a3b8; margin-top:-0.5rem; margin-bottom:1.5rem;">'
            '<span>₹5k</span><span>₹100k</span>'
            '</div>',
            unsafe_allow_html=True
        )
        
        # 3. Brand Pill Filter
        st.markdown('**Brand**')
        brands = ["All brands", "Sony", "Bose", "Apple", "Sennheiser", "JBL"]
        if "active_brand" not in st.session_state:
            st.session_state.active_brand = "All brands"
            
        # Display brand pills in a 3x2 grid
        b_cols1 = st.columns(3)
        b_cols2 = st.columns(3)
        
        brand_clicked = None
        
        for i, brand in enumerate(brands):
            target_col = b_cols1[i] if i < 3 else b_cols2[i - 3]
            is_active = (st.session_state.active_brand == brand)
            with target_col:
                if st.button(
                    brand, 
                    key=f"brand_pill_{brand}",
                    type="primary" if is_active else "secondary",
                    use_container_width=True
                ):
                    brand_clicked = brand
                    
        # Update active brand if clicked
        if brand_clicked is not None:
            st.session_state.active_brand = brand_clicked
            st.rerun()
            
        st.markdown("<div style='margin-bottom:2rem;'></div>", unsafe_allow_html=True)
        
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
    brand_filter_val = "" if st.session_state.active_brand == "All brands" else st.session_state.active_brand
    return query, float(budget), brand_filter_val, search_clicked
