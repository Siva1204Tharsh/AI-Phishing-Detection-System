import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.title("🔐 AI Phishing Detection System")

st.markdown("Enter a message or email content to analyze:")

text = st.text_area("Message")
if st.button("Analyze"):
    response = requests.post(f"{API_URL}/predict_remediate", json={"message": text})
    result = response.json()

    if result["phishing"]:
        st.error("⚠️ Phishing detected!")
    else:
        st.success("✅ Message is safe.")

    st.subheader("💡 Recommended Actions:")
    for step in result["remediation"]["steps"]:
        st.markdown(f"- {step}")

st.subheader("📊 Recent Activity Log")
log_resp = requests.get(f"{API_URL}/logs")
if log_resp.ok:
    df_logs = pd.DataFrame(log_resp.json())
    st.dataframe(df_logs)
