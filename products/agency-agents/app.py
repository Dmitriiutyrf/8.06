import streamlit as st
import os

st.set_page_config(page_title="Agency Agents PRO", page_icon="🤖", layout="wide")
st.title("🚀 Agency Agents PRO")
st.markdown("##### *Цифровая Фабрика: Инструмент для работы с ИИ*")

@st.cache_data
def get_agents():
    all_agents = []
    excluded = ['__pycache__', 'scripts', '.github', 'examples', 'integrations']
    categories = sorted([d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.') and d not in excluded])
    for cat in categories:
        try:
            for f in os.listdir(cat):
                if f.endswith('.md'):
                    all_agents.append({"name": f.replace('.md', '').replace('-', ' ').title(), "category": cat, "path": os.path.join(cat, f)})
        except: continue
    return all_agents

agents = get_agents()
st.sidebar.title("🔍 Поиск")
q = st.sidebar.text_input("Название или роль:")
filtered = [a for a in agents if not q or q.lower() in a['name'].lower()]

col1, col2 = st.columns([1, 2])
with col1:
    if filtered:
        sel = st.radio("Агенты:", [a['name'] for a in filtered], label_visibility="collapsed")
        agent = next(a for a in filtered if a['name'] == sel)
    else:
        st.write("Ничего не найдено")
        agent = None

if agent:
    with col2:
        st.subheader(agent['name'])
        with open(agent['path'], 'r') as f: content = f.read()
        t1, t2 = st.tabs(["👁 Инструкция", "🚀 Внедрение"])
        with t1: st.markdown(content)
        with t2:
            st.markdown("#### Экспорт")
            if st.button("Сгенерировать .cursorrules"): st.code(f"// Cursor\n\n{content}")
