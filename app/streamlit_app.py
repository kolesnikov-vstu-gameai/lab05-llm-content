import streamlit as st

from lab05.generators import STATS, gen_item, gen_quest, npc_reply

st.title("ЛР 5 — LLM-генерация контента")
tab1, tab2, tab3 = st.tabs(["Квест", "Предмет", "Диалог"])
with tab1:
    s = st.text_input("Сеттинг", "тёмное фэнтези, портовый город")
    if st.button("Сгенерировать квест"):
        st.json(gen_quest(s).model_dump())
with tab2:
    lvl = st.slider("Уровень", 1, 20, 5)
    if st.button("Сгенерировать предмет"):
        st.json(gen_item(s, lvl).model_dump())
with tab3:
    persona = st.selectbox("NPC", ["Торговец Барт — жадный, весёлый", "Стражница Ирма — строгая",
                                   "Старик Йор — загадочный"])
    if "hist" not in st.session_state:
        st.session_state.hist = []
    msg = st.chat_input("Реплика игрока")
    if msg:
        t = npc_reply(persona, st.session_state.hist, msg)
        st.session_state.hist += [{"role": "player", "text": msg}, {"role": "npc", "text": t.text}]
    for h in st.session_state.hist:
        st.chat_message("user" if h["role"] == "player" else "assistant").write(h["text"])
st.sidebar.metric("Валидных JSON", f"{STATS['valid']}/{STATS['calls']}")
