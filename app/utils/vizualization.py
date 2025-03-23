import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import List, Dict, Tuple, Union

# Define Parc brand colors
PARC_GREEN = '#29B09D'
PARC_RED = '#EF553B'
PARC_BLACK = '#000000'
PARC_DARK_GRAY = '#0F0F0F'
PARC_LIGHT_GRAY = '#2A2A2A'
PARC_WHITE = '#FFFFFF'

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
			line=dict(color=PARC_GREEN, width=3),
			marker=dict(size=10, color=PARC_GREEN)
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
		paper_bgcolor='rgba(0,0,0,0)',
		plot_bgcolor='rgba(0,0,0,0)',
		font=dict(
			family="sans-serif",
			size=12,
			color=PARC_WHITE
		)
	)
	
	# Add a grid
	fig.update_xaxes(
		showgrid=True, 
		gridwidth=1, 
		gridcolor=PARC_LIGHT_GRAY,
		zeroline=False,
		showline=True,
		linewidth=1,
		linecolor=PARC_LIGHT_GRAY
	)
	fig.update_yaxes(
		showgrid=True, 
		gridwidth=1, 
		gridcolor=PARC_LIGHT_GRAY,
		zeroline=False,
		showline=True,
		linewidth=1,
		linecolor=PARC_LIGHT_GRAY
	)
	
	return fig

def create_sensitivity_heatmap(data, row_labels, col_labels, title, fmt='.2f', cmap='viridis'):
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
	# Set Matplotlib style to dark theme
	plt.style.use('dark_background')
	
	fig, ax = plt.subplots(figsize=(10, 6))
	fig.patch.set_facecolor(PARC_BLACK)
	
	# Create a DataFrame from the sensitivity data
	df = pd.DataFrame(data, index=row_labels, columns=col_labels)
	
	# Create a custom colormap that goes from dark to PARC_GREEN
	custom_cmap = sns.light_palette(PARC_GREEN, as_cmap=True)
	
	# Create the heatmap
	sns.heatmap(df, annot=True, fmt=fmt, cmap=custom_cmap, ax=ax, linewidths=.5, cbar_kws={'label': title.split(' ')[0]})
	ax.set_title(title, color=PARC_WHITE, fontsize=14, fontweight='bold')
	
	# Style the axis labels and ticks
	ax.set_xticklabels(ax.get_xticklabels(), color=PARC_WHITE)
	ax.set_yticklabels(ax.get_yticklabels(), color=PARC_WHITE)
	
	plt.tight_layout()
	
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
		connector={'line': {'color': PARC_LIGHT_GRAY}},
		increasing={'marker': {'color': PARC_GREEN}},
		decreasing={'marker': {'color': PARC_RED}},
		totals={'marker': {'color': PARC_GREEN}}
	))
	
	fig.update_layout(
		title=title,
		showlegend=False,
		height=500,
		paper_bgcolor='rgba(0,0,0,0)',
		plot_bgcolor='rgba(0,0,0,0)',
		font=dict(
			family="sans-serif",
			size=12,
			color=PARC_WHITE
		),
		yaxis_title=f'Value ({currency})',
		yaxis_tickformat=',.0f'
	)
	
	fig.update_xaxes(
		showgrid=False,
		zeroline=False,
		showline=True,
		linewidth=1,
		linecolor=PARC_LIGHT_GRAY
	)
	fig.update_yaxes(
		showgrid=True,
		gridwidth=1,
		gridcolor=PARC_LIGHT_GRAY,
		zeroline=False,
		showline=True,
		linewidth=1,
		linecolor=PARC_LIGHT_GRAY
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
		marker=dict(color=PARC_RED),
		showlegend=True
	))
	
	# Add bars for high values
	fig.add_trace(go.Bar(
		y=params,
		x=high_diff,
		name='Positive Impact',
		orientation='h',
		marker=dict(color=PARC_GREEN),
		showlegend=True
	))
	
	# Update layout
	fig.update_layout(
		title=title,
		xaxis_title=f'Change in {metric_name}',
		barmode='relative',
		height=500,
		paper_bgcolor='rgba(0,0,0,0)',
		plot_bgcolor='rgba(0,0,0,0)',
		font=dict(
			family="sans-serif",
			size=12,
			color=PARC_WHITE
		),
		legend=dict(
			orientation='h', 
			yanchor='bottom', 
			y=1.02, 
			xanchor='right', 
			x=1,
			font=dict(color=PARC_WHITE)
		)
	)
	
	# Add a vertical line at the base value
	fig.add_shape(
		type='line',
		x0=0, y0=-0.5,
		x1=0, y1=len(params)-0.5,
		line=dict(color=PARC_WHITE, width=2, dash='dash')
	)
	
	fig.update_xaxes(
		showgrid=True,
		gridwidth=1,
		gridcolor=PARC_LIGHT_GRAY,
		zeroline=False,
		showline=True,
		linewidth=1,
		linecolor=PARC_LIGHT_GRAY
	)
	fig.update_yaxes(
		showgrid=False,
		zeroline=False,
		showline=True,
		linewidth=1,
		linecolor=PARC_LIGHT_GRAY
	)
	
	return fig 