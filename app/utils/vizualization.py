import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import List, Dict, Tuple, Union

def create_revenue_progression_chart(years, revenues, currency='AUD'):
	"""
	Create a plotly chart showing revenue progression over time.
	
	Args:
		years: Array of years
		revenues: Array of revenue values
		currency: Currency symbol to use
	
	Returns:
		Plotly figure object
	"""
	fig = go.Figure()
	
	# Add revenue line
	fig.add_trace(
		go.Scatter(
			x=years,
			y=revenues,
			mode='lines+markers',
			name='Revenue',
			line=dict(color='#1f77b4', width=3),
			marker=dict(size=10)
		)
	)
	
	# Format the y-axis to display currency values
	fig.update_layout(
		title='Revenue Progression Over Time',
		xaxis_title='Year',
		yaxis_title=f'Revenue ({currency})',
		yaxis_tickformat=',.0f',
		height=500,
		hovermode='x unified',
		template='plotly_white'
	)
	
	# Add a grid
	fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
	fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
	
	return fig

def create_sensitivity_heatmap(data, row_labels, col_labels, title, fmt='.2f', cmap='YlGnBu'):
	"""
	Create a sensitivity analysis heatmap.
	
	Args:
		data: 2D array of sensitivity values
		row_labels: Labels for rows (typically parameter 1 values)
		col_labels: Labels for columns (typically parameter 2 values)
		title: Chart title
		fmt: Format string for annotation values
		cmap: Colormap to use
	
	Returns:
		Matplotlib figure and axis
	"""
	fig, ax = plt.subplots(figsize=(10, 6))
	
	# Create a DataFrame from the sensitivity data
	df = pd.DataFrame(data, index=row_labels, columns=col_labels)
	
	# Create the heatmap
	sns.heatmap(df, annot=True, fmt=fmt, cmap=cmap, ax=ax, linewidths=.5)
	ax.set_title(title)
	
	return fig

def create_waterfall_chart(start_value, changes, labels, title='Value Creation Bridge', currency='AUD'):
	"""
	Create a waterfall chart showing the build-up of value.
	
	Args:
		start_value: Starting value
		changes: List of value changes
		labels: Labels for each change
		title: Chart title
		currency: Currency symbol to use
	
	Returns:
		Plotly figure object
	"""
	# Calculate the cumulative values
	values = [start_value] + changes
	cumulative = [start_value]
	for change in changes:
		cumulative.append(cumulative[-1] + change)
	
	# Create measure and text arrays
	measure = ['absolute'] + ['relative'] * len(changes)
	text = [f'{start_value:,.0f}'] + [f'{change:+,.0f}' for change in changes]
	labels = ['Entry Value'] + labels + ['Exit Value']
	
	# Add the final total
	measure.append('total')
	text.append(f'{cumulative[-1]:,.0f}')
	
	fig = go.Figure(go.Waterfall(
		name='Value Bridge',
		orientation='v',
		measure=measure,
		x=labels,
		textposition='outside',
		text=text,
		y=[start_value] + changes + [0],  # The final 0 is ignored when measure='total'
		connector={'line': {'color': 'rgb(63, 63, 63)'}},
		increasing={'marker': {'color': '#29B09D'}},
		decreasing={'marker': {'color': '#EF553B'}}
	))
	
	fig.update_layout(
		title=title,
		showlegend=False,
		height=500,
		template='plotly_white',
		yaxis_title=f'Value ({currency})',
		yaxis_tickformat=',.0f'
	)
	
	return fig

def create_tornado_chart(base_value, param_changes, param_names, title='Sensitivity Analysis', metric_name='IRR'):
	"""
	Create a tornado chart to show parameter sensitivity.
	
	Args:
		base_value: Base value of the metric
		param_changes: Dictionary of parameter name to [low_impact, high_impact]
		param_names: Display names for parameters
		title: Chart title
		metric_name: Name of the metric being displayed
	
	Returns:
		Plotly figure object
	"""
	# Sort the parameters by magnitude of impact
	sorted_indices = sorted(
		range(len(param_names)),
		key=lambda i: abs(param_changes[i][1] - param_changes[i][0]),
		reverse=True
	)
	
	# Reorder the data
	params = [param_names[i] for i in sorted_indices]
	changes = [param_changes[i] for i in sorted_indices]
	
	# Calculate low and high differences from base
	low_diff = [change[0] - base_value for change in changes]
	high_diff = [change[1] - base_value for change in changes]
	
	fig = go.Figure()
	
	# Add bars for low values
	fig.add_trace(go.Bar(
		y=params,
		x=low_diff,
		name='Negative Impact',
		orientation='h',
		marker=dict(color='#EF553B'),
		showlegend=True
	))
	
	# Add bars for high values
	fig.add_trace(go.Bar(
		y=params,
		x=high_diff,
		name='Positive Impact',
		orientation='h',
		marker=dict(color='#29B09D'),
		showlegend=True
	))
	
	# Update layout
	fig.update_layout(
		title=title,
		xaxis_title=f'Change in {metric_name}',
		barmode='relative',
		height=500,
		template='plotly_white',
		legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
	)
	
	# Add a vertical line at the base value
	fig.add_shape(
		type='line',
		x0=0, y0=-0.5,
		x1=0, y1=len(params)-0.5,
		line=dict(color='black', width=2, dash='dash')
	)
	
	return fig 