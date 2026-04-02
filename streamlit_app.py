import streamlit as st
import random as rand

# 這裡放入你之前的 Connect6Logic 類別 (純邏輯部分)
class Connect6Logic:
    def __init__(self):
        self.size = 19
        if 'chess_map' not in st.session_state:
            st.session_state.chess_map = [[0 for _ in range(19)] for _ in range(19)]
        if 'black_turn' not in st.session_state:
            st.session_state.black_turn = True

    def place_chess(self, x, y):
        if st.session_state.chess_map[x][y] == 0:
            st.session_state.chess_map[x][y] = 1 if st.session_state.black_turn else 2
            st.session_state.black_turn = not st.session_state.black_turn
            return True
        return False

# --- Streamlit 介面 ---
st.title("六子棋 Connect 6")

logic = Connect6Logic()

# 建立 19x19 的網格按鈕 (這只是一個簡易展示)
for i in range(19):
    cols = st.columns(19)
    for j in range(19):
        state = st.session_state.chess_map[i][j]
        label = "⚫" if state == 1 else ("⚪" if state == 2 else " ")
        if cols[j].button(label, key=f"{i}-{j}"):
            if logic.place_chess(i, j):
                st.rerun()
