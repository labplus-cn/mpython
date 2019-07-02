# Flappy Bird game for mPython
# frok from github.com/zelacerda/micropython ,2017 - by zelacerda
# modify from LabPlus@Tangliufeng

from mpython import *
from framebuf import FrameBuffer
import framebuf
import time, uos,urandom

# 16 x 12
BIRD = bytearray([
    0x7, 0xe0, 0x18, 0xf0, 0x21, 0xf8, 0x71, 0xec, 0xf9, 0xec, 0xfc, 0xfc, 0xbe, 0x7e, 0x4c, 0x81, 0x71, 0x7e, 0x40,
    0x82, 0x30, 0x7c, 0xf, 0x80
])

# 16 x 32
PIPE_TOP = bytearray([
    0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20,
    0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c,
    0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0xff, 0xff, 0x80, 0xf, 0x80,
    0xf, 0x80, 0xf, 0x80, 0xf, 0xff, 0xff
])
PIPE_DOWN = bytearray([
    0xff, 0xff, 0x80, 0xf, 0x80, 0xf, 0x80, 0xf, 0x80, 0xf, 0xff, 0xff, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c,
    0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20,
    0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c,
    0x20, 0x1c, 0x20, 0x1c, 0x20, 0x1c
])


# Bitmap images
bird_size = (16, 12)
pipe_size = (16, 32)


WIDTH = 128
HEIGHT = 64


"""飞行小鸟类"""
class Bird:
    def __init__(self):
        self.height = bird_size[1]
        self.y = HEIGHT // 2 - self.height // 2
        self.wing_power = 4
        self.gravity = 0.8
        self.vel = -self.wing_power

    # 下落
    def drop(self):
        self.vel += self.gravity
        self.y = int(self.y + self.vel)

    # 飞行
    def flap(self):
        self.vel = -self.wing_power

    # 是否坠落
    def crashed(self):                          
        y_limit = HEIGHT - self.height
        return self.y > y_limit

"""障碍类"""
class Obstacle:
    def __init__(self, x,size ):
        self.size =size 
        self.gap = urandom.randint(6 + self.size, HEIGHT - 6 - self.size)     # 随机生成间隙大小
        self.x = x              # 距离鸟大小
        self.score = 0          # 分数
        self.rate = 3           # 速率

    # 移动
    def scroll(self):           
        self.x -= self.rate    
        if self.x < -pipe_size[0]:
            self.score += 1
            self.x = WIDTH
            self.gap = urandom.randint(6 + self.size, HEIGHT - 6 - self.size)

    # 是否碰撞
    def collided(self, y):                     
        if self.x < bird_size[0] and self.x > -pipe_size[0] and \
           (self.gap - y > self.size or y + bird_size[1] - self.gap > self.size):
            return True
        else:
            return False


class Game():
    def __init__(self,gap_size):
        
        # 创建鸟和管道的framebuffer
        self.bird_fb = FrameBuffer(BIRD, bird_size[0], bird_size[1], framebuf.MONO_HLSB)         
        self.pipe_top_fb = FrameBuffer(PIPE_TOP, pipe_size[0], pipe_size[1], framebuf.MONO_HLSB)
        self.pipe_down_fb = FrameBuffer(PIPE_DOWN, pipe_size[0], pipe_size[1], framebuf.MONO_HLSB)

        self.gap_size = gap_size
        self.high_score = 0
        self.pressed  = False
        self.game_state = 0
        self.flappy_bird =  None
        self.obstacle_1 =  None
        self.obstacle_2 =  None

    # 保存最高分
    def write_high_score(self,n):
        f = open('fb_high_score.txt', 'w')
        f.write(str(n))
        f.close()

    # 读取最高分
    def read_high_score(self):
        if 'fb_high_score' in uos.listdir():
            f = open('fb_high_score.txt', 'r')
            high_score = f.read()
            f.close()
            return int(high_score)
        else:
            self.write_high_score(0)
            return 0

   # 绘制
    def draw(self):
        oled.fill(0)
        oled.blit(self.bird_fb, 0, self.flappy_bird.y)
        oled.blit(self.pipe_top_fb, self.obstacle_1.x, self.obstacle_1.gap - self.gap_size - pipe_size[1])
        oled.blit(self.pipe_down_fb, self.obstacle_1.x, self.obstacle_1.gap + self.gap_size)
        oled.blit(self.pipe_top_fb, self.obstacle_2.x, self.obstacle_2.gap - self.gap_size - pipe_size[1])
        oled.blit(self.pipe_down_fb, self.obstacle_2.x, self.obstacle_2.gap + self.gap_size)
        oled.fill_rect(WIDTH // 2 - 13, 0, 26, 9, 0)
        oled.text('%03d' % (self.obstacle_1.score + self.obstacle_2.score), WIDTH // 2 - 12, 0)
        oled.show()
   

    def _clicked(self):
        if button_a.value() == 0 and not self.pressed:
            self.pressed = True
            return True
        elif button_a.value() == 1 and self.pressed:
            self.pressed = False
        return False

    # 开机画面
    def game_start(self):
        oled.fill(0)
        oled.blit(self.pipe_down_fb, (WIDTH - pipe_size[0]) // 2, HEIGHT - 12)
        oled.blit(self.bird_fb, (WIDTH - bird_size[0]) // 2, HEIGHT - 12 - bird_size[1])
        oled.rect(0, 0, WIDTH, HEIGHT, 1)
        oled.text('F L A P P Y', WIDTH // 2 - 44, 3)
        oled.text('B I R D', WIDTH // 2 - 28, 13)
        oled.text('Record: ' + '%03d' % self.high_score, WIDTH // 2 - 44, HEIGHT // 2 - 6)
        oled.show()
        self.game_state = 1
      
    def game_waiting(self):
        if self._clicked():
            self.flappy_bird = Bird()                                                               # 实例小鸟对象
            self.obstacle_1 = Obstacle(WIDTH,self.gap_size)                                           # 实例第一个障碍对象
            self.obstacle_2 = Obstacle(WIDTH + (WIDTH + pipe_size[0]) // 2,self.gap_size)             # 实例第二个障碍对象
            self.game_state = 2

    def game_running(self):
        if self._clicked():
            self.flappy_bird.flap()
        self.flappy_bird.drop()
        if self.flappy_bird.crashed():
            self.flappy_bird.y = HEIGHT - self.flappy_bird.height      # 边界限制
            self.game_state = 3
        self.obstacle_1.scroll()
        self.obstacle_2.scroll()
        if self.obstacle_1.collided(self.flappy_bird.y) or self.obstacle_2.collided(self.flappy_bird.y):
            self.game_state = 3
        self.draw()

    def game_over(self):
        oled.fill_rect(WIDTH // 2 - 32, 10, 64, 23, 0)
        oled.rect(WIDTH // 2 - 32, 10, 64, 23, 1)
        oled.text('G A M E', WIDTH // 2 - 28, 13)
        oled.text('O V E R', WIDTH // 2 - 28, 23)
        self.score = self.obstacle_1.score + self.obstacle_2.score
        if self.score > self.high_score:
            self.high_score = self.score
            oled.fill_rect(WIDTH // 2 - 48, 37, 96, 14, 0)
            oled.rect(WIDTH // 2 - 48, 37, 96, 14, 1)
            oled.text('New record!', WIDTH // 2 - 44, 40)
            self.write_high_score(self.high_score)
        oled.show()

        try:
            self.send_score(self.score)
        except:
            pass
        self.game_state = 1


    def run(self):
        while True:
            if self.game_state == 0: self.game_start()
            elif self.game_state == 1: self.game_waiting()
            elif self.game_state == 2: self.game_running()
            elif self.game_state == 3: self.game_over()



if __name__ == '__main__':
    game=Game(gap_size = 16)
    game.run()
                
            

