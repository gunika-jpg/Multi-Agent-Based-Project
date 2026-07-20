import streamlit as st

def inject_custom_css():
    """Inject premium CSS styles for styling native Streamlit widgets."""
    css = """
    <style>
    
    /* Global Typography Overrides */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif !important;
        background-color: #fcfdfe !important;
        color: #1e293b !important;
    }

    /* Hide Streamlit default header */

#MainMenu {
    visibility: hidden !important;
}


    /* Top Navigation bar styling */
    .shopwise-header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background-color: #ffffff;
        border-bottom: 1px solid #f1f5f9;
        margin-top: -6rem; /* pull up to top of streamlit wrapper */
        margin-bottom: 2rem;
        width: 100vw;
        position: relative;
        left: 50%;
        right: 50%;
        margin-left: -50vw;
        margin-right: -50vw;
        box-sizing: border-box;
    }
    
    .shopwise-logo-group {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .shopwise-logo-icon {
        background-color: #2563EB;
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        font-weight: 700;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.25);
    }
    
    .shopwise-logo-text {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0f172a;
        letter-spacing: -0.5px;
    }
    
    .shopwise-logo-sub {
        font-size: 0.875rem;
        color: #94a3b8;
        font-weight: 500;
        margin-top: 0.25rem;
    }

    .shopwise-nav-actions {
        display: flex;
        align-items: center;
        gap: 1.25rem;
        color: #64748b;
    }

    /* Left Sidebar Filter Container styling */
    [data-testid="stSidebar"] {
        background-color: black !important;
        border-right: 1px solid #f1f5f9 !important;
        padding-top: 2rem;
    }
    
    .filter-panel-title {
        font-size: 0.75rem;
        font-weight: 700;
        color: #94a3b8;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Form Inputs and UI overrides */
    .stTextInput input {
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
        padding: 0.625rem 1rem !important;
        font-size: 0.95rem !important;
        color: #334155 !important;
        background-color: #ffffff !important;
        box-shadow: none !important;
        transition: border-color 0.2s ease;
    }
    
    .stTextInput input:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;

    }

    /* Brand Button Pills */
    div.stButton > button {
        border-radius: 20px !important;
        padding: 0.375rem 1rem !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        border: 1px solid #e2e8f0 !important;
        background-color: #ffffff !important;
        color: #475569 !important;
    }
    
    /* Hover and Selected states for Streamlit buttons */
    div.stButton > button:hover {
        border-color: #7c4dff !important;
        color: #7c4dff !important;
        background-color: #f5f3ff !important;
    }
    
    div.stButton > button[kind="primary"] {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border-color: #0f172a !important;
    }
    
    div.stButton > button[kind="primary"]:hover {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border-color: #1e293b !important;
    }

    /* AI Search Button */
    .ai-search-container div.stButton > button {
        background-color: #2563EB !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(124, 77, 255, 0.2) !important;
    }
    
    .ai-search-container div.stButton > button:hover {
        background-color: #1D4ED8 !important;
        box-shadow: 0 6px 16px rgba(124, 77, 255, 0.3) !important;
    }

    /* Slider styling overrides */
    div[data-role="stSlider"] [data-testid="stThumb"] {
        background-color: #7c4dff !important;
        border: 2px solid #7c4dff !important;
    }
    
    div[data-role="stSlider"] [data-testid="stTrack"] > div {
        background-color: #7c4dff !important;
    }

    /* Results Header */
    .results-title {
        font-size: 2.25rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.25rem;
    }
    
    .results-title span {
        color: #7c4dff;
    }
    
    .results-subtitle {
        font-size: 1rem;
        color: #64748b;
        margin-bottom: 2rem;
    }

    /* Matches Header Row */
    .matches-header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.25rem;
        border-bottom: 1.5px solid #f1f5f9;
        padding-bottom: 0.75rem;
    }
    
    .matches-count {
        font-size: 0.875rem;
        font-weight: 700;
        color: #475569;
        letter-spacing: 1px;
    }
    
    .matches-sort-label {
        font-size: 0.875rem;
        color: #64748b;
        font-weight: 500;
    }

    /* Target Native Streamlit Containers for Progress Tracker Cards */
    div[data-testid="stVerticalBlockBorderDiv"]:has(div.progress-card-anchor) {
        border-radius: 16px !important;
        border: 1px solid #f1f5f9 !important;
        background-color: #ffffff !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02) !important;
        padding: 1rem 1.25rem !important;
        transition: all 0.2s ease !important;
    }
    
    /* Running progress state styling */
    div[data-testid="stVerticalBlockBorderDiv"]:has(div.progress-card-anchor.running) {
        border: 1.5px dashed #7c4dff !important;
        background-color: #f5f3ff !important;
    }
    
    /* Completed progress state styling */
    div[data-testid="stVerticalBlockBorderDiv"]:has(div.progress-card-anchor.completed) {
        background-color: #ffffff !important;
        border: 1px solid #d1fae5 !important;
    }

    /* Target Native Product Card Containers */
    div[data-testid="stVerticalBlockBorderDiv"]:has(div.product-card-anchor) {
        border-radius: 20px !important;
        border: 1px solid #f1f5f9 !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02) !important;
        padding: 1.25rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        background-color: #ffffff !important;
    }
    
    div[data-testid="stVerticalBlockBorderDiv"]:has(div.product-card-anchor):hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.06) !important;
        border-color: #2563EB !important;
    }

    /* Styling elements inside native product cards */
    .product-badge-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        margin-bottom: 0.5rem;
    }

    .source-badge {
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.25rem 0.75rem;
        border-radius: 8px;
        display: inline-block;
    }
    
    .source-badge.amazon {
        background-color: #ffedd5 !important;
        color: #ea580c !important;
    }
    
    .source-badge.flipkart {
        background-color: #e0f2fe !important;
        color: #0284c7 !important;
    }
    
    .source-badge.croma {
        background-color: #ccfbf1 !important;
        color: #0d9488 !important;
    }
    
    .source-badge.other {
        background-color: #f1f5f9 !important;
        color: #475569 !important;
    }

    .best-value-badge {
        background-color: #d1fae5 !important;
        color: #065f46 !important;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        padding: 0.25rem 0.75rem !important;
        border-radius: 8px !important;
    }

    .discount-badge {
        background-color: #0f172a !important;
        color: #ffffff !important;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        width: 34px !important;
        height: 34px !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-left: auto;
    }

    /* Product Title text styling */
    .product-title-text {
        font-size: 0.975rem !important;
        font-weight: 600 !important;
        color: #0f172a !important;
        line-height: 1.4 !important;
        height: 2.7rem !important;
        display: -webkit-box !important;
        -webkit-line-clamp: 2 !important;
        -webkit-box-orient: vertical !important;
        overflow: hidden !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Target native Link Buttons (to look like view button) */
    div.stLinkButton > a {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 12px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        color: #1e293b !important;
        background-color: #ffffff !important;
        text-decoration: none !important;
        font-size: 0.875rem !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }
    
    div.stLinkButton > a:hover {
        border-color: #0f172a !important;
        background-color: #f8fafc !important;
        color: #0f172a !important;
    }

    /* TARGET PREMIUM AI RECOMMENDATION CONTAINER */
    div[data-testid="stVerticalBlockBorderDiv"]:has(div.rec-card-anchor) {
        background: linear-gradient(135deg, #7c4dff 0%, #6366f1 100%) !important;
        border: none !important;
        border-radius: 24px !important;
        padding: 2.25rem !important;
        box-shadow: 0 10px 30px rgba(124, 77, 255, 0.25) !important;
        color: #ffffff !important;
    }
    
    /* Make text elements inside recommendation container white */
    div[data-testid="stVerticalBlockBorderDiv"]:has(div.rec-card-anchor) .rec-text-white,
    div[data-testid="stVerticalBlockBorderDiv"]:has(div.rec-card-anchor) [data-testid="stMarkdownContainer"] p,
    div[data-testid="stVerticalBlockBorderDiv"]:has(div.rec-card-anchor) h1,
    div[data-testid="stVerticalBlockBorderDiv"]:has(div.rec-card-anchor) h2,
    div[data-testid="stVerticalBlockBorderDiv"]:has(div.rec-card-anchor) h3 {
        color: #ffffff !important;
    }
    
    div[data-testid="stVerticalBlockBorderDiv"]:has(div.rec-card-anchor) [data-testid="stMetricLabel"] {
        color: #c7d2fe !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.5px !important;
    }
    
    div[data-testid="stVerticalBlockBorderDiv"]:has(div.rec-card-anchor) [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }
    
    /* Style the dark CTA button inside purple recommendation card */
    div[data-testid="stVerticalBlockBorderDiv"]:has(div.rec-card-anchor) div.stLinkButton > a {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 30px !important;
        font-weight: 600 !important;
        padding: 0.75rem 2rem !important;
        width:auto !important;
        min-width: 180px !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.3) !important;
        margin-left: auto;
    }
    
    div[data-testid="stVerticalBlockBorderDiv"]:has(div.rec-card-anchor) div.stLinkButton > a:hover {
        background-color: #1e293b !important;
        color: #ffffff !important;
        transform: translateY(-2px) !important;
    }

    /* Welcome/Home Page Styling */
    .home-container {
        text-align: center;
        padding: 3.5rem 2rem;
        background-color: #ffffff;
        border: 1px solid #f1f5f9;
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.015);
        max-width: 650px;
        margin: 1rem auto;
        animation: fadeIn 0.8s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .home-illustration-wrapper {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #7C4DFF 0%, #6D28D9 100%);
        width: 90px;
        height: 90px;
        border-radius: 24px;
        box-shadow: 0 10px 25px rgba(124, 77, 255, 0.25);
        margin-bottom: 2rem;
        transition: transform 0.3s ease;
    }
    
    .home-illustration-wrapper:hover {
        transform: scale(1.05) rotate(5deg);
    }

    .home-title {
        font-size: 3rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .home-subtitle {
        font-size: 0.875rem;
        color: #2563EB;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 1.5rem;
    }
    
    .home-description {
        font-size: 1.1rem;
        color: #475569;
        line-height: 1.6;
        margin-bottom: 2.5rem;
        max-width: 500px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Center and style the Enter App button */
    .home-button-container {
        display: flex;
        justify-content: center;
        margin-top: 1rem;
    }
    
    .home-button-container div.stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #3B82F6 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        padding: 0.75rem 2.5rem !important;
        box-shadow: 0 4px 15px rgba(124, 77, 255, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        height: auto !important;
        min-width: 200px !important;
    }
    
    .home-button-container div.stButton > button:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #2563EB 100%) !important;
        box-shadow: 0 6px 20px rgba(124, 77, 255, 0.45) !important;
        transform: translateY(-2px) !important;
        color: #ffffff !important;
    }
    
    .home-button-container div.stButton > button:active {
        transform: translateY(0) !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
