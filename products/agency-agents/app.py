import streamlit as st
import os

st.set_page_config(page_title="Agency Agents PRO", page_icon="🤖", layout="wide")
st.title("🚀 Agency Agents PRO")
st.markdown("##### *Цифровая Фабрика: Профессиональный инструмент для работы с ИИ*")

@st.cache_data
def get_all_agents():
    all_agents = []
    excluded = ['__pycache__', 'scripts', '.github', 'examples', 'integrations']
    categories = sorted([d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.') and d not in excluded])
    for cat in categories:
        try:
            for f in os.listdir(cat):
                if f.endswith('.md'):
                    all_agents.append({
                        "name": f.replace('.md', '').replace('-', ' ').title(),
                        "category": cat,
                        "path": os.path.join(cat, f)
                    })
        except: continue
    return all_agents

agents = get_all_agents()
st.sidebar.title("🔍 Поиск и Фильтры")
q = st.sidebar.text_input("Поиск по названию или роли:", placeholder="Например: Marketing...")
filtered = [a for a in agents if not q or q.lower() in a['name'].lower() or q.lower() in a['category'].lower()]

col1, col2 = st.columns([1, 2])
with col1:
    st.subheader(f"Найдено: {len(filtered)}")
    if filtered:
        sel_name = st.radio("Выберите агента:", [a['name'] for a in filtered], label_visibility="collapsed")
        selected = next(a for a in filtered if a['name'] == sel_name)
    else:
        st.write("Ничего не найдено")
        selected = None

if selected:
    with col2:
        st.subheader(selected['name'])
        with open(selected['path'], 'r') as f: content = f.read()
        tab1, tab2 = st.tabs(["👁 Просмотр", "🚀 Внедрение"])
        with tab1: st.markdown(content)
        with tab2:
            st.markdown("#### Экспорт для IDE")
            if st.button("Сгенерировать .cursorrules"):
                st.code(f"// .cursorrules for {selected['name']}\n\n{content}")
        st.download_button("📥 Скачать инструкцию", content, file_name=f"{selected['name']}.md")

st.markdown("---")
st.caption("Agency Agents PRO v2.0 - Сделано для Цифровой Фабрики")
