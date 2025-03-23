"""
Contains the Visualisations page content.
"""
import streamlit as st
from app.ui.components import render_navigation_buttons

def render_page(investment, params, change_page):
    """
    Renders the Visualisations page.
    
    Args:
        investment: PEInvestment model instance
        params: Dictionary of input parameters
        change_page: Function to change pages
    """
    st.markdown("""<h2>Investment Visualisations</h2>""", unsafe_allow_html=True)
    
    # Create tabs for different visualisations
    viz_tab1, viz_tab2, viz_tab3, viz_tab4 = st.tabs([
        "Revenue Progression",
        "Value Bridge",
        "Sensitivity Analysis",
        "Parameter Impact"
    ])
    
    # Tab 1: Revenue Progression
    with viz_tab1:
        render_revenue_progression(investment, params['currency'])
    
    # Tab 2: Value Bridge
    with viz_tab2:
        render_value_bridge(investment, params['currency_symbol'])
    
    # Tab 3: Sensitivity Analysis
    with viz_tab3:
        render_sensitivity_analysis(investment, params)
    
    # Tab 4: Parameter Impact
    with viz_tab4:
        render_parameter_impact(investment, params)
    
    # Navigation buttons
    render_navigation_buttons(2, change_page)

def render_revenue_progression(investment, currency):
    """Renders the revenue progression chart."""
    st.markdown("""<h3>Revenue Progression Over Time</h3>""", unsafe_allow_html=True)
    
    # Import visualization function
    from app.utils.vizualization import create_revenue_progression_chart
    
    years, revenues = investment.get_revenue_progression()
    fig = create_revenue_progression_chart(years, revenues, currency=currency)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def render_value_bridge(investment, currency_symbol):
    """Renders the value bridge chart."""
    st.markdown("""<h3>Value Creation Bridge</h3>""", unsafe_allow_html=True)
    
    # Import visualization function
    from app.utils.vizualization import create_waterfall_chart
    
    # Calculate value creation components
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

def render_sensitivity_analysis(investment, params):
    """Renders the sensitivity analysis charts."""
    st.markdown("""<h3>Sensitivity Analysis</h3>""", unsafe_allow_html=True)
    
    # Import visualization function
    from app.utils.vizualization import create_sensitivity_heatmap
    
    # Define deltas for sensitivity analysis
    growth_deltas = [-4, -2, 0, 2, 4]
    multiple_deltas = [-2, -1, 0, 1, 2]
    
    sensitivity_subtab1, sensitivity_subtab2 = st.tabs(["IRR Sensitivity", "Money Multiple Sensitivity"])
    
    revenue_growth = params['revenue_growth']
    exit_multiple = params['exit_multiple']
    
    # IRR Sensitivity
    with sensitivity_subtab1:
        st.markdown("""<h4>IRR Sensitivity: Revenue Growth vs Exit Multiple</h4>""", unsafe_allow_html=True)
        
        @st.cache_data  # Cache sensitivity data
        def get_irr_sensitivity_data(rev_growth, ex_multiple, growth_deltas, multiple_deltas):
            return investment.generate_sensitivity_matrix(
                'revenue_growth', rev_growth, growth_deltas,
                'exit_multiple', ex_multiple, multiple_deltas,
                'irr'
            )
        
        irr_data = get_irr_sensitivity_data(revenue_growth, exit_multiple, growth_deltas, multiple_deltas)
        row_labels = [f"{revenue_growth + d}%" for d in growth_deltas]
        col_labels = [f"{exit_multiple + d}x" for d in multiple_deltas]
        
        fig = create_sensitivity_heatmap(
            irr_data,
            row_labels,
            col_labels,
            "IRR Sensitivity (%)",
            fmt=".1f"
        )
        st.pyplot(fig)
    
    # Money Multiple Sensitivity
    with sensitivity_subtab2:
        st.markdown("""<h4>Money Multiple Sensitivity: Revenue Growth vs Exit Multiple</h4>""", unsafe_allow_html=True)
        
        @st.cache_data  # Cache sensitivity data
        def get_mm_sensitivity_data(rev_growth, ex_multiple, growth_deltas, multiple_deltas):
            return investment.generate_sensitivity_matrix(
                'revenue_growth', rev_growth, growth_deltas,
                'exit_multiple', ex_multiple, multiple_deltas,
                'money_multiple'
            )
        
        mm_data = get_mm_sensitivity_data(revenue_growth, exit_multiple, growth_deltas, multiple_deltas)
        row_labels = [f"{revenue_growth + d}%" for d in growth_deltas]
        col_labels = [f"{exit_multiple + d}x" for d in multiple_deltas]
        
        fig = create_sensitivity_heatmap(
            mm_data,
            row_labels,
            col_labels,
            "Money Multiple Sensitivity",
            fmt=".2f"
        )
        st.pyplot(fig)

def render_parameter_impact(investment, params):
    """Renders the parameter impact chart."""
    st.markdown("""<h3>Parameter Impact Analysis</h3>""", unsafe_allow_html=True)
    
    # Import visualization function
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
    
    @st.cache_data  # Cache parameter sensitivity calculations
    def calculate_parameter_sensitivity(metric_type, params, deltas, inv_params):
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
    
    # Get investment parameters as dictionary
    inv_params = {
        'revenue_growth': params['revenue_growth'],
        'initial_ebitda_margin': params['initial_ebitda_margin'],
        'exit_ebitda_margin': params['exit_ebitda_margin'],
        'entry_multiple': params['entry_multiple'],
        'exit_multiple': params['exit_multiple'],
        'holding_period': params['holding_period'],
        'irr': investment.irr,
        'money_multiple': investment.money_multiple
    }
    
    # Calculate parameter sensitivity
    base_value, param_values = calculate_parameter_sensitivity(
        metric_selector, 
        list(param_deltas.keys()), 
        param_deltas, 
        inv_params
    )
    
    # Create tornado chart
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