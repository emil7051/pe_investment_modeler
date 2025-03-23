"""
Contains code for rendering and handling the sidebar inputs.
"""
import streamlit as st
from app.ui.styles import HIGHLIGHT_COLOR, LIGHT_COLOR

def render_sidebar():
    """
    Renders the sidebar with investment parameter inputs.
    
    Returns:
        dict: Dictionary of input parameters
    """
    with st.sidebar:
        st.markdown(f"""
        <h2 style="color: {HIGHLIGHT_COLOR}; font-weight: 500; margin-bottom: 1.5rem;">Investment Parameters</h2>
        """, unsafe_allow_html=True)
        
        # Entry Valuation
        st.markdown(f"""
        <h3 style="color: {LIGHT_COLOR}; font-weight: 400; margin-bottom: 1.2rem; opacity: 0.9;">Entry Valuation</h3>
        """, unsafe_allow_html=True)
        
        initial_revenue = st.number_input(
            "Initial Revenue (AUD)",
            min_value=1000,
            value=10000000,
            step=1000000,
            format="%d",
            help="The starting annual revenue of the company at acquisition."
        )
        
        initial_ebitda_margin = st.slider(
            "Initial EBITDA Margin (%)",
            min_value=0.0,
            max_value=50.0,
            value=15.0,
            step=0.5,
            help="The starting EBITDA margin (Earnings Before Interest, Taxes, Depreciation, and Amortisation) as a percentage of revenue."
        )
        
        entry_multiple = st.slider(
            "Entry Multiple",
            min_value=1.0,
            max_value=20.0,
            value=8.0,
            step=0.5,
            help="The EV/EBITDA multiple used to determine the acquisition price. Higher multiples mean higher purchase prices."
        )
        
        # Growth Assumptions
        st.markdown(f"""
        <h3 style="color: {LIGHT_COLOR}; font-weight: 400; margin-top: 2rem; margin-bottom: 1.2rem; opacity: 0.9;">Growth Assumptions</h3>
        """, unsafe_allow_html=True)
        
        revenue_growth = st.slider(
            "Annual Revenue Growth (%)",
            min_value=-10.0,
            max_value=50.0,
            value=10.0,
            step=0.5,
            help="The annual compound growth rate for revenue during the holding period."
        )
        
        holding_period = st.slider(
            "Holding Period (Years)",
            min_value=1,
            max_value=10,
            value=5,
            help="The number of years the investment will be held before exiting."
        )
        
        exit_ebitda_margin = st.slider(
            "Exit EBITDA Margin (%)",
            min_value=0.0,
            max_value=50.0,
            value=20.0,
            step=0.5,
            help="The projected EBITDA margin at exit, reflecting operational improvements during ownership."
        )
        
        # Exit Assumptions
        st.markdown(f"""
        <h3 style="color: {LIGHT_COLOR}; font-weight: 400; margin-top: 2rem; margin-bottom: 1.2rem; opacity: 0.9;">Exit Assumptions</h3>
        """, unsafe_allow_html=True)
        
        exit_multiple = st.slider(
            "Exit Multiple",
            min_value=1.0,
            max_value=20.0,
            value=10.0,
            step=0.5,
            help="The EV/EBITDA multiple applied at exit. Often higher than entry multiple due to company improvements and growth."
        )
        
        # Advanced options in an expander
        with st.expander("Advanced Options"):
            currency = st.selectbox(
                "Currency",
                options=["AUD", "USD", "EUR", "GBP"],
                index=0,
                help="The currency to use for all monetary values in the model."
            )
            
            currency_symbol = {
                "AUD": "AU$",
                "USD": "US$",
                "EUR": "€",
                "GBP": "£"
            }[currency]
    
    # Return all parameters as a dictionary
    return {
        'initial_revenue': initial_revenue,
        'initial_ebitda_margin': initial_ebitda_margin,
        'entry_multiple': entry_multiple,
        'revenue_growth': revenue_growth,
        'holding_period': holding_period,
        'exit_ebitda_margin': exit_ebitda_margin,
        'exit_multiple': exit_multiple,
        'currency': currency,
        'currency_symbol': currency_symbol
    } 