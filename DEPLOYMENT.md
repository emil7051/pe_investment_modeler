# Deploying to Streamlit Cloud

Follow these steps to deploy the PE Investment Modeler to Streamlit Cloud:

## Prerequisites

1. A GitHub account
2. This repository pushed to GitHub
3. A Streamlit Cloud account (sign up at [streamlit.io](https://streamlit.io))

## Deployment Steps

1. **Push to GitHub**:
   - Create a new GitHub repository
   - Push this code to the repository
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Connect to Streamlit Cloud**:
   - Log in to [Streamlit Cloud](https://streamlit.io)
   - Click "New app"
   - Select your GitHub repository
   - Set the main file path to `main.py`
   - Click "Deploy"

3. **Configure App Settings**:
   - Give your app a name
   - Select the branch to deploy from
   - Set any required secrets (none for this app)
   - Configure advanced settings if needed

4. **Share Your App**:
   - Once deployed, Streamlit will provide a public URL
   - Share this URL with stakeholders
   - Optionally, set up access controls if you need to restrict access

## Updating the App

To update your deployed app, simply push changes to your GitHub repository. Streamlit Cloud will automatically rebuild and redeploy the app.

```bash
git add .
git commit -m "Update app"
git push
```

## Monitoring

Streamlit Cloud provides basic app metrics in the dashboard, including:
- Number of viewers
- Runtime errors
- Resource usage

## Troubleshooting

If your app fails to deploy:

1. Check the logs in the Streamlit Cloud dashboard
2. Verify dependencies in `requirements.txt`
3. Ensure your main file (`main.py`) is correctly specified
4. Test locally before deploying: `streamlit run main.py` 