"""
Constants used throughout the application.
This module centralizes styling constants, chart configurations, and other common values.
"""

# Import colors from styles for consistency
from app.ui.styles import (
    HIGHLIGHT_COLOR,
    BACKGROUND_COLOR,
    DARK_GRAY,
    MEDIUM_GRAY,
    LIGHT_COLOR,
    ERROR_COLOR
)

# Color aliases for visualization
PARC_GREEN = HIGHLIGHT_COLOR
PARC_RED = ERROR_COLOR
PARC_BLACK = BACKGROUND_COLOR
PARC_DARK_GRAY = DARK_GRAY
PARC_LIGHT_GRAY = MEDIUM_GRAY
PARC_WHITE = LIGHT_COLOR

# Chart configurations
PLOTLY_DEFAULT_CONFIG = {
    'displayModeBar': False,  # Hide mode bar for cleaner look
    'responsive': True  # Make plots responsive
}

# Common styling for plotly charts
PLOTLY_LAYOUT_DEFAULTS = {
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'font': dict(
        family="Roboto, sans-serif",
        size=12,
        color=PARC_WHITE
    ),
    'margin': dict(l=40, r=40, t=50, b=40)  # Tighter margins
}

# Default chart height
DEFAULT_CHART_HEIGHT = 450 