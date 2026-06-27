import streamlit as st
from engine import HunterEngine
import os

st.set_page_config(page_title="TrendSniper Dashboard", page_icon="🎯", layout="wide")

st.title("🎯 TrendSniper")
st.markdown("### Daily Open-Source & AI Opportunity Scout")

st.sidebar.header("Settings")
query = st.sidebar.text_input("Niche Filter:", value="AI")
hunt_button = st.sidebar.button("Start Daily Hunt")

st.sidebar.markdown("""
---
**Dmitry Standard Hunter**
- 🔍 GitHub Trending
- 📰 Hacker News Hype
- 🐈 Product Hunt Top
""")

engine = HunterEngine()

if hunt_button:
    with st.spinner("Hunting for opportunities..."):
        results = engine.hunt(query)

        if not results:
            st.warning("No trending projects found for this niche.")
        else:
            st.success(f"Found {len(results)} potential products!")

            for i, project in enumerate(results):
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"### {i+1}. [{project['name']}]({project['url']})")
                        st.write(f"**Source:** {project['source']} | **Hype Score:** {project['stars']}")
                        st.write(f"*{project['description']}*")
                    with col2:
                        st.info("**Monetization Idea**")
                        st.write(engine.analyze_monetization(project))
                    st.markdown("---")
else:
    st.info("Click 'Start Daily Hunt' in the sidebar to scan for today's top opportunities.")

st.markdown("---")
st.caption("Part of the Dmitry Digital Factory | Powered by TrendSniper v1.0")
