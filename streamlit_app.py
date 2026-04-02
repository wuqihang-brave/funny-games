import streamlit as st
import random as rand

# --- 1. 遊戲邏輯與 AI 函數 ---
def check_win(board, x, y, flag):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dx, dy in directions:
        count = 1
        for i in range(1, 6):
            nx, ny = x + dx * i, y + dy * i
            if 0 <= nx < 19 and 0 <= ny < 19 and board[nx][ny] == flag: count += 1
            else: break
        for i in range(1, 6):
            nx, ny = x - dx * i, y - dy * i
            if 0 <= nx < 19 and 0 <= ny < 19 and board[nx][ny] == flag: count += 1
            else: break
        if count >= 6: return True
    return False

def ai_move():
    # 簡單的 AI：優先找能連線最多的位置
    best_score = -1
    moves = []
    for x in range(19):
        for y in range(19):
            if st.session_state.chess_map[x][y] == 0:
                # 這裡簡化評分邏輯：找自己或對手最長連線處
                score = max(evaluate(x, y, 1), evaluate(x, y, 2)) 
                if score > best_score:
                    best_score = score
                    moves = [(x, y)]
                elif score == best_score:
                    moves.append((x, y))
    return rand.choice(moves) if moves else None

def evaluate(x, y, flag):
    # 模擬計算該位置在四個方向的最大連線數
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    max_c = 0
    for dx, dy in directions:
        c = 1
        for i in range(1, 6):
            nx, ny = x + dx*i, y + dy*i
            if 0<=nx<19 and 0<=ny<19 and st.session_state.chess_map[nx][ny] == flag: c+=1
            else: break
        max_c = max(max_c, c)
    return max_c

# --- 2. 初始化 Session State ---
if 'chess_map' not in st.session_state:
    st.session_state.chess_map = [[0 for _ in range(19)] for _ in range(19)]
    st.session_state.black_turn = True # 玩家先手 (黑)
    st.session_state.game_over = False
    st.session_state.status = "遊戲開始！玩家請落子"

# --- 3. 下棋動作 ---
def player_step(r, c):
    if st.session_state.chess_map[r][c] == 0 and not st.session_state.game_over:
        # 玩家落子 (黑棋)
        st.session_state.chess_map[r][c] = 1
        if check_win(st.session_state.chess_map, r, c, 1):
            st.session_state.status = "🎉 恭喜！你贏了！"
            st.session_state.game_over = True
        else:
            # 輪到電腦 (白棋)
            move = ai_move()
            if move:
                ar, ac = move
                st.session_state.chess_map[ar][ac] = 2
                if check_win(st.session_state.chess_map, ar, ac, 2):
                    st.session_state.status = "💀 電腦贏了，再接再厲！"
                    st.session_state.game_over = True
                else:
                    st.session_state.status = f"電腦下在 ({ar+1}, {ac+1})，輪到你了"

# --- 4. UI 介面 ---
st.set_page_config(page_title="Connect 6 AI", layout="centered")
st.title("六子棋：挑戰 AI")
st.write(st.session_state.status)

if st.button("重置遊戲"):
    st.session_state.chess_map = [[0 for _ in range(19)] for _ in range(19)]
    st.session_state.game_over = False
    st.session_state.status = "遊戲已重置"
    st.rerun()

# 調整 CSS 讓按鈕排版更緊湊
st.markdown("""
    <style>
    .stButton > button {
        width: 30px !important; height: 30px !important;
        padding: 0px !important; margin: 0px !important;
        font-size: 18px !important;
    }
    div[data-testid="column"] {
        width: 30px !important; flex: 0 0 30px !important;
        min-width: 30px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 渲染棋盤
for r in range(19):
    cols = st.columns(19)
    for c in range(19):
        val = st.session_state.chess_map[r][c]
        label = "⚫" if val == 1 else ("⚪" if val == 2 else " ")
        cols[c].button(label, key=f"b{r}_{c}", on_click=player_step, args=(r, c))
