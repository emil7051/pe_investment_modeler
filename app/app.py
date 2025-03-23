import streamlit as st
# Import only what's needed initially to reduce startup time
import pandas as pd
import numpy as np

# Set page config first
st.set_page_config(
	page_title="PE Investment Analysis",
	page_icon="📈",
	layout="wide",
	initial_sidebar_state="expanded"
)

# Now import the PEInvestment model and basic utilities
from app.models import PEInvestment
from app.utils.data import create_export_dataframe, export_to_csv, export_to_excel

# Declare the visualization imports but don't import the functions yet
# This will be done lazily when the tabs are clicked
visualization_module = "app.utils.vizualization"

# Define brand colors for consistency
PARC_GREEN = '#34C759'  # More pure green, less teal
PARC_BLACK = '#121212'  # Dark gray instead of pure black
PARC_DARK_GRAY = '#1E1E1E'  # Slightly lighter gray
PARC_LIGHT_GRAY = '#2A2A2A'  # Medium gray
PARC_WHITE = '#F0F0F0'  # Off-white for reduced contrast

# Apply custom CSS for better styling
st.markdown("""
<style>
	.main .block-container {
		padding-top: 1.5rem;
		padding-bottom: 1.5rem;
		max-width: 1200px; /* Limit max width for better readability */
	}
	
	/* Parc brand styling */
	h1, h2, h3 {
		font-weight: 700 !important;
		font-family: 'Inter', 'Segoe UI', 'Helvetica', sans-serif !important;
	}
	
	h1 {
		margin-bottom: 1rem !important;
	}
	
	h2 {
		border-bottom: 2px solid """ + PARC_GREEN + """;
		padding-bottom: 0.5rem;
		margin-top: 1.5rem !important;
		color: """ + PARC_WHITE + """ !important;
	}
	
	p {
		line-height: 1.5;
	}
	
	/* Metrics styling */
	.stMetric {
		background-color: """ + PARC_DARK_GRAY + """;
		padding: 1.25rem;
		border-radius: 8px;
		border-left: 4px solid """ + PARC_GREEN + """;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}
	
	.stMetric > div {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}
	
	.stMetric label {
		font-size: 1.1rem !important;
		font-weight: 600 !important;
		color: """ + PARC_WHITE + """ !important;
		opacity: 0.9;
	}
	
	.stMetric [data-testid="stMetricValue"] {
		font-size: 2.2rem !important;
		font-weight: 700 !important;
		color: """ + PARC_GREEN + """ !important;
	}
	
	/* Header styling */
	[data-testid="stHeader"] {
		background-color: rgba(18, 18, 18, 0.8);
		backdrop-filter: blur(10px);
	}
	
	/* Sidebar styling */
	[data-testid="stSidebar"] {
		background-color: """ + PARC_BLACK + """;
		border-right: 1px solid """ + PARC_DARK_GRAY + """;
	}
	
	.sidebar .sidebar-content {
		background-color: """ + PARC_BLACK + """;
	}
	
	/* Tables styling */
	table {
		border-collapse: collapse;
		width: 100%;
	}
	
	thead th {
		background-color: """ + PARC_DARK_GRAY + """ !important;
		color: """ + PARC_GREEN + """ !important;
		font-weight: 600 !important;
	}
	
	tbody tr:nth-child(odd) {
		background-color: """ + PARC_BLACK + """ !important;
	}
	
	tbody tr:nth-child(even) {
		background-color: """ + PARC_DARK_GRAY + """ !important;
	}
	
	/* Tab styling */
	.stTabs [data-baseweb="tab-list"] {
		gap: 2px;
	}
	
	.stTabs [data-baseweb="tab"] {
		background-color: """ + PARC_DARK_GRAY + """;
		border-radius: 4px 4px 0 0;
		border: none;
		color: """ + PARC_WHITE + """;
		padding: 8px 16px;
	}
	
	.stTabs [aria-selected="true"] {
		background-color: """ + PARC_GREEN + """ !important;
		color: #121212 !important;
		font-weight: 600;
	}
	
	/* Button styling */
	.stButton>button {
		background-color: """ + PARC_GREEN + """;
		color: #121212;
		border: none;
		font-weight: 600;
		border-radius: 4px;
		padding: 0.5rem 1rem;
		transition: all 0.3s;
	}
	
	.stButton>button:hover {
		background-color: #2DAA4A;
		color: #FFFFFF;
	}
	
	.metric-positive [data-testid="stMetricDelta"] {
		color: """ + PARC_GREEN + """ !important;
	}
	
	.metric-negative [data-testid="stMetricDelta"] {
		color: #FF3B30 !important;
	}
	
	/* Chart improvements */
	.js-plotly-plot .plotly {
		background-color: transparent !important;
	}
	
	.js-plotly-plot .bg {
		fill: transparent !important;
	}
	
	/* Slider optimizations for better performance */
	.stSlider div[data-baseweb="slider"] {
		height: 6px;
	}
	
	.stSlider div[role="slider"] {
		background-color: """ + PARC_GREEN + """;
	}
	
	/* Footer styling */
	footer {
		border-top: 1px solid """ + PARC_DARK_GRAY + """;
		padding-top: 1rem;
		margin-top: 2rem;
		opacity: 0.8;
	}
</style>
""", unsafe_allow_html=True)

# App title and introduction
st.markdown("""
<div style="text-align: left; margin-bottom: 1.5rem;">
    <h1 style="color: """ + PARC_WHITE + """; margin-bottom: 0.5rem; font-weight: 700;">
        Private Equity Investment Analysis
        <span style="color: """ + PARC_GREEN + """;">.</span>
    </h1>
    <p style="color: """ + PARC_WHITE + """; opacity: 0.8; font-size: 1.1rem; max-width: 800px;">
        This app helps you model and visualise the performance of private equity investments. 
        Adjust the parameters in the sidebar to see how they affect the investment returns.
    </p>
</div>
""", unsafe_allow_html=True)

# Create sidebar for inputs
with st.sidebar:
	st.markdown("""
	<h2 style="color: """ + PARC_GREEN + """; font-weight: 700; margin-bottom: 1rem;">Investment Parameters</h2>
	""", unsafe_allow_html=True)
	
	st.markdown("""
	<h3 style="color: """ + PARC_WHITE + """; font-weight: 600; margin-bottom: 0.75rem; opacity: 0.9;">Entry Valuation</h3>
	""", unsafe_allow_html=True)
	
	initial_revenue = st.number_input(
		"Initial Revenue (AUD)",
		min_value=1000,
		value=10000000,
		step=1000000,
		format="%d"
	)
	
	initial_ebitda_margin = st.slider(
		"Initial EBITDA Margin (%)",
		min_value=0.0,
		max_value=50.0,
		value=15.0,
		step=0.5
	)
	
	entry_multiple = st.slider(
		"Entry Multiple",
		min_value=1.0,
		max_value=20.0,
		value=8.0,
		step=0.5
	)
	
	st.markdown("""
	<h3 style="color: """ + PARC_WHITE + """; font-weight: 600; margin-top: 1.25rem; margin-bottom: 0.75rem; opacity: 0.9;">Growth Assumptions</h3>
	""", unsafe_allow_html=True)
	
	revenue_growth = st.slider(
		"Annual Revenue Growth (%)",
		min_value=-10.0,
		max_value=50.0,
		value=10.0,
		step=0.5
	)
	
	holding_period = st.slider(
		"Holding Period (Years)",
		min_value=1,
		max_value=10,
		value=5
	)
	
	exit_ebitda_margin = st.slider(
		"Exit EBITDA Margin (%)",
		min_value=0.0,
		max_value=50.0,
		value=20.0,
		step=0.5
	)
	
	st.markdown("""
	<h3 style="color: """ + PARC_WHITE + """; font-weight: 600; margin-top: 1.25rem; margin-bottom: 0.75rem; opacity: 0.9;">Exit Assumptions</h3>
	""", unsafe_allow_html=True)
	
	exit_multiple = st.slider(
		"Exit Multiple",
		min_value=1.0,
		max_value=20.0,
		value=10.0,
		step=0.5
	)
	
	# Advanced options in an expander
	with st.expander("Advanced Options"):
		currency = st.selectbox(
			"Currency",
			options=["AUD", "USD", "EUR", "GBP"],
			index=0
		)
		
		currency_symbol = {
			"AUD": "AU$",
			"USD": "US$",
			"EUR": "€",
			"GBP": "£"
		}[currency]

# Create the investment model - this is fast and essential for all parts of the app
investment = PEInvestment(
	initial_revenue=initial_revenue,
	initial_ebitda_margin=initial_ebitda_margin,
	entry_multiple=entry_multiple,
	revenue_growth=revenue_growth,
	holding_period=holding_period,
	exit_ebitda_margin=exit_ebitda_margin,
	exit_multiple=exit_multiple
)

# Display main results in two columns
col1, col2 = st.columns(2)

with col1:
	st.markdown("""<h2>Entry Valuation</h2>""", unsafe_allow_html=True)
	entry_metrics = investment.get_entry_metrics()
	entry_df = pd.DataFrame(entry_metrics.items(), columns=["Metric", "Value"])
	st.table(entry_df)

with col2:
	st.markdown("""<h2>Exit Valuation</h2>""", unsafe_allow_html=True)
	exit_metrics = investment.get_exit_metrics()
	exit_df = pd.DataFrame(exit_metrics.items(), columns=["Metric", "Value"])
	st.table(exit_df)

# Display return metrics with visual emphasis
st.markdown("""<h2>Return Metrics</h2>""", unsafe_allow_html=True)
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

# Create tabs for different visualisations with lazy loading
tab1, tab2, tab3, tab4 = st.tabs([
	"Revenue Progression",
	"Value Bridge",
	"Sensitivity Analysis",
	"Parameter Impact"
])

# Tab 1: Revenue Progression - only load when selected
with tab1:
	st.markdown("""<h3>Revenue Progression Over Time</h3>""", unsafe_allow_html=True)
	
	# Only import the visualization function when the tab is used
	from app.utils.vizualization import create_revenue_progression_chart
	
	years, revenues = investment.get_revenue_progression()
	fig = create_revenue_progression_chart(years, revenues, currency=currency)
	st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# Tab 2: Value Bridge - only load when selected
with tab2:
	st.markdown("""<h3>Value Creation Bridge</h3>""", unsafe_allow_html=True)
	
	# Only import the visualization function when the tab is used
	from app.utils.vizualization import create_waterfall_chart
	
	# Calculate the components of value creation
	revenue_growth_impact = investment.exit_revenue * (investment.initial_ebitda_margin / 100) * investment.entry_multiple - investment.entry_price
	margin_improvement = investment.exit_revenue * ((investment.exit_ebitda_margin - investment.initial_ebitda_margin) / 100) * investment.entry_multiple
	multiple_expansion = investment.exit_ebitda * (investment.exit_multiple - investment.entry_multiple)
	
	changes = [revenue_growth_impact, margin_improvement, multiple_expansion]
	labels = ["Revenue Growth", "Margin Improvement", "Multiple Expansion"]
	
	fig = create_waterfall_chart(
		investment.entry_price,
		changes,
		labels,
		currency=currency_symbol
	)
	st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# Tab 3: Sensitivity Analysis - only load when selected
with tab3:
	st.markdown("""<h3>Sensitivity Analysis</h3>""", unsafe_allow_html=True)
	
	# Import the matplotlib visualization functions only when this tab is used
	from app.utils.vizualization import create_sensitivity_heatmap
	
	# Define deltas for sensitivity analysis
	growth_deltas = [-4, -2, 0, 2, 4]
	multiple_deltas = [-2, -1, 0, 1, 2]
	
	subtab1, subtab2 = st.tabs(["IRR Sensitivity", "Money Multiple Sensitivity"])
	
	# IRR Sensitivity
	with subtab1:
		st.markdown("""<h4>IRR Sensitivity: Revenue Growth vs Exit Multiple</h4>""", unsafe_allow_html=True)
		
		@st.cache_data  # Cache the matrix generation to avoid redundant calculations
		def get_irr_sensitivity_data(rev_growth, ex_multiple, growth_deltas, multiple_deltas):
			return investment.generate_sensitivity_matrix(
				'revenue_growth', rev_growth, growth_deltas,
				'exit_multiple', ex_multiple, multiple_deltas,
				'irr'
			)
		
		# Get cached sensitivity data
		irr_data = get_irr_sensitivity_data(revenue_growth, exit_multiple, growth_deltas, multiple_deltas)
		
		# Create row and column labels for the heatmap
		row_labels = [f"{revenue_growth + d}%" for d in growth_deltas]
		col_labels = [f"{exit_multiple + d}x" for d in multiple_deltas]
		
		# Create heatmap
		fig = create_sensitivity_heatmap(
			irr_data,
			row_labels,
			col_labels,
			"IRR Sensitivity (%)",
			fmt=".1f"
		)
		st.pyplot(fig)
	
	# Money Multiple Sensitivity
	with subtab2:
		st.markdown("""<h4>Money Multiple Sensitivity: Revenue Growth vs Exit Multiple</h4>""", unsafe_allow_html=True)
		
		@st.cache_data  # Cache the matrix generation to avoid redundant calculations
		def get_mm_sensitivity_data(rev_growth, ex_multiple, growth_deltas, multiple_deltas):
			return investment.generate_sensitivity_matrix(
				'revenue_growth', rev_growth, growth_deltas,
				'exit_multiple', ex_multiple, multiple_deltas,
				'money_multiple'
			)
		
		# Get cached sensitivity data
		mm_data = get_mm_sensitivity_data(revenue_growth, exit_multiple, growth_deltas, multiple_deltas)
		
		# Create row and column labels for the heatmap
		row_labels = [f"{revenue_growth + d}%" for d in growth_deltas]
		col_labels = [f"{exit_multiple + d}x" for d in multiple_deltas]
		
		# Create heatmap
		fig = create_sensitivity_heatmap(
			mm_data,
			row_labels,
			col_labels,
			"Money Multiple Sensitivity",
			fmt=".2f"
		)
		st.pyplot(fig)

# Tab 4: Parameter Impact - only load when selected
with tab4:
	st.markdown("""<h3>Parameter Impact Analysis</h3>""", unsafe_allow_html=True)
	
	# Only import the visualization function when the tab is used
	from app.utils.vizualization import create_tornado_chart
	
	# Define parameter deltas
	param_deltas = {
		'revenue_growth': [-5, 5],
		'initial_ebitda_margin': [-5, 5],
		'exit_ebitda_margin': [-5, 5],
		'entry_multiple': [-2, 2],
		'exit_multiple': [-2, 2],
		'holding_period': [-1, 1]
	}
	
	# Create parameter display names
	param_names = [
		'Revenue Growth',
		'Initial EBITDA Margin',
		'Exit EBITDA Margin',
		'Entry Multiple',
		'Exit Multiple',
		'Holding Period'
	]
	
	metric_selector = st.radio(
		"Select Metric",
		["IRR", "Money Multiple"],
		horizontal=True
	)
	
	@st.cache_data  # Cache the parameter sensitivity calculations
	def calculate_parameter_sensitivity(metric_type, params, deltas, inv_params):
		"""Cache the parameter sensitivity calculations"""
		if metric_type == "IRR":
			base_value = inv_params['irr'] * 100
			param_values = []
			
			for param_name in params:
				param_values.append([
					investment.calculate_sensitivity(param_name, inv_params[param_name], [deltas[param_name][0]], 'irr')[0],
					investment.calculate_sensitivity(param_name, inv_params[param_name], [deltas[param_name][1]], 'irr')[0]
				])
			return base_value, param_values
		else:
			base_value = inv_params['money_multiple']
			param_values = []
			
			for param_name in params:
				param_values.append([
					investment.calculate_sensitivity(param_name, inv_params[param_name], [deltas[param_name][0]], 'money_multiple')[0],
					investment.calculate_sensitivity(param_name, inv_params[param_name], [deltas[param_name][1]], 'money_multiple')[0]
				])
			return base_value, param_values
	
	# Get the investment parameters as a dictionary
	inv_params = {
		'revenue_growth': revenue_growth,
		'initial_ebitda_margin': initial_ebitda_margin,
		'exit_ebitda_margin': exit_ebitda_margin,
		'entry_multiple': entry_multiple,
		'exit_multiple': exit_multiple,
		'holding_period': holding_period,
		'irr': investment.irr,
		'money_multiple': investment.money_multiple
	}
	
	# Calculate base value and impact of each parameter using cached function
	base_value, param_values = calculate_parameter_sensitivity(
		metric_selector, 
		list(param_deltas.keys()), 
		param_deltas, 
		inv_params
	)
	
	# Create the tornado chart
	if metric_selector == "IRR":
		fig = create_tornado_chart(
			base_value,
			param_values,
			param_names,
			title="Impact on IRR (%)",
			metric_name="IRR (%)"
		)
	else:
		fig = create_tornado_chart(
			base_value,
			param_values,
			param_names,
			title="Impact on Money Multiple",
			metric_name="Money Multiple"
		)
	
	st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# Add export options
st.markdown(f"""
<h2 style="border-bottom: 2px solid {PARC_GREEN}; padding-bottom: 0.5rem; margin-top: 1.5rem;">
    Export Results
</h2>
""", unsafe_allow_html=True)

# Create a data frame for all results
@st.cache_data  # Cache the export data creation
def get_export_data(investment):
	return create_export_dataframe(investment)

results_df = get_export_data(investment)

# Add export buttons
export_col1, export_col2 = st.columns(2)

with export_col1:
	csv = export_to_csv(results_df)
	st.download_button(
		label="Download Results as CSV",
		data=csv,
		file_name=f"pe_investment_analysis_{currency}.csv",
		mime="text/csv",
	)

with export_col2:
	excel_data = export_to_excel(results_df)
	st.download_button(
		label="Download Results as Excel",
		data=excel_data,
		file_name=f"pe_investment_analysis_{currency}.xlsx",
		mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
	)

# Add footer
st.markdown(f"""
<footer>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 2rem; padding-top: 1.25rem; border-top: 1px solid {PARC_DARK_GRAY};">
        <div>
            <p style="color: {PARC_WHITE}; opacity: 0.7;">
                PE Investment Modeller by <span style="color: {PARC_GREEN};">Parc</span>
            </p>
        </div>
        <div style="text-align: right;">
            <p style="color: {PARC_WHITE}; opacity: 0.7;">
                Data is for illustrative purposes only
            </p>
        </div>
    </div>
</footer>
""", unsafe_allow_html=True)

# Run the main app
def main():
	try:
		# Nothing to do in main() since the app code is already executed
		pass
	except Exception as e:
		print(f"Error during app initialization: {e}")
		st.error(f"An error occurred during app initialization: {e}")

if __name__ == '__main__':
	main()
