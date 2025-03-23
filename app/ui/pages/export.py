"""
Contains the Export page content.
"""
import streamlit as st
from app.utils.data import create_export_dataframe, export_to_csv, export_to_excel
from app.ui.components import render_navigation_buttons

def render_page(investment, params, change_page):
    """
    Renders the Export page.
    
    Args:
        investment: PEInvestment model instance
        params: Dictionary of input parameters
        change_page: Function to change pages
    """
    st.markdown("""<h2>Export Results</h2>""", unsafe_allow_html=True)
    
    # Create a data frame for all results
    @st.cache_data  # Cache the export data creation
    def get_export_data(_investment):
        return create_export_dataframe(_investment)
    
    results_df = get_export_data(investment)
    
    # Show a preview of the data
    st.markdown("""<h3>Data Preview</h3>""", unsafe_allow_html=True)
    st.dataframe(results_df[['Parameter', 'Formatted Value']], use_container_width=True)
    
    # Add export buttons
    st.markdown("""<h3>Download Options</h3>""", unsafe_allow_html=True)
    export_col1, export_col2 = st.columns(2)
    
    with export_col1:
        csv = export_to_csv(results_df)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name=f"pe_investment_analysis_{params['currency']}.csv",
            mime="text/csv",
        )
    
    with export_col2:
        excel_data = export_to_excel(results_df)
        st.download_button(
            label="Download as Excel",
            data=excel_data,
            file_name=f"pe_investment_analysis_{params['currency']}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    
    # Back button
    render_navigation_buttons(3, change_page) 