import streamlit as st
import os

st.set_page_config(page_title="Agency Agents Explorer", layout="wide")

st.title("🤖 Agency Agents Explorer")
st.markdown("### Digital Factory: Upgrade Pack for AI Engineers")

categories = sorted([d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.') and d not in ['__pycache__']])

col1, col2 = st.columns([1, 3])

with col1:
    st.header("Categories")
    selected_cat = st.radio("Select a category:", categories)

if selected_cat:
    with col2:
        st.header(f"Agents in {selected_cat}")
        cat_path = selected_cat
        agents = [f for f in os.listdir(cat_path) if f.endswith('.md')]

        if not agents:
            st.write("No agents found in this category.")
        else:
            selected_agent = st.selectbox("Select an agent:", agents)

            if selected_agent:
                with open(os.path.join(cat_path, selected_agent), 'r') as f:
                    content = f.read()

                st.markdown("---")
                st.markdown(f"### Instruction for {selected_agent}")
                st.code(content, language='markdown')

                st.download_button(
                    label="Download Agent Instructions",
                    data=content,
                    file_name=selected_agent,
                    mime="text/markdown"
                )

st.sidebar.markdown("---")
st.sidebar.info("Select a category to explore specialized AI personas and their instructions.")
