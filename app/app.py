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
from app.ui.components import render_header, render_footer
from app.ui.sidebar import render_sidebar
from app.ui.pages import overview, detailed_metrics, visualizations, export

def main():
	"""Main entry point for the application."""
	try:
		# Add a small script to help prevent MutationObserver errors
		st.markdown("""
		<script>
			// Small delay to ensure DOM is fully loaded
			document.addEventListener('DOMContentLoaded', function() {
				// This runs when the DOM is fully loaded
				console.log('DOM fully loaded');
			});
		</script>
		""", unsafe_allow_html=True)
		
		# Apply CSS styling - ensure unsafe_allow_html is set to True
		css = get_css()
		st.markdown(css, unsafe_allow_html=True)
		
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
		
		# Create tabs for main navigation
		tab_overview, tab_metrics, tab_viz, tab_export = st.tabs([
			"Overview", "Detailed Metrics", "Visualisations", "Export"
		])
		
		# Render the appropriate content in each tab
		with tab_overview:
			overview.render_page(investment)
		
		with tab_metrics:
			detailed_metrics.render_page(investment)
		
		with tab_viz:
			visualizations.render_page(investment, params)
		
		with tab_export:
			export.render_page(investment, params)
		
		# Render footer
		render_footer()
	
	except Exception as e:
		print(f"Error during app initialization: {e}")
		st.error(f"An error occurred during app initialization: {e}")

if __name__ == '__main__':
	main()
