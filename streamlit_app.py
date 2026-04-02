import streamlit as st

# 1. 初始化遊戲狀態 (避免重新渲染時數據丟失)
if 'chess_map' not in st.session_state:
    st.session_state.chess_map = [[0 for _ in range(19)] for _ in range(19)]
    st.session_state.black_turn = True
    st.session_state.game_over = False

def place_piece(r, c):
    if st.session_state.chess_map[r][c] == 0 and not st.session_state.game_over:
        # 1 代表黑棋，2 代表白棋
        st.session_state.chess_map[r][c] = 1 if st.session_state.black_turn else 2
        st.session_state.black_turn = not st.session_state.black_turn

def reset_game():
    st.session_state.chess_map = [[0 for _ in range(19)] for _ in range(19)]
    st.session_state.black_turn = True
    st.session_state.game_over = False

# --- UI 介面 ---
st.title("六子棋 Connect 6")

# 顯示目前輪到誰
current_player = "黑棋 ⚫" if st.session_state.black_turn else "白棋 ⚪"
st.subheader(f"當前回合: {current_player}")

if st.button("重置遊戲"):
    reset_game()
    st.rerun()

# 2. 繪製棋盤
# 使用 CSS 強制縮小按鈕間距，讓它看起來像棋盤
st.markdown("""
    <style>
    div.stButton > button {
        width: 30px !important;
        height: 30px !important;
        padding: 0 !important;
        margin: 0 !important;
        line-height: 30px !important;
    }
    </style>
""", unsafe_allow_html=True)

for r in range(19):
    cols = st.columns(19)
    for c in range(19):
        state = st.session_state.chess_map[r][c]
        label = "⚫" if state == 1 else ("⚪" if state == 2 else " ")
        # 點擊按鈕執行下棋
        cols[c].button(label, key=f"btn_{r}_{c}", on_click=place_piece, args=(r, c))
