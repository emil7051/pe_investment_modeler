import numpy as np

class PEInvestment:
	"""
	Private Equity Investment model that calculates various performance metrics.
	"""
	
	def __init__(self, initial_revenue, initial_ebitda_margin, entry_multiple,
			   revenue_growth, holding_period, exit_ebitda_margin, exit_multiple):
		self.initial_revenue = initial_revenue
		self.initial_ebitda_margin = initial_ebitda_margin
		self.entry_multiple = entry_multiple
		self.revenue_growth = revenue_growth
		self.holding_period = holding_period
		self.exit_ebitda_margin = exit_ebitda_margin
		self.exit_multiple = exit_multiple
		
		# Calculate derived values
		self._calculate_metrics()
	
	def _calculate_metrics(self):
		"""Calculate all investment metrics based on input parameters."""
		# Entry metrics
		self.initial_ebitda = self.initial_revenue * (self.initial_ebitda_margin / 100)
		self.entry_price = self.initial_ebitda * self.entry_multiple
		
		# Exit metrics
		self.exit_revenue = self.initial_revenue * (1 + self.revenue_growth / 100) ** self.holding_period
		self.exit_ebitda = self.exit_revenue * (self.exit_ebitda_margin / 100)
		self.exit_price = self.exit_ebitda * self.exit_multiple
		
		# Return metrics
		self.money_multiple = self.exit_price / self.entry_price
		self.irr = (self.money_multiple ** (1 / self.holding_period)) - 1
	
	def get_entry_metrics(self):
		"""Return a dictionary of entry metrics."""
		return {
			'Initial Revenue': f'${self.initial_revenue:,.0f}',
			'Initial EBITDA Margin': f'{self.initial_ebitda_margin:.1f}%',
			'Initial EBITDA': f'${self.initial_ebitda:,.0f}',
			'Entry Multiple': f'{self.entry_multiple:.1f}x',
			'Entry Price': f'${self.entry_price:,.0f}'
		}
	
	def get_exit_metrics(self):
		"""Return a dictionary of exit metrics."""
		return {
			'Exit Revenue': f'${self.exit_revenue:,.0f}',
			'Exit EBITDA Margin': f'{self.exit_ebitda_margin:.1f}%',
			'Exit EBITDA': f'${self.exit_ebitda:,.0f}',
			'Exit Multiple': f'{self.exit_multiple:.1f}x',
			'Exit Price': f'${self.exit_price:,.0f}'
		}
	
	def get_return_metrics(self):
		"""Return a dictionary of return metrics."""
		return {
			'Money Multiple': f'{self.money_multiple:.2f}x',
			'IRR': f'{self.irr*100:.2f}%'
		}
	
	def get_revenue_progression(self):
		"""Return yearly revenue progression over the holding period."""
		years = np.arange(0, self.holding_period + 1)
		revenues = [self.initial_revenue * (1 + self.revenue_growth / 100) ** year for year in years]
		return years, revenues
	
	def calculate_sensitivity(self, parameter_name, parameter_value, deltas, target_metric='irr'):
		"""
		Calculate sensitivity of a metric to changes in a parameter.
		
		Args:
			parameter_name: The parameter to vary (e.g., 'revenue_growth')
			parameter_value: The base value of the parameter
			deltas: List of deltas to apply to the parameter
			target_metric: Which metric to calculate sensitivity for ('irr' or 'money_multiple')
			
		Returns:
			List of calculated values for each delta
		"""
		results = []
		
		for delta in deltas:
			# Create a copy of the current instance with the modified parameter
			new_params = {
				'initial_revenue': self.initial_revenue,
				'initial_ebitda_margin': self.initial_ebitda_margin,
				'entry_multiple': self.entry_multiple,
				'revenue_growth': self.revenue_growth,
				'holding_period': self.holding_period,
				'exit_ebitda_margin': self.exit_ebitda_margin,
				'exit_multiple': self.exit_multiple
			}
			
			# Apply the delta to the specified parameter
			new_params[parameter_name] = parameter_value + delta
			
			# Create a new investment model with the modified parameter
			new_investment = PEInvestment(**new_params)
			
			# Get the requested metric
			if target_metric == 'irr':
				results.append(new_investment.irr * 100)  # Convert to percentage
			elif target_metric == 'money_multiple':
				results.append(new_investment.money_multiple)
				
		return results
	
	def generate_sensitivity_matrix(self, param1_name, param1_value, param1_deltas, 
									param2_name, param2_value, param2_deltas, 
									target_metric='irr'):
		"""
		Generate a sensitivity matrix for two parameters.
		
		Returns:
			2D array of values for each combination of deltas
		"""
		matrix = []
		
		for delta1 in param1_deltas:
			row = []
			
			for delta2 in param2_deltas:
				# Create a copy of the current instance with the modified parameters
				new_params = {
					'initial_revenue': self.initial_revenue,
					'initial_ebitda_margin': self.initial_ebitda_margin,
					'entry_multiple': self.entry_multiple,
					'revenue_growth': self.revenue_growth,
					'holding_period': self.holding_period,
					'exit_ebitda_margin': self.exit_ebitda_margin,
					'exit_multiple': self.exit_multiple
				}
				
				# Apply the deltas to the specified parameters
				new_params[param1_name] = param1_value + delta1
				new_params[param2_name] = param2_value + delta2
				
				# Create a new investment model with the modified parameters
				new_investment = PEInvestment(**new_params)
				
				# Get the requested metric
				if target_metric == 'irr':
					row.append(new_investment.irr * 100)  # Convert to percentage
				elif target_metric == 'money_multiple':
					row.append(new_investment.money_multiple)
					
			matrix.append(row)
				
		return matrix 