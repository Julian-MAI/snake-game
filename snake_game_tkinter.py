import tkinter as tk
from tkinter import messagebox
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("贪吃蛇游戏")
        self.root.resizable(False, False)
        
        # 游戏参数
        self.cell_size = 20
        self.grid_width = 32
        self.grid_height = 24
        self.width = self.grid_width * self.cell_size
        self.height = self.grid_height * self.cell_size
        
        # 创建画布
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='black')
        self.canvas.pack()
        
        # 创建信息标签
        self.info_label = tk.Label(root, text="Score: 0  |  按 R 重新开始  按 Q 退出", 
                                   bg='black', fg='white', font=('Arial', 12))
        self.info_label.pack()
        
        # 绑定键盘事件
        self.root.bind('<Up>', self.on_key)
        self.root.bind('<Down>', self.on_key)
        self.root.bind('<Left>', self.on_key)
        self.root.bind('<Right>', self.on_key)
        self.root.bind('<r>', self.restart)
        self.root.bind('<R>', self.restart)
        self.root.bind('<q>', self.quit_game)
        self.root.bind('<Q>', self.quit_game)
        
        # 初始化游戏
        self.init_game()
        
        # 启动游戏循环
        self.game_loop()
    
    def init_game(self):
        """初始化游戏"""
        # 蛇的初始位置（坐标）
        self.snake = [(self.grid_width // 2, self.grid_height // 2)]
        self.direction = (1, 0)  # 向右
        self.next_direction = (1, 0)
        
        # 苹果位置
        self.apple = self.generate_apple()
        
        # 游戏状态
        self.score = 0
        self.game_over = False
    
    def generate_apple(self):
        """生成苹果"""
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if (x, y) not in self.snake:
                return (x, y)
    
    def on_key(self, event):
        """键盘事件处理"""
        if self.game_over:
            return
        
        if event.keysym == 'Up' and self.direction != (0, 1):
            self.next_direction = (0, -1)
        elif event.keysym == 'Down' and self.direction != (0, -1):
            self.next_direction = (0, 1)
        elif event.keysym == 'Left' and self.direction != (1, 0):
            self.next_direction = (-1, 0)
        elif event.keysym == 'Right' and self.direction != (-1, 0):
            self.next_direction = (1, 0)
    
    def restart(self, event=None):
        """重新开始游戏"""
        self.init_game()
    
    def quit_game(self, event=None):
        """退出游戏"""
        self.root.quit()
    
    def update(self):
        """更新游戏状态"""
        if self.game_over:
            return
        
        # 更新方向
        self.direction = self.next_direction
        
        # 计算新的蛇头位置
        head_x, head_y = self.snake[0]
        new_x = head_x + self.direction[0]
        new_y = head_y + self.direction[1]
        
        # 检查碰撞
        if (new_x < 0 or new_x >= self.grid_width or 
            new_y < 0 or new_y >= self.grid_height or
            (new_x, new_y) in self.snake):
            self.game_over = True
            return
        
        # 添加新头部
        self.snake.insert(0, (new_x, new_y))
        
        # 检查是否吃到苹果
        if (new_x, new_y) == self.apple:
            self.score += 10
            self.apple = self.generate_apple()
        else:
            # 没吃到则移除尾部
            self.snake.pop()
    
    def draw(self):
        """绘制游戏"""
        self.canvas.delete('all')
        
        # 绘制蛇
        for i, (x, y) in enumerate(self.snake):
            px = x * self.cell_size
            py = y * self.cell_size
            
            if i == 0:  # 蛇头
                self.canvas.create_rectangle(px, py, px + self.cell_size, py + self.cell_size,
                                            fill='yellow', outline='white')
            else:  # 蛇身
                self.canvas.create_rectangle(px, py, px + self.cell_size, py + self.cell_size,
                                            fill='lime', outline='white')
        
        # 绘制苹果
        apple_x = self.apple[0] * self.cell_size
        apple_y = self.apple[1] * self.cell_size
        self.canvas.create_oval(apple_x + 2, apple_y + 2,
                               apple_x + self.cell_size - 2, apple_y + self.cell_size - 2,
                               fill='red')
        
        # 更新信息
        if self.game_over:
            self.canvas.create_text(self.width // 2, self.height // 2,
                                   text='游戏结束！\nScore: {}\n\n按 R 重新开始'.format(self.score),
                                   font=('Arial', 20),
                                   fill='red')
            self.info_label.config(text=f"Score: {self.score}  |  游戏结束！按 R 重新开始")
        else:
            self.info_label.config(text=f"Score: {self.score}  |  按 R 重新开始  按 Q 退出")
    
    def game_loop(self):
        """游戏循环"""
        self.update()
        self.draw()
        self.root.after(100, self.game_loop)

if __name__ == '__main__':
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
