"""
Contains the Overview page content.
"""
import streamlit as st
from app.ui.components import render_card

def render_page(investment, change_page):
    """
    Renders the Overview page.
    
    Args:
        investment: PEInvestment model instance
        change_page: Function to change pages
    """
    st.markdown("""<h2>Investment Overview</h2>""", unsafe_allow_html=True)
    
    # Key metrics in a clean layout
    return_col1, return_col2 = st.columns(2)
    
    with return_col1:
        st.metric(
            "Money Multiple",
            investment.get_return_metrics()["Money Multiple"]
        )
    
    with return_col2:
        st.metric(
            "IRR",
            investment.get_return_metrics()["IRR"]
        )
    
    # Display entry price and exit price
    price_col1, price_col2 = st.columns(2)
    
    with price_col1:
        render_card(
            "Entry Investment", 
            investment.entry_price,
            f"Initial valuation based on {investment.entry_multiple:.1f}x multiple"
        )
    
    with price_col2:
        render_card(
            "Exit Value", 
            investment.exit_price,
            f"After {investment.holding_period} years with {investment.exit_multiple:.1f}x exit multiple"
        )
    
    # Next page button
    if st.button("View Detailed Metrics →"):
        change_page(1)
        st.experimental_rerun() 