import streamlit as st
from typing import Dict, Any, List
from frontend.helpers import get_pricing_details
from utils.helpers import format_currency

def render_header():
    """Renders the top navigation header using native Streamlit columns and inline layout elements."""
    col1, col2 = st.columns([8, 2])
    with col1:
        st.markdown(
            '<div style="display:flex; align-items:center; gap:0.5rem; margin-top:-0.5rem;">'
            '<span style="font-size:1.6rem; background-color:#7c4dff; color:white; padding:0.25rem 0.5rem; border-radius:8px; font-weight:700; box-shadow: 0 4px 10px rgba(124, 77, 255, 0.25);">🛍️</span>'
            '<span style="font-size:1.5rem; font-weight:700; color:#0f172a; letter-spacing:-0.5px; margin-left:0.25rem;">ShopWise</span>'
            '<span style="font-size:0.875rem; color:#94a3b8; font-weight:500; margin-top:0.35rem;">&nbsp;&bull;&nbsp; AI Compare</span>'
            '</div>',
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            '<div style="display:flex; justify-content:flex-end; align-items:center; gap:1.25rem; color:#64748b; font-size:1.25rem; margin-top:0.15rem;">'
            '</div>',
            unsafe_allow_html=True
        )
    st.markdown('<hr style="margin-top:0.5rem; margin-bottom:1.5rem; border:0; border-top:1px solid #f1f5f9;"/>', unsafe_allow_html=True)

def render_progress_tracker(agent_status: Dict[str, str]):
    """Renders the 4 progress steps (Search, Compare, Recommend, Response) 
    using 4 native Streamlit containers within columns.
    """
    steps = [
        ("search", "01 Search", "Scanning...", "🔍"),
        ("comparison", "02 Compare", "Weighing...", "⚖️"),
        ("recommendation", "03 Recommend", "Finding...", "🪄"),
        ("response", "04 Response", "Ready...", "✅")
    ]
    
    cols = st.columns(4)
    
    for idx, (key, label, active_desc, emoji) in enumerate(steps):
        status = agent_status.get(key, "pending").lower()
        
        status_text = "Pending"
        if status == "completed":
            status_text = "✓ Completed"
        elif status == "running":
            status_text = "Running..."
        elif status == "failed":
            status_text = "Failed"
            
        with cols[idx]:
            with st.container(border=True):
                # Anchor tag for styling via styles.py
                st.markdown(f'<div class="progress-card-anchor {status}"></div>', unsafe_allow_html=True)
                
                # Internal layout of progress card
                sub_c1, sub_c2 = st.columns([1, 4])
                with sub_c1:
                    st.markdown(f"<span style='font-size: 1.5rem;'>{emoji}</span>", unsafe_allow_html=True)
                with sub_c2:
                    st.markdown(f"<div style='font-size: 0.75rem; color: #94a3b8; font-weight: 600; letter-spacing: 0.5px;'>{label}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='font-size: 0.9rem; font-weight: 700; color:#1e293b;'>{active_desc if status == 'running' else label.split(' ')[1]}</div>", unsafe_allow_html=True)
                    
                # Mini badge text
                if status == "completed":
                    st.markdown('<div style="font-size:0.75rem; font-weight:600; color:#059669; margin-top:0.25rem;">Completed</div>', unsafe_allow_html=True)
                elif status == "running":
                    st.markdown('<div style="font-size:0.75rem; font-weight:600; color:#7c4dff; margin-top:0.25rem;">Running...</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div style="font-size:0.75rem; font-weight:600; color:#94a3b8; margin-top:0.25rem;">Pending</div>', unsafe_allow_html=True)

def render_product_card(product: Dict[str, Any], is_best_value: bool = False):
    """Renders a single product card inside a native Streamlit container."""
    name = getattr(product, "name", "Unknown Product")
    price = getattr(product, "price", 0.0)
    rating = getattr(product, "rating", 0.0)
    reviews = getattr(product, "reviews", 0)
    source = getattr(product, "source", "Unknown").lower()
    delivery_info = getattr(product, "delivery_info", "")
    url = getattr(product, "url", "#")
    image_url = getattr(product, "image_url", "")

    with st.container(border=True):
        # Product Card Anchor for styles.py to target
        st.markdown('<div class="product-card-anchor"></div>', unsafe_allow_html=True)
        
        # Original price and discount calculation
        original_price, discount_str = get_pricing_details(price, name)
        
        # Badge line (Source, Best Value, Discount)
        badges_html = f'<div class="product-badge-row"><div class="source-badge {source}">{source.title()}</div>'
        if is_best_value:
            badges_html += '<div class="best-value-badge">🏆 Best value</div>'
        badges_html += f'<div class="discount-badge">{discount_str}</div></div>'
        st.markdown(badges_html, unsafe_allow_html=True)
        
        # Product media thumbnail
        if image_url:
            st.image(image_url, use_container_width=True)
        else:
            # Box package SVG placeholder
            st.markdown(
                '<div style="background-color:#f8fafc; border-radius:16px; height:120px; display:flex; align-items:center; justify-content:center; margin-bottom:0.75rem; margin-top:0.5rem;">'
                '<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#cbd5e1" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
                '<path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/>'
                '<path d="m3.3 7 8.7 5 8.7-5"/>'
                '<path d="M12 22V12"/>'
                '</svg>'
                '</div>',
                unsafe_allow_html=True
            )
            
        # Title text
        st.markdown(f'<div class="product-title-text" title="{name}">{name}</div>', unsafe_allow_html=True)
        
        # Formatted price text
        price_formatted = format_currency(price, "₹").replace(".00", "")
        orig_formatted = format_currency(original_price, "₹").replace(".00", "")
        st.markdown(
            f'<div style="display:flex; align-items:baseline; gap:0.5rem; margin-bottom:0.5rem;">'
            f'<span style="font-size:1.3rem; font-weight:700; color:#0f172a;">{price_formatted}</span>'
            f'<span style="font-size:0.9rem; text-decoration:line-through; color:#94a3b8;">{orig_formatted}</span>'
            f'</div>',
            unsafe_allow_html=True
        )
        
        # Ratings and delivery text
        rating_str = ""
        if rating > 0:
            rating_str = f"⭐ {rating:.1f}"
            if reviews > 0:
                rating_str += f" ({reviews:,})"
                
        meta_str = f"<span style='color:#64748b; font-size:0.8rem; font-weight:500;'>{rating_str}"
        if delivery_info:
            if rating_str:
                meta_str += " | "
            meta_str += delivery_info
        meta_str += "</span>"
        
        st.markdown(meta_str, unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:0.75rem;'></div>", unsafe_allow_html=True)
        
        # Native Streamlit Link Button
        st.link_button(label="View product", url=url, use_container_width=True)

def render_recommendation_section(recommendation: Dict[str, Any]):
    """Renders the AI recommendation card using a native Streamlit container and metrics."""
    name = getattr(recommendation, "name", "Unknown Product")
    price = getattr(recommendation, "price", 0.0)
    rating = getattr(recommendation, "rating", 0.0)
    reviews = getattr(recommendation, "reviews", 0)
    why = getattr(
        recommendation,
        "why",
        "Highly recommended based on your preferences."
    )
    url = getattr(recommendation, "url", "#")
    source = getattr(recommendation, "source", "Amazon")    
    
    with st.container(border=True):
        # Anchor tag to allow styles.py to apply the purple background styling
        st.markdown('<div class="rec-card-anchor"></div>', unsafe_allow_html=True)
        
        # Header Badge
        st.markdown(
            '<div style="display:flex; align-items:center; gap:0.5rem; font-size:0.75rem; font-weight:700; letter-spacing:1px; color:#e0e7ff; margin-bottom:0.75rem;">'
            '<span>🏆</span><span>BEST VALUE RECOMMENDATION</span>'
            '</div>',
            unsafe_allow_html=True
        )
        
        # Recommendation Title & Summary (with rec-text-white override class)
        st.markdown(f'<h3 class="rec-text-white" style="margin-top:0.25rem; font-size:1.75rem; font-weight:700; letter-spacing:-0.5px; line-height:1.2;">{name}</h3>', unsafe_allow_html=True)
        st.markdown(f'<p class="rec-text-white" style="font-size:1rem; opacity:0.9; margin-bottom:1.75rem; line-height:1.5;">{why} ShopWise AI ranked this as the best balance of price, reviews and shipping.</p>', unsafe_allow_html=True)
        
        # Metrics & Button columns
        original_price, _ = get_pricing_details(price, name)
        savings = original_price - price
        
        price_formatted = format_currency(price, "₹").replace(".00", "")
        orig_formatted = format_currency(original_price, "₹").replace(".00", "")
        savings_formatted = format_currency(savings, "₹").replace(".00", "")
        
        col1, col2, col3, col4 = st.columns([2, 3, 3, 4])
        
        with col1:
            st.metric(label="BEST PRICE", value=price_formatted)
        with col2:
            st.metric(label="YOU SAVE", value=savings_formatted, delta=f"vs {orig_formatted}")
        with col3:
            st.metric(label="RATING", value=f"{rating:.1f} ★", delta=f"{reviews:,} reviews")
        with col4:
            # Spacing helper for button alignment
            st.markdown('<div style="height: 1.5rem;"></div>', unsafe_allow_html=True)
            st.link_button(label=f"View on {source}", url=url)
