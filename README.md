# AI-Powered Application Validation — Demo

## Run locally
1. Install Python 3.10+.
2. In this folder run: `pip install -r requirements.txt`
3. Run: `streamlit run app.py`
4. Open the local URL shown by Streamlit.

OCR needs the Tesseract system executable. The app still works without OCR.

## Deploy to a website
Push these files to a GitHub repository, then create a new app on Streamlit Community Cloud and select `app.py`.

## Important
This is a demo prototype, not an official AICTE service. It checks form completeness and can optionally extract text from an image. It does not authenticate documents or connect to official databases. Use dummy data only until proper security, privacy, and verification integrations are implemented.
