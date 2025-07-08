import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

from modules.ai_detection import train_model
from modules.compliance_check import run_compliance_check

# Page title
st.title("\U0001F510 AIREN: AI-Powered IoT Threat Detection")

# Upload section
uploaded_file = st.file_uploader("Upload IoT Log CSV File", type=["csv"])

# Train the model
model = train_model()

if uploaded_file:
    # Read and display data
    df = pd.read_csv(uploaded_file)
    st.subheader("\U0001F4CA Uploaded Data")
    st.dataframe(df)

    # Preprocess data
    df['event_type'] = df['event_type'].astype('category').cat.codes
    df['device_id'] = df['device_id'].astype('category').cat.codes

    # Make predictions
    X = df[['device_id', 'event_type']]
    predictions = model.predict(X)
    df['Threat Prediction'] = ["\u26A0\uFE0F Yes" if p == 1 else "\u2705 Safe" for p in predictions]

    # Display predictions
    st.subheader("\U0001F50D Threat Detection Results")
    st.dataframe(df)

    # ✅ Save to log file
    output_log_path = "data/prediction_log.csv"
    df.to_csv(output_log_path, index=False)
    st.success(f"\U0001F4DD Predictions saved to: {output_log_path}")

    # ✅ Threat summary bar chart
    st.subheader("\U0001F4CA Threat Summary Chart")
    threat_counts = df['Threat Prediction'].value_counts()
    fig, ax = plt.subplots()
    ax.bar(threat_counts.index, threat_counts.values, color=['green', 'red'])
    ax.set_ylabel("Number of Logs")
    ax.set_title("Threat vs Safe Logs")
    st.pyplot(fig)

# 🛡️ Compliance Check Section
st.subheader("\U0001F6E1\uFE0F Compliance Check (GDPR / NIST)")
st.write("Select your current security practices:")

config = {
    "data_encrypted": st.checkbox("Is data encrypted?"),
    "user_consent": st.checkbox("Is user consent collected?"),
    "device_authentication": st.checkbox("Are devices authenticated?"),
    "audit_logs": st.checkbox("Are audit logs maintained?")
}

if st.button("Run Compliance Check"):
    result = run_compliance_check(config)

    st.markdown(f"**Compliance Score:** {result['score']}%")
    st.markdown(f"**Status:** {result['status']}")

    st.markdown("### Feedback:")
    if result["feedback"]:
        for fb in result["feedback"]:
            st.write(fb)
    else:
        st.success("\u2705 All checks passed. You're fully compliant!")

    # ✅ Compliance pie chart
    st.subheader("\U0001F370 Compliance Score Breakdown")
    comp_data = [result["score"], 100 - result["score"]]
    labels = ['Compliant %', 'Non-Compliant %']
    colors = ['blue', 'orange']

    fig2, ax2 = plt.subplots()
    ax2.pie(comp_data, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax2.axis('equal')
    st.pyplot(fig2)

