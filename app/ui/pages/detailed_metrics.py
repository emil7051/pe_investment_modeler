"""
Contains the Detailed Metrics page content.
"""
import streamlit as st
import pandas as pd
from app.ui.components import render_navigation_buttons

def render_page(investment):
    """
    Renders the Detailed Metrics page.
    
    Args:
        investment: PEInvestment model instance
    """
    st.markdown("""<h2>Detailed Metrics</h2>""", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""<h3>Entry Valuation</h3>""", unsafe_allow_html=True)
        entry_metrics = investment.get_entry_metrics()
        entry_df = pd.DataFrame(entry_metrics.items(), columns=["Metric", "Value"])
        st.table(entry_df)
    
    with col2:
        st.markdown("""<h3>Exit Valuation</h3>""", unsafe_allow_html=True)
        exit_metrics = investment.get_exit_metrics()
        exit_df = pd.DataFrame(exit_metrics.items(), columns=["Metric", "Value"])
        st.table(exit_df) 