import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import optimize
import plotly.graph_objects as go

from app.models import PEInvestment
from app.utils.data import create_export_dataframe, export_to_csv, export_to_excel
from app.utils.vizualization import (
	create_revenue_progression_chart,
	create_sensitivity_heatmap,
	create_waterfall_chart,
	create_tornado_chart
)

# Set page config
st.set_page_config(
	page_title="PE Investment Analysis",
	page_icon="📈",
	layout="wide",
	initial_sidebar_state="expanded"
)

# Apply custom CSS for better styling
st.markdown("""
<style>
	.main .block-container {
		padding-top: 2rem;
		padding-bottom: 2rem;
	}
	.stMetric {
		background-color: #f0f2f6;
		padding: 15px;
		border-radius: 5px;
	}
	.stMetric > div {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}
	.stMetric label {
		font-size: 1.2rem !important;
		font-weight: 600 !important;
	}
	.stMetric [data-testid="stMetricValue"] {
		font-size: 2.5rem !important;
		font-weight: 700 !important;
	}
	[data-testid="stHeader"] {
		background-color: rgba(255, 255, 255, 0.8);
		backdrop-filter: blur(10px);
	}
	.metric-positive [data-testid="stMetricDelta"] {
		color: #29B09D !important;
	}
	.metric-negative [data-testid="stMetricDelta"] {
		color: #EF553B !important;
	}
</style>
""", unsafe_allow_html=True)

# App title
st.title("Private Equity Investment Analysis")
st.markdown("""
This app helps you model and visualise the performance of private equity investments.
Adjust the parameters in the sidebar to see how they affect the investment returns.
""")

# Create sidebar for inputs
with st.sidebar:
	st.header("Investment Parameters")
	
	st.subheader("Entry Valuation")
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
	
	st.subheader("Growth Assumptions")
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
	
	st.subheader("Exit Assumptions")
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


# Create the investment model
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
	st.header("Entry Valuation")
	entry_metrics = investment.get_entry_metrics()
	entry_df = pd.DataFrame(entry_metrics.items(), columns=["Metric", "Value"])
	st.table(entry_df)

with col2:
	st.header("Exit Valuation")
	exit_metrics = investment.get_exit_metrics()
	exit_df = pd.DataFrame(exit_metrics.items(), columns=["Metric", "Value"])
	st.table(exit_df)

# Display return metrics with visual emphasis
st.header("Return Metrics")
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

# Create tabs for different visualisations
tab1, tab2, tab3, tab4 = st.tabs([
	"Revenue Progression",
	"Value Bridge",
	"Sensitivity Analysis",
	"Parameter Impact"
])

# Tab 1: Revenue Progression
with tab1:
	st.subheader("Revenue Progression Over Time")
	
	years, revenues = investment.get_revenue_progression()
	fig = create_revenue_progression_chart(years, revenues, currency=currency)
	st.plotly_chart(fig, use_container_width=True)

# Tab 2: Value Bridge
with tab2:
	st.subheader("Value Creation Bridge")
	
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
	st.plotly_chart(fig, use_container_width=True)

# Tab 3: Sensitivity Analysis
with tab3:
	st.subheader("Sensitivity Analysis")
	
	# Define deltas for sensitivity analysis
	growth_deltas = [-4, -2, 0, 2, 4]
	margin_deltas = [-4, -2, 0, 2, 4]
	multiple_deltas = [-2, -1, 0, 1, 2]
	
	subtab1, subtab2 = st.tabs(["IRR Sensitivity", "Money Multiple Sensitivity"])
	
	# IRR Sensitivity
	with subtab1:
		st.subheader("IRR Sensitivity: Revenue Growth vs Exit Multiple")
		
		# Generate sensitivity matrix for IRR
		irr_data = investment.generate_sensitivity_matrix(
			'revenue_growth', revenue_growth, growth_deltas,
			'exit_multiple', exit_multiple, multiple_deltas,
			'irr'
		)
		
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
		st.subheader("Money Multiple Sensitivity: Revenue Growth vs Exit Multiple")
		
		# Generate sensitivity matrix for Money Multiple
		mm_data = investment.generate_sensitivity_matrix(
			'revenue_growth', revenue_growth, growth_deltas,
			'exit_multiple', exit_multiple, multiple_deltas,
			'money_multiple'
		)
		
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

# Tab 4: Parameter Impact
with tab4:
	st.subheader("Parameter Impact Analysis")
	
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
	
	# Calculate base value and impact of each parameter
	if metric_selector == "IRR":
		base_value = investment.irr * 100
		param_values = []
		
		for param_name, deltas in param_deltas.items():
			param_values.append([
				investment.calculate_sensitivity(param_name, getattr(investment, param_name), [deltas[0]], 'irr')[0],
				investment.calculate_sensitivity(param_name, getattr(investment, param_name), [deltas[1]], 'irr')[0]
			])
		
		fig = create_tornado_chart(
			base_value,
			param_values,
			param_names,
			title="Impact on IRR (%)",
			metric_name="IRR (%)"
		)
	else:
		base_value = investment.money_multiple
		param_values = []
		
		for param_name, deltas in param_deltas.items():
			param_values.append([
				investment.calculate_sensitivity(param_name, getattr(investment, param_name), [deltas[0]], 'money_multiple')[0],
				investment.calculate_sensitivity(param_name, getattr(investment, param_name), [deltas[1]], 'money_multiple')[0]
			])
		
		fig = create_tornado_chart(
			base_value,
			param_values,
			param_names,
			title="Impact on Money Multiple",
			metric_name="Money Multiple"
		)
	
	st.plotly_chart(fig, use_container_width=True)

# Add export options
st.header("Export Results")

# Create a data frame for all results
results_df = create_export_dataframe(investment)

# Add export buttons
col1, col2 = st.columns(2)

with col1:
	csv = export_to_csv(results_df)
	st.download_button(
		label="Download Results as CSV",
		data=csv,
		file_name=f"pe_investment_analysis_{currency}.csv",
		mime="text/csv",
	)

with col2:
	excel_data = export_to_excel(results_df)
	st.download_button(
		label="Download Results as Excel",
		data=excel_data,
		file_name=f"pe_investment_analysis_{currency}.xlsx",
		mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
	)

# Add footer
st.markdown("""
---
Created with ❤️ using Streamlit
""")

# Run the main app
def main():
	try:
		# For debugging purposes, print a message when the app starts
		print("App initialization started")
		
		# All the app code above will be executed when this file is imported
		print("App initialized successfully")
	except Exception as e:
		# Log any exceptions that occur during initialization
		print(f"Error during app initialization: {e}")
		st.error(f"An error occurred during app initialization: {e}")

if __name__ == '__main__':
	main()
