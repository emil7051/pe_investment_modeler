# Private Equity Investment Modeler

A Streamlit application that helps model and visualise the performance of private equity investments.

## Features

- **Investment Parameter Inputs**: Set entry valuation, growth assumptions, and exit assumptions.
- **Performance Metrics**: Calculate key PE metrics like IRR and Money Multiple.
- **Interactive Visualisations**:
  - Revenue progression chart
  - Value creation bridge
  - Sensitivity analysis heatmaps
  - Parameter impact tornado charts
- **Export Options**: Download results as CSV or Excel files.

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd pe_investment_modeler
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running Locally

To run the app locally:

```bash
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`.

### Deployment to Streamlit Cloud

1. Create a Streamlit account at [streamlit.io](https://streamlit.io)
2. Connect your GitHub repository
3. Deploy the app by selecting your repository and branch

## Project Structure

- `app/`: Core application code
  - `app.py`: Main Streamlit application
  - `models.py`: Investment model logic
  - `utils/`: Utility functions
    - `data.py`: Data manipulation utilities
    - `vizualization.py`: Visualization utilities
- `main.py`: Entry point for the application
- `requirements.txt`: Python dependencies

## Customisation

- Modify the models in `app/models.py` to add additional investment logic
- Add new visualisations in `app/utils/vizualization.py`
- Extend the app interface in `app/app.py`
