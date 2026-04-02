import streamlit as st
import random as rand

# --- 1. 大腦升級：稍強一點的 AI 邏輯 ---
def evaluate_board(board, x, y, flag):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    max_count = 0
    for dx, dy in directions:
        count = 1
        # 正向
        for i in range(1, 6):
            nx, ny = x + dx*i, y + dy*i
            if 0<=nx<19 and 0<=ny<19 and board[nx][ny] == flag: count += 1
            else: break
        # 反向
        for i in range(1, 6):
            nx, ny = x - dx*i, y - dy*i
            if 0<=nx<19 and 0<=ny<19 and board[nx][ny] == flag: count += 1
            else: break
        max_count = max(max_count, count)
    return max_count

def ai_move():
    best_score = -1
    best_moves = []
    # 遍歷棋盤找最佳點
    for r in range(19):
        for c in range(19):
            if st.session_state.chess_map[r][c] == 0:
                # 攻擊分數 (自己連線) + 防禦分數 (堵截玩家)
                score = evaluate_board(st.session_state.chess_map, r, c, 2) * 1.1 + \
                        evaluate_board(st.session_state.chess_map, r, c, 1)
                if score > best_score:
                    best_score = score
                    best_moves = [(r, c)]
                elif score == best_score:
                    best_moves.append((r, c))
    return rand.choice(best_moves) if best_moves else None

# --- 2. 視覺升級：復用木質棋盤風格 ---
st.markdown("""
    <style>
    .board-container {
        background-color: #AA8866;  /* 復用你原來的 BG_COLOR */
        padding: 10px;
        border-radius: 5px;
        display: inline-block;
    }
    /* 這裡微調按鈕樣式，讓它圓潤一點像棋子 */
    .stButton > button {
        border-radius: 50% !important;
        width: 25px !important;
        height: 25px !important;
        background-color: rgba(255,255,255,0.1) !important;
        border: 1px solid #886644 !important;
        color: transparent !important;
        padding: 0 !important;
    }
    .stButton > button:hover {
        border-color: #000 !important;
    }
    /* 黑白子樣式 */
    button[kind="primary"] { background-color: #000 !important; color: #000 !important; opacity: 1 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. 遊戲狀態與邏輯 ---
if 'chess_map' not in st.session_state:
    st.session_state.chess_map = [[0 for _ in range(19)] for _ in range(19)]
    st.session_state.game_over = False

def handle_click(r, c):
    if st.session_state.chess_map[r][c] == 0 and not st.session_state.game_over:
        st.session_state.chess_map[r][c] = 1 # 玩家下黑棋
        # 電腦立刻回應
        move = ai_move()
        if move:
            st.session_state.chess_map[move[0]][move[1]] = 2

# --- 4. 渲染 ---
st.title("六子棋：復刻版介面")
with st.container():
    st.write("目前狀態：玩家 vs AI (強攻型)")
    for r in range(19):
        cols = st.columns(19)
        for c in range(19):
            val = st.session_state.chess_map[r][c]
            # 根據棋子狀態顯示不同符號
            icon = " "
            if val == 1: icon = "⚫"
            if val == 2: icon = "⚪"
            
            cols[c].button(icon, key=f"{r}-{c}", on_click=handle_click, args=(r, c))
