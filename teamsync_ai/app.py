import streamlit as st
import os
from bridge import GNAPProtocol

st.set_page_config(page_title="TeamSync AI - Orchestrator", page_icon="🤖", layout="wide")

st.title("🤖 TeamSync AI")
st.markdown("### Git-Native Agent Orchestrator (GNAP 2026)")

gnap = GNAPProtocol()

st.sidebar.header("Agent Team")
st.sidebar.markdown("""
- 👨‍✈️ **Coordinator** (Claude Opus 4.6)
- 👨‍💻 **DevOps** (GPT-5)
- 📊 **Analyst** (Gemini 3.1)
- 🎨 **Designer** (Midjourney Agent)
""")

st.sidebar.markdown("""
---
**Dmitry Standard 2026**
- 📂 Serverless Board
- 🌐 Multi-Agent Sync
- 📈 Real-time VibeOps
""")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🆕 Create New Task")
    title = st.text_input("Task Title:")
    desc = st.text_area("Description:")
    assignee = st.selectbox("Assign to Agent:", ["Unassigned", "Coordinator", "DevOps", "Analyst", "Designer"])

    if st.button("Deploy Task to Board"):
        if title and desc:
            filename = gnap.create_task(title, desc)
            if assignee != "Unassigned":
                gnap.claim_task(filename, assignee)
            st.success(f"Task '{title}' deployed to Git Board.")
        else:
            st.error("Title and Description are required.")

with col2:
    st.subheader("📋 Task Board Status")
    status = gnap.get_status()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info("📅 TODO")
        for t in status["todo"]:
            st.text(f"📄 {t}")

    with c2:
        st.warning("⚡ DOING")
        for t in status["doing"]:
            st.text(f"🔥 {t}")
            if st.button(f"Done: {t}"):
                gnap.complete_task(t, "Task completed via GUI manually.")
                st.rerun()

    with c3:
        st.success("✅ DONE")
        for t in status["done"]:
            st.text(f"🏁 {t}")

st.markdown("---")
st.caption("GNAP Protocol | Part of the Shadow Suite Digital Factory")
