import streamlit as st
import streamlit.components.v1 as components

# 頁面設定
st.set_page_config(page_title="Python Snake", layout="centered")
st.title("🐍 貪吃蛇 (Streamlit Web 版)")
st.write("請先點擊下方黑色的遊戲畫面，然後使用鍵盤的 **上、下、左、右** 開始遊戲！")

# 將原來的 Tkinter 邏輯轉換為 HTML5 + JavaScript
snake_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #ffffff;
        }
        canvas {
            background-color: #000000;
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
        }
    </style>
</head>
<body>
    <canvas id="gameCanvas" width="500" height="300"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        // 配置常量 (放大 BLOCK_SIZE 適應網頁)
        const BLOCK_SIZE = 20;
        const MAP_WIDTH = 25;
        const MAP_HEIGHT = 15;
        const COLOR = "#33AAFF";
        const FOOD_COLOR = "#FF3377";
        
        let snake = [];
        let food = {};
        let direction = "";
        let nextDirection = "";
        let speed = 100;
        let gameLoop;
        let gameStarted = false;
        let gameOver = false;

        function initGame() {
            let startX = Math.floor(MAP_WIDTH / 2);
            let startY = Math.floor(MAP_HEIGHT / 2) - 1;
            snake = [
                {x: startX, y: startY},
                {x: startX, y: startY + 1},
                {x: startX, y: startY + 2}
            ];
            placeFood();
            direction = "UP";
            nextDirection = "UP";
            speed = 100;
            gameOver = false;
            gameStarted = false;
            drawInitScreen();
        }

        function placeFood() {
            food = {
                x: Math.floor(Math.random() * MAP_WIDTH),
                y: Math.floor(Math.random() * MAP_HEIGHT)
            };
        }

        function drawBlock(x, y, color) {
            ctx.fillStyle = color;
            ctx.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
            // 畫個邊框讓蛇有立體感
            ctx.strokeStyle = "#000000";
            ctx.strokeRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
        }

        function drawInitScreen() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            // 畫蛇
            snake.forEach(segment => drawBlock(segment.x, segment.y, COLOR));
            // 文字
            ctx.fillStyle = "#ffffff";
            ctx.font = "20px Arial";
            ctx.textAlign = "center";
            ctx.fillText("Press Arrow Key To Start.", canvas.width / 2, canvas.height / 2);
        }

        function update() {
            if (gameOver) return;

            direction = nextDirection;
            let head = {x: snake[0].x, y: snake[0].y};

            if (direction === "LEFT") head.x -= 1;
            else if (direction === "UP") head.y -= 1;
            else if (direction === "RIGHT") head.x += 1;
            else if (direction === "DOWN") head.y += 1;

            // 死亡判定 (撞牆)
            if (head.x < 0 || head.x >= MAP_WIDTH || head.y < 0 || head.y >= MAP_HEIGHT) {
                endGame();
                return;
            }

            // 死亡判定 (撞自己)
            for (let i = 0; i < snake.length; i++) {
                if (snake[i].x === head.x && snake[i].y === head.y) {
                    endGame();
                    return;
                }
            }

            snake.unshift(head); // 加入新頭

            // 吃食物判定
            if (head.x === food.x && head.y === food.y) {
                placeFood();
                if (speed > 40) speed -= 5; // 加速
                clearInterval(gameLoop);
                gameLoop = setInterval(update, speed);
            } else {
                snake.pop(); // 沒吃到就移除尾巴
            }

            draw();
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawBlock(food.x, food.y, FOOD_COLOR);
            snake.forEach(segment => drawBlock(segment.x, segment.y, COLOR));
        }

        function endGame() {
            gameOver = true;
            clearInterval(gameLoop);
            ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#ffffff";
            ctx.font = "20px Arial";
            ctx.textAlign = "center";
            ctx.fillText("GameOver", canvas.width / 2, canvas.height / 2 - 15);
            ctx.fillText("Press Arrow Key To Replay.", canvas.width / 2, canvas.height / 2 + 15);
        }

        // 鍵盤監聽
        window.addEventListener("keydown", function(e) {
            // 防止按下方向鍵時畫面捲動
            if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight"].indexOf(e.code) > -1) {
                e.preventDefault();
            }

            if (gameOver) {
                initGame();
                return;
            }

            if (!gameStarted) {
                gameStarted = true;
                gameLoop = setInterval(update, speed);
            }

            if (e.code === "ArrowLeft" && direction !== "RIGHT") nextDirection = "LEFT";
            else if (e.code === "ArrowUp" && direction !== "DOWN") nextDirection = "UP";
            else if (e.code === "ArrowRight" && direction !== "LEFT") nextDirection = "RIGHT";
            else if (e.code === "ArrowDown" && direction !== "UP") nextDirection = "DOWN";
        });

        initGame();
    </script>
</body>
</html>
"""

# 將 HTML 嵌入 Streamlit，設定高度以容納 Canvas
components.html(snake_html, height=350)
