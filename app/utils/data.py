import pandas as pd
import numpy as np
import io
from typing import Dict, List, Any, Union

def format_currency(value, currency_symbol='$'):
	"""Format a number as currency"""
	return f'{currency_symbol}{value:,.0f}'

def format_percentage(value):
	"""Format a number as percentage"""
	return f'{value:.2f}%'

def format_multiple(value):
	"""Format a number as a multiple"""
	return f'{value:.2f}x'

def create_export_dataframe(investment_model):
	"""
	Create a DataFrame with all investment results for export.
	
	Args:
		investment_model: An instance of the PEInvestment class
		
	Returns:
		DataFrame with all model parameters and results
	"""
	# Get raw values for export (not formatted strings)
	data = {
		'Parameter': [
			'Initial Revenue', 'Initial EBITDA Margin', 'Initial EBITDA', 'Entry Multiple', 'Entry Price',
			'Revenue Growth', 'Holding Period', 'Exit Revenue', 'Exit EBITDA Margin', 'Exit EBITDA',
			'Exit Multiple', 'Exit Price', 'Money Multiple', 'IRR'
		],
		'Value': [
			investment_model.initial_revenue,
			investment_model.initial_ebitda_margin,
			investment_model.initial_ebitda,
			investment_model.entry_multiple,
			investment_model.entry_price,
			investment_model.revenue_growth,
			investment_model.holding_period,
			investment_model.exit_revenue,
			investment_model.exit_ebitda_margin,
			investment_model.exit_ebitda,
			investment_model.exit_multiple,
			investment_model.exit_price,
			investment_model.money_multiple,
			investment_model.irr * 100  # Convert to percentage
		]
	}
	
	# Format values appropriately
	formatted_values = []
	for param, value in zip(data['Parameter'], data['Value']):
		if 'Revenue' in param or 'EBITDA' in param or 'Price' in param:
			formatted_values.append(format_currency(value))
		elif 'Margin' in param or 'IRR' in param or 'Growth' in param:
			formatted_values.append(format_percentage(value))
		elif 'Multiple' in param:
			formatted_values.append(format_multiple(value))
		else:
			formatted_values.append(str(value))
	
	# Create DataFrame with raw and formatted values
	df = pd.DataFrame({
		'Parameter': data['Parameter'],
		'Raw Value': data['Value'],
		'Formatted Value': formatted_values
	})
	
	return df

def export_to_csv(df):
	"""
	Convert a DataFrame to CSV.
	
	Args:
		df: DataFrame to export
		
	Returns:
		CSV string
	"""
	# Use just the Parameter and Formatted Value columns for the CSV
	export_df = df[['Parameter', 'Formatted Value']].copy()
	export_df.columns = ['Parameter', 'Value']
	return export_df.to_csv(index=False)

def export_to_excel(df):
	"""
	Convert a DataFrame to Excel.
	
	Args:
		df: DataFrame to export
		
	Returns:
		Excel file as bytes
	"""
	output = io.BytesIO()
	with pd.ExcelWriter(output, engine='openpyxl') as writer:
		df.to_excel(writer, sheet_name='PE Investment Analysis', index=False)
	
	output.seek(0)
	return output.getvalue() 