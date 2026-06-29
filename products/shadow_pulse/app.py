import streamlit as st
from bridge import Scanner
import os

st.set_page_config(page_title="ShadowPulse", page_icon="🔍", layout="wide")

st.title("🔍 ShadowPulse")
st.markdown("### Deep OSINT Scanner & Market Insights")

# Sidebar for configuration
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("OpenRouter/OpenAI API Key (optional)", type="password")
if api_key:
    os.environ["OPENROUTER_API_KEY"] = api_key

st.sidebar.markdown("""
---
**Dmitry Standard Product**
- 🚀 One-click Scan
- 📊 Multi-source Analysis
- 💰 Business-ready Results
""")

# Main UI
query = st.text_input("Enter Topic, Brand, or Competitor:", placeholder="e.g. 'Cursor AI', 'OpenClaw vs Hermes', 'Nvidia earnings'")

if st.button("Run Intelligence Scan"):
    if not query:
        st.warning("Please enter a topic to scan.")
    else:
        with st.spinner(f"Scanning the web for '{query}'... This may take a minute."):
            scanner = Scanner()
            report = scanner.scan(query)

            st.markdown("---")
            st.markdown("## 📊 Intelligence Report")
            st.markdown(report)

            # Allow downloading the report
            st.download_button(
                label="Download Report as Markdown",
                data=report,
                file_name=f"OSINT_Report_{query.replace(' ', '_')}.md",
                mime="text/markdown"
            )

st.markdown("---")
st.caption("Powered by Last30Days Engine | Part of the Dmitry Standard Collection")
