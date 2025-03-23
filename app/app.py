"""
PE Investment Modeller main application.
"""
import streamlit as st

# Set page config first
st.set_page_config(
	page_title="PE Investment Analysis",
	page_icon="📈",
	layout="wide",
	initial_sidebar_state="expanded"
)

# Import components
from app.models import PEInvestment
from app.ui.styles import get_css
from app.ui.components import render_header, render_footer, render_pagination_dots
from app.ui.sidebar import render_sidebar
from app.ui.pages import overview, detailed_metrics, visualizations, export

def main():
	"""Main entry point for the application."""
	try:
		# Apply CSS styling
		st.markdown(get_css(), unsafe_allow_html=True)
		
		# Render header
		render_header()
		
		# Get parameters from sidebar
		params = render_sidebar()
		
		# Create the investment model
		investment = PEInvestment(
			initial_revenue=params['initial_revenue'],
			initial_ebitda_margin=params['initial_ebitda_margin'],
			entry_multiple=params['entry_multiple'],
			revenue_growth=params['revenue_growth'],
			holding_period=params['holding_period'],
			exit_ebitda_margin=params['exit_ebitda_margin'],
			exit_multiple=params['exit_multiple']
		)
		
		# Set up pagination
		page_names = ["Overview", "Detailed Metrics", "Visualisations", "Export"]
		
		# Create session state for pagination if it doesn't exist
		if 'current_page' not in st.session_state:
			st.session_state.current_page = 0
		
		# Function to change page
		def change_page(page_index):
			st.session_state.current_page = page_index
		
		# Render pagination dots
		render_pagination_dots(st.session_state.current_page)
		
		# Render the appropriate page based on current_page
		current_page = st.session_state.current_page
		
		if current_page == 0:
			overview.render_page(investment, change_page)
		elif current_page == 1:
			detailed_metrics.render_page(investment, change_page)
		elif current_page == 2:
			visualizations.render_page(investment, params, change_page)
		elif current_page == 3:
			export.render_page(investment, params, change_page)
		
		# Render footer
		render_footer()
	
	except Exception as e:
		print(f"Error during app initialization: {e}")
		st.error(f"An error occurred during app initialization: {e}")

if __name__ == '__main__':
	main()
