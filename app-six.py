import tkinter as tk
import random as rand

# --- 配置常量 ---
CONFIG = {
    "WINDOW_TITLE": "Python Connect 6",
    "CONNECT": 6,
    "MAP_SIZE": 19,
    "BLOCK_SIZE": 24,
    "BORDER_SIZE": 15,
    "TEXT_SIZE": 23,
    "COLORS": {
        "BG": "#AA8866",
        "TEXT_FG": "#FFFFFF",
        "TEXT_BG": "#000000",
        "WHITE": "#FFFFFF",
        "BLACK": "#000000"
    }
}

class Connect6Logic:
    """純遊戲邏輯類別，不依賴 tkinter，方便未來移植到 Streamlit"""
    def __init__(self):
        self.size = CONFIG["MAP_SIZE"]
        self.reset()

    def reset(self):
        self.chess_map = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.black_turn = True
        self.is_over = False

    def place_chess(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size and self.chess_map[x][y] == 0:
            flag = 1 if self.black_turn else 2
            self.chess_map[x][y] = flag
            win = self.check_win(x, y, flag)
            self.black_turn = not self.black_turn
            return True, win
        return False, False

    def check_win(self, x, y, flag):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            # 正向檢查
            for i in range(1, CONFIG["CONNECT"]):
                nx, ny = x + dx * i, y + dy * i
                if 0 <= nx < self.size and 0 <= ny < self.size and self.chess_map[nx][ny] == flag:
                    count += 1
                else: break
            # 反向檢查
            for i in range(1, CONFIG["CONNECT"]):
                nx, ny = x - dx * i, y - dy * i
                if 0 <= nx < self.size and 0 <= ny < self.size and self.chess_map[nx][ny] == flag:
                    count += 1
                else: break
            if count >= CONFIG["CONNECT"]:
                return True
        return False

    def get_ai_move(self):
        """簡單 AI：搜尋目前分數最高的位置"""
        best_score = -1
        best_pos = (rand.randint(0, 18), rand.randint(0, 18))
        
        # 這裡簡化原始邏輯，優先攻擊(自己連線)或防禦(對手連線)
        for f in [1, 2]: # 檢查黑白雙方潛在威脅
            for x in range(self.size):
                for y in range(self.size):
                    if self.chess_map[x][y] == 0:
                        # 模擬放置並計算連線數 (此處使用簡化評分)
                        score = self.evaluate_pos(x, y, f)
                        if score > best_score:
                            best_score = score
                            best_pos = (x, y)
        return best_pos

    def evaluate_pos(self, x, y, flag):
        # 簡單模擬原始的 result 邏輯
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        max_c = 0
        for dx, dy in directions:
            c = 1
            for i in range(1, 6):
                nx, ny = x+dx*i, y+dy*i
                if 0<=nx<19 and 0<=ny<19 and self.chess_map[nx][ny]==flag: c+=1
                else: break
            for i in range(1, 6):
                nx, ny = x-dx*i, y-dy*i
                if 0<=nx<19 and 0<=ny<19 and self.chess_map[nx][ny]==flag: c+=1
                else: break
            max_c = max(max_c, c)
        return max_c

# --- GUI 介面類別 ---
class GameGUI:
    def __init__(self, root):
        self.root = root
        self.logic = Connect6Logic()
        self.computer_starts = True
        
        # 計算視窗大小
        self.w_val = (CONFIG["MAP_SIZE"] - 1) * CONFIG["BLOCK_SIZE"] + CONFIG["BORDER_SIZE"] * 2
        self.h_val = self.w_val + CONFIG["TEXT_SIZE"]
        
        self.canvas = tk.Canvas(root, width=self.w_val, height=self.h_val, bg=CONFIG["COLORS"]["BG"])
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)
        
        self.init_board()

    def init_board(self):
        self.logic.reset()
        self.canvas.delete("all")
        # 畫線
        for i in range(CONFIG["MAP_SIZE"]):
            # 橫線
            offset = CONFIG["BORDER_SIZE"] + i * CONFIG["BLOCK_SIZE"]
            self.canvas.create_line(CONFIG["BORDER_SIZE"], offset, self.w_val - CONFIG["BORDER_SIZE"], offset)
            # 直線
            self.canvas.create_line(offset, CONFIG["BORDER_SIZE"], offset, self.w_val - CONFIG["BORDER_SIZE"])
        
        # 底部文字區
        self.canvas.create_rectangle(0, self.w_val, self.w_val, self.h_val, fill=CONFIG["COLORS"]["TEXT_BG"])
        self.update_msg("Game Started!")

        if self.computer_starts:
            self.ai_turn()

    def update_msg(self, msg):
        self.canvas.delete("msg")
        self.canvas.create_text(5, self.h_val - 5, text=msg, fill=CONFIG["COLORS"]["TEXT_FG"], anchor=tk.SW, tags="msg")

    def draw_stone(self, x, y, color_code):
        px = CONFIG["BORDER_SIZE"] + x * CONFIG["BLOCK_SIZE"] - CONFIG["BLOCK_SIZE"] / 2
        py = CONFIG["BORDER_SIZE"] + y * CONFIG["BLOCK_SIZE"] - CONFIG["BLOCK_SIZE"] / 2
        color = CONFIG["COLORS"]["BLACK"] if color_code == 1 else CONFIG["COLORS"]["WHITE"]
        self.canvas.create_oval(px, py, px + CONFIG["BLOCK_SIZE"], py + CONFIG["BLOCK_SIZE"], fill=color)

    def handle_click(self, event):
        if self.logic.is_over:
            self.computer_starts = not self.computer_starts
            self.init_board()
            return

        x = int((event.x - CONFIG["BORDER_SIZE"]) / CONFIG["BLOCK_SIZE"] + 0.5)
        y = int((event.y - CONFIG["BORDER_SIZE"]) / CONFIG["BLOCK_SIZE"] + 0.5)
        
        if 0 <= x < 19 and 0 <= y < 19:
            success, win = self.logic.place_chess(x, y)
            if success:
                self.draw_stone(x, y, 2 if self.logic.black_turn else 1) # 畫剛才下的那步
                if win:
                    self.update_msg("You Win! Click to restart.")
                    self.logic.is_over = True
                else:
                    self.ai_turn()

    def ai_turn(self):
        x, y = self.logic.get_ai_move()
        success, win = self.logic.place_chess(x, y)
        if success:
            self.draw_stone(x, y, 2 if self.logic.black_turn else 1)
            if win:
                self.update_msg("Computer Wins! Click to restart.")
                self.logic.is_over = True

if __name__ == "__main__":
    root = tk.Tk()
    root.title(CONFIG["WINDOW_TITLE"])
    gui = GameGUI(root)
    root.mainloop()