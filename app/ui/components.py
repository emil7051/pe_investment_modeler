"""
Contains reusable UI components for the application.
"""
import streamlit as st
from app.ui.styles import HIGHLIGHT_COLOR, LIGHT_COLOR, DARK_GRAY

def render_header(title="Private Equity Investment Analysis"):
    """
    Renders the application header.
    
    Args:
        title: The title of the application
    """
    st.markdown(f"""
    <div style="text-align: left; margin-bottom: 2rem;">
        <h1 style="color: {LIGHT_COLOR}; margin-bottom: 1rem; font-weight: 500;">
            {title}
            <span style="color: {HIGHLIGHT_COLOR};">.</span>
        </h1>
        <p style="color: {LIGHT_COLOR}; opacity: 0.9; font-size: 1.1rem; max-width: 700px;">
            This app helps you model and visualise the performance of private equity investments. 
            Adjust the parameters in the sidebar to see how they affect the investment returns.
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    """
    Renders the application footer.
    """
    st.markdown(f"""
    <footer>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 2.5rem; padding-top: 1.5rem; border-top: 1px solid {DARK_GRAY};">
            <div>
                <p style="color: {LIGHT_COLOR}; opacity: 0.7;">
                    PE Investment Modeller by <span style="color: {HIGHLIGHT_COLOR};">Parc</span>
                </p>
            </div>
            <div style="text-align: right;">
                <p style="color: {LIGHT_COLOR}; opacity: 0.7;">
                    Data is for illustrative purposes only
                </p>
            </div>
        </div>
    </footer>
    """, unsafe_allow_html=True)

def render_card(title, value, subtitle=None, prefix="$", suffix=""):
    """
    Renders a card with a title, value, and optional subtitle.
    
    Args:
        title: The title of the card
        value: The main value to display in the card
        subtitle: Optional subtitle text
        prefix: Value prefix (e.g., '$')
        suffix: Value suffix (e.g., '%')
    """
    if isinstance(value, (int, float)):
        display_value = f"{prefix}{value:,.0f}{suffix}"
    else:
        display_value = f"{value}"
    
    subtitle_html = f'<p style="opacity: 0.7; margin-top: 0.5rem;">{subtitle}</p>' if subtitle else ''
    
    st.markdown(f"""
    <div class="card">
        <h3 style="margin-top: 0;">{title}</h3>
        <h2 style="color: {HIGHLIGHT_COLOR} !important; border: none; font-size: 2rem !important; margin: 0.5rem 0;">
            {display_value}
        </h2>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)

def render_pagination_dots(current_page, total_pages=4):
    """
    Renders pagination dots for navigation.
    
    Args:
        current_page: The current active page (0-based index)
        total_pages: Total number of pages
    """
    dots_html = ""
    for i in range(total_pages):
        active_class = " active" if i == current_page else ""
        dots_html += f'<span class="dot{active_class}"></span>'
    
    col_nav = st.columns([1, 3, 1])
    with col_nav[1]:
        st.markdown(f"""
        <div class="progress-dots">
            {dots_html}
        </div>
        """, unsafe_allow_html=True)

def render_navigation_buttons(current_page, change_page_func):
    """
    Renders navigation buttons for going between pages.
    
    Args:
        current_page: The current page index
        change_page_func: Function to call when changing pages
    """
    if current_page > 0 and current_page < 3:
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            prev_label = f"← Back to {['Overview', 'Detailed Metrics', 'Visualisations'][current_page-1]}"
            if st.button(prev_label):
                change_page_func(current_page - 1)
                st.rerun()
        with col_btn2:
            next_label = f"Continue to {['Detailed Metrics', 'Visualisations', 'Export'][current_page]}" + " →"
            if st.button(next_label):
                change_page_func(current_page + 1)
                st.rerun()
    elif current_page == 0:
        if st.button("View Detailed Metrics →"):
            change_page_func(1)
            st.rerun()
    elif current_page == 3:
        if st.button("← Back to Visualisations"):
            change_page_func(2)
            st.rerun() 