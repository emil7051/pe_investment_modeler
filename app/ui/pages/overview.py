"""
Contains the Overview page content.
"""
import streamlit as st
from app.ui.components import render_card

def render_page(investment):
    """
    Renders the Overview page.
    
    Args:
        investment: PEInvestment model instance
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
    
    # Investment details
    st.markdown("""<h3>Investment Details</h3>""", unsafe_allow_html=True)
    
    # Create two columns for the investment details cards
    col1, col2 = st.columns(2)
    
    with col1:
        render_card(
            "Entry Enterprise Value",
            investment.get_entry_enterprise_value(),
            "The initial purchase price of the company.",
            value_format="currency"
        )
        
        render_card(
            "Initial EBITDA",
            investment.get_initial_ebitda(),
            "The starting earnings before interest, taxes, depreciation, and amortization.",
            value_format="currency"
        )
        
    with col2:
        render_card(
            "Exit Enterprise Value",
            investment.get_exit_enterprise_value(),
            "The projected sale price at exit.",
            value_format="currency"
        )
        
        render_card(
            "Final EBITDA",
            investment.get_exit_ebitda(),
            "The projected EBITDA at the time of exit.",
            value_format="currency"
        ) 