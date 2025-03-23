"""
Contains CSS styling for the application.
"""

# Brand colors - centralized for the entire application
# These can be imported by other modules
HIGHLIGHT_COLOR = '#01FDA2'  # PARC green
BACKGROUND_COLOR = '#121212'  # Dark background
DARK_GRAY = '#1E1E1E'       # Dark gray for panels
MEDIUM_GRAY = '#2A2A2A'     # Medium gray for secondary elements
LIGHT_COLOR = '#F5F5F5'     # Light color for text
ERROR_COLOR = '#FF3B30'     # Red for errors and negative values

def get_css():
    """
    Returns the CSS styling for the application.
    """
    return """
    <style>
    /* Global styles */
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif !important;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1000px;
    }
    
    /* Headers styling */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Roboto', sans-serif !important;
        font-weight: 500 !important;
        letter-spacing: 0.02em;
    }
    
    h1 {
        font-size: 2.2rem !important;
        margin-bottom: 1.5rem !important;
    }
    
    h2 {
        font-size: 1.5rem !important;
        color: """ + LIGHT_COLOR + """ !important;
        border-bottom: 2px solid """ + HIGHLIGHT_COLOR + """;
        padding-bottom: 0.8rem;
        margin-top: 2rem !important;
        margin-bottom: 1.5rem !important;
    }
    
    h3 {
        font-size: 1.3rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    p {
        line-height: 1.6;
        font-weight: 300;
    }
    
    /* Metrics styling */
    .stMetric {
        background-color: """ + DARK_GRAY + """;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid """ + HIGHLIGHT_COLOR + """;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        margin-bottom: 1rem;
    }
    
    .stMetric > div {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .stMetric label {
        font-size: 1.1rem !important;
        font-weight: 400 !important;
        color: """ + LIGHT_COLOR + """ !important;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: """ + HIGHLIGHT_COLOR + """ !important;
    }
    
    /* Header styling */
    [data-testid="stHeader"] {
        background-color: rgba(18, 18, 18, 0.95);
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: """ + BACKGROUND_COLOR + """;
        border-right: 1px solid """ + DARK_GRAY + """;
    }
    
    [data-testid="stSidebar"] .sidebar-content {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    [data-testid="stSidebar"] h3 {
        margin-top: 2rem !important;
        margin-bottom: 1.2rem !important;
        padding-top: 0.8rem;
        border-top: 1px solid """ + MEDIUM_GRAY + """;
    }
    
    [data-testid="stSidebar"] .stSlider {
        padding-top: 0.5rem;
        padding-bottom: 1.5rem;
    }
    
    [data-testid="stSidebar"] .stNumberInput {
        padding-bottom: 1.5rem;
    }
    
    /* Tables styling */
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 1.5rem 0;
    }
    
    thead th {
        background-color: """ + DARK_GRAY + """ !important;
        color: """ + HIGHLIGHT_COLOR + """ !important;
        font-weight: 500 !important;
        padding: 0.8rem !important;
    }
    
    tbody tr:nth-child(odd) {
        background-color: """ + BACKGROUND_COLOR + """ !important;
    }
    
    tbody tr:nth-child(even) {
        background-color: """ + DARK_GRAY + """ !important;
    }
    
    tbody td {
        padding: 0.8rem !important;
        border-bottom: 1px solid """ + MEDIUM_GRAY + """ !important;
    }
    
    /* Cards/containers */
    .card {
        background-color: """ + DARK_GRAY + """;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Buttons */
    .stButton button {
        background-color: """ + HIGHLIGHT_COLOR + """ !important;
        color: """ + BACKGROUND_COLOR + """ !important;
        font-weight: 500 !important;
        border: none !important;
        border-radius: 5px !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton button:hover {
        opacity: 0.9 !important;
        transform: translateY(-2px) !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background-color: """ + HIGHLIGHT_COLOR + """ !important;
    }
    
    /* Download button */
    .stDownloadButton button {
        background-color: """ + HIGHLIGHT_COLOR + """ !important;
        color: """ + BACKGROUND_COLOR + """ !important;
        font-weight: 500 !important;
        border: none !important;
        border-radius: 5px !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease !important;
    }
    
    .stDownloadButton button:hover {
        opacity: 0.9 !important;
        transform: translateY(-2px) !important;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding-top: 2rem;
        opacity: 0.7;
        font-size: 0.9rem;
    }
    
    /* Custom card layouts */
    .metric-card {
        background-color: """ + DARK_GRAY + """;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Progress indicators */
    .progress-dots {
        display: flex;
        justify-content: center;
        gap: 8px;
        margin: 2rem 0;
    }
    
    .dot {
        height: 10px;
        width: 10px;
        background-color: """ + MEDIUM_GRAY + """;
        border-radius: 50%;
        display: inline-block;
    }
    
    .dot.active {
        background-color: """ + HIGHLIGHT_COLOR + """;
    }
    </style>
    
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    """ 