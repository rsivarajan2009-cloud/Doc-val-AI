import streamlit as st
import re, io, json
from datetime import datetime
from PIL import Image
import pytesseract

st.set_page_config(page_title="AI Application & Document Checker", page_icon="🛡️", layout="wide")
st.title("🛡️ AI-Powered Application Validation")
st.caption("SIH-style prototype • Demo only — not an official AICTE service")
st.warning("Prototype notice: this demo performs basic form checks and optional OCR text extraction. It cannot prove that a certificate is genuine. Suspicious cases must be reviewed by an authorised person.")

with st.sidebar:
    st.header("How to use")
    st.write("1. Fill in the application details.")
    st.write("2. Upload a document image or PDF.")
    st.write("3. Review the flags and export a demo report.")
    st.caption("Use sample or dummy data only. Avoid uploading real sensitive documents.")

st.subheader("1. Applicant details")
c1, c2 = st.columns(2)
with c1:
    applicant_name = st.text_input("Applicant name")
    email = st.text_input("Email")
    application_id = st.text_input("Application ID")
with c2:
    age = st.number_input("Age", min_value=0, max_value=120, value=18)
    scheme = st.selectbox("Application type", ["Scholarship", "Admission", "Institutional grant", "Other"])
    declared_complete = st.checkbox("I have filled all required fields")

st.subheader("2. Document check")
uploaded = st.file_uploader("Upload a sample document image (PNG/JPG/JPEG) or PDF", type=["png","jpg","jpeg","pdf"])
use_ocr = st.checkbox("Try extracting text from image (OCR)", value=False)
ocr_text = ""
if uploaded:
    st.info(f"Uploaded: {uploaded.name} ({uploaded.size:,} bytes)")
    if uploaded.type == "application/pdf":
        st.caption("PDF preview/OCR is not enabled in this lightweight demo. You can still run the form checks.")
    else:
        try:
            img = Image.open(uploaded)
            st.image(img, caption="Uploaded document preview", width=420)
            if use_ocr:
                try:
                    ocr_text = pytesseract.image_to_string(img)
                    st.text_area("Extracted text (OCR may contain errors)", value=ocr_text, height=150)
                except Exception:
                    st.warning("OCR engine isn't available in this deployment. Form validation still works.")
        except Exception:
            st.error("Could not read this image file.")

if st.button("🔎 Validate application", type="primary"):
    issues = []
    if not applicant_name.strip():
        issues.append("Applicant name is missing.")
    if not email.strip() or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email.strip()):
        issues.append("Email is missing or does not look valid.")
    if not application_id.strip():
        issues.append("Application ID is missing.")
    if age < 16:
        issues.append("Applicant age is below 16; confirm the scheme's eligibility rules.")
    if not declared_complete:
        issues.append("Required-fields confirmation is not checked.")
    if not uploaded:
        issues.append("No supporting document was uploaded.")
    if uploaded and uploaded.size == 0:
        issues.append("Uploaded file is empty.")
    st.subheader("3. Validation results")
    if issues:
        st.error(f"{len(issues)} item(s) need attention")
        for issue in issues:
            st.write("• " + issue)
    else:
        st.success("No basic form issues found in this demo. This does NOT mean the document is authentic or the applicant is eligible.")
    if uploaded:
        st.info("Document authenticity: NOT VERIFIED. A trusted issuer/official database or human reviewer is required.")
    report = {
        "prototype": "AI-Powered Application Validation",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "application_id": application_id.strip(),
        "scheme": scheme,
        "basic_form_issues": issues,
        "document_authenticity": "NOT VERIFIED",
        "note": "Demo-only checks. Human review required for suspicious or high-stakes decisions."
    }
    st.download_button("⬇️ Download demo report (JSON)", data=json.dumps(report, indent=2), file_name="validation_report.json", mime="application/json")

st.divider()
st.subheader("What this prototype does / doesn't do")
a, b = st.columns(2)
with a:
    st.markdown("**Does**")
    st.write("- Checks required fields and email format")
    st.write("- Flags a simple age threshold for manual review")
    st.write("- Accepts a supporting document upload")
    st.write("- Can attempt OCR on an image")
with b:
    st.markdown("**Does not**")
    st.write("- Confirm a document is genuine")
    st.write("- Connect to AICTE or government databases")
    st.write("- Make official eligibility decisions")
    st.write("- Store or protect data like a production system")
