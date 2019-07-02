# Snake game for mPython
# MIT license,Copyright (c) 2019 labplus@Tangliufeng

from mpython import *
import random, time

WIDTH, HEIGHT = 127, 63


class Direction():
    """
    贪吃蛇方向,含上下左右
    """

    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class GameState():
    """
    游戏状态
    """
    PLAYING = 0
    PAUSE = 1
    WIN = 2
    FAIL = 3


class Snake():
    """
    贪吃蛇

    构建snake

    :param cube(int): 网格大小默认4
    """

    def __init__(self, cube=4):

        self.cube_width = cube
        self.grid_width_num, self.grid_height_num = WIDTH // self.cube_width, HEIGHT // self.cube_width
        self.snake_body = []
        self.snake_body.append((int(self.grid_width_num // 2 * self.cube_width),
                                int(self.grid_height_num // 2 * self.cube_width)))  # 添加贪吃蛇的“头”
        self.food_pos = self.generate_food()
        self.direction = Direction.LEFT

    def draw_grids(self):
        """
        绘制网格
        """
        for i in range(self.grid_width_num + 1):
            oled.vline(self.cube_width * i, 0, HEIGHT, 1)

        for i in range(self.grid_height_num + 1):
            oled.hline(0, self.cube_width * i, WIDTH, 1)

    def draw_body(self):
        """
        绘制snake
        """
        for sb in self.snake_body:
            # pygame.draw.rect(screen, WHITE, (sb[0], sb[1], CUBE_WIDTH, CUBE_WIDTH))
            oled.fill_rect(sb[0], sb[1], self.cube_width, self.cube_width, 1)

    def generate_food(self):
        """
        随机产生一个食物
        """
        self.food_pos = (random.randint(0, self.cube_width - 1), random.randint(0, self.grid_height_num - 1))
        return self.food_pos

    def draw_food(self):
        """
        绘制食物
        """
        oled.fill_rect(self.food_pos[0] * self.cube_width, self.food_pos[1] * self.cube_width, self.cube_width,
                       self.cube_width, 1)

    def grow(self):
        """
        判断贪吃蛇是否吃到了事物，如果吃到了我们就加长小蛇的身体
        """
        if self.snake_body[0][0] == self.food_pos[0] * self.cube_width and \
            self.snake_body[0][1] == self.food_pos[1] * self.cube_width:
            return True

        return False

    def refresh(self):
        """ 
        更新小蛇身体的位置
        """
        for i in range(len(self.snake_body) - 1, 0, -1):
            self.snake_body[i] = self.snake_body[i - 1]

    def move(self):
        """
        移动snake身体
        """
        if self.direction == Direction.UP:
            self.snake_body[0] = (self.snake_body[0][0], self.snake_body[0][1] - self.cube_width)

        elif self.direction == Direction.DOWN:
            self.snake_body[0] = (self.snake_body[0][0], self.snake_body[0][1] + self.cube_width)

        # top += cube_width
        elif self.direction == Direction.LEFT:

            self.snake_body[0] = (self.snake_body[0][0] - self.cube_width, self.snake_body[0][1])

        # left -= cube_width
        elif self.direction == Direction.RIGHT:
            self.snake_body[0] = (self.snake_body[0][0] + self.cube_width, self.snake_body[0][1])


class Game():
    """
    snake游戏控制
    """

    def __init__(self, fps=8):
        self.snake = Snake()
        self.get_body = self.snake.snake_body
        self.state = None
        self.fps = fps
        self.handles_cb = None

    def is_win(self):
        """
        判断是否赢
        """
        return len(self.get_body) == WIDTH * HEIGHT - 1

    def is_fail(self):
        """
        判断是否输
        """
        if not 0 <= self.get_body[0][0] < WIDTH or not 0 <= self.get_body[0][1] < HEIGHT:
            return True

        return False

    @property
    def score(self):
        """
        游戏分数
        """
        return len(self.get_body) - 1

    def handles_accele(self, threshold=0.2):
        """
        掌控板加速度控制
        """
        x = accelerometer.get_x()
        y = accelerometer.get_y()
        if y <= 1 and y >= -1:
            if abs(y) > threshold:
                if y > 0:
                    self.snake.direction = Direction.LEFT
                else:
                    self.snake.direction = Direction.RIGHT
        if x <= 1 and x >= -1:
            if abs(x) > threshold:
                if x > 0:
                    self.snake.direction = Direction.DOWN
                else:
                    self.snake.direction = Direction.UP

    def handles_callback(self, f):
        """
        游戏控制回调函数,可外部自定义控制方式
        """
        self.handles_cb = f

    def run(self):
        """
        游戏运行
        """
        self.state = GameState.PLAYING
        update_time = time.ticks_ms()

        while self.state == GameState.PLAYING:  # 游戏状态为PLAYING

            self.handles_cb()  # 游戏控制回调函数

            # 显示帧刷新,刷新方块位置
            if time.ticks_diff(time.ticks_ms(), update_time) > (1000 // self.fps):

                last_pos = self.get_body[-1]  # 这里需要保存一下尾部的位置，如果小蛇迟到了食物，需要在尾部增长

                self.snake.refresh()  # 更新小蛇身体的位置
                self.snake.move()  # 改变头部的位置

                if self.snake.grow():  # 判断小蛇是否吃到了事物，吃到了就成长,如果吃到了事物我们就产生一个新的食物
                    self.snake.generate_food()
                    self.get_body.append(last_pos)

                oled.fill(0)  # 清屏
                self.snake.draw_body()  # 画小蛇的身体
                self.snake.draw_food()  # 画出食物

                oled.show()  # 显示生效
                update_time = time.ticks_ms()  # 刷新帧时间

                if self.is_fail():  # 判断if输
                    self.state = GameState.FAIL
                    break
                if self.is_win():  # 判断if赢
                    self.state = GameState.WIN
                    break

        if self.state == GameState.FAIL:  # 输了,显示分数
            oled.fill(0)
            oled.text('Game over!', 25, 20)
            oled.text('Score:%d' % self.score, 25, 32)
            oled.show()

        if self.state == GameState.WIN:  # 赢了！
            oled.fill(0)
            oled.text('You win!', 25, 20)
            oled.show()


if __name__ == '__main__':
    game = Game(fps=8)
    game.handles_callback(game.handles_accele)
    game.run()