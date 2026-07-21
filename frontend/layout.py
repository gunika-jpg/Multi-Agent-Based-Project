import streamlit as st
from typing import Tuple
from pydantic import BaseModel


class SidebarFilters(BaseModel):
    query: str
    budget: float
    brand_filter: str
    search_clicked: bool


def render_sidebar_filters() -> Tuple[str, float, str, bool]:
    """Render the sidebar filters."""

    with st.sidebar:

        st.markdown(
            '<div class="filter-panel-title">⚙️ FILTERS</div>',
            unsafe_allow_html=True,
        )

        # ---------------- Product Search ----------------

        st.markdown("**Product Search**")

        query = st.text_input(
            "Product Search",
            placeholder="MacBook Air M4",
            label_visibility="collapsed",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ---------------- Budget ----------------

        current_budget = st.session_state.get("budget_limit", 30000)

        st.markdown(f"**Budget • Up to ₹{current_budget:,}**")

        budget = st.slider(
            "Budget",
            min_value=5000,
            max_value=1000000,
            value=int(current_budget),
            step=5000,
            label_visibility="collapsed",
        )

        st.caption("₹5,000                                    ₹10,00,000")

        st.markdown("---")

        # ---------------- Brand Filter ----------------

        brands = [
            "All Brands",
            "Apple",
            "Samsung",
            "OnePlus",
            "boAt",
            "Sony",
            "HP",
            "Dell",
            "Lenovo",
        ]

        selected_brand = st.selectbox(
            "Brand",
            brands,
            index=0,
        )

        brand_filter = (
            ""
            if selected_brand == "All Brands"
            else selected_brand
        )

        st.session_state.active_brand = selected_brand

        st.markdown("---")

        # ---------------- Search Sources ----------------

        st.markdown("### 🛒 Search Sources")

        for source in [
            "Amazon",
            "Flipkart",
            "Croma",
            "Reliance Digital",
        ]:
            st.markdown(f"✅ {source}")

        st.caption("More retailers coming soon...")

        st.markdown("<br>", unsafe_allow_html=True)

        # ---------------- Search Button ----------------

        search_clicked = st.button(
            "✨ Search with AI",
            use_container_width=True,
        )

        st.caption(
            "Results are aggregated live from multiple e-commerce websites."
        )

    filters = SidebarFilters(
        query=query.strip(),
        budget=float(budget),
        brand_filter=brand_filter,
        search_clicked=search_clicked,
    )

    return (
        filters.query,
        filters.budget,
        filters.brand_filter,
        filters.search_clicked,
    )