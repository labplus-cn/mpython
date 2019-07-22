# Tetris game for mPython
# MIT license,Copyright (c) 2019 labplus@Tangliufeng

from mpython import *
import math
import random, time

class Brick():
    def __init__(self, p_position):
        self.position = p_position

    def draw(self):

        x = self.position[1] * brick_size
        y = self.position[0] * brick_size
        oled.fill_rect(brick_size * (field_height - 1) - x, y, brick_size, brick_size, 1)


class Block():
    def __init__(self, p_bricks_layout, p_direction):
        self.bricks_layout = p_bricks_layout
        self.direction = p_direction
        self.init_position = (field_width // 2 - 2, 0)
        self.cur_layout = self.bricks_layout[self.direction]
        self.position = self.init_position
        self.stopped = False
        self.move_interval = 500
        self.last_move = 0
        self.bricks = []
        for (x, y) in self.cur_layout:
            self.bricks.append(Brick((self.position[0] + x, self.position[1] + y)))

    def draw(self):
        for brick in self.bricks:
            brick.draw()

    def isLegal(self, layout, position):
        (x0, y0) = position
        for (x, y) in layout:
            if x + x0 < 0 or y + y0 < 0 or x + x0 >= field_width or y + y0 >= field_height:
                return False
            if field_map[y + y0][x + x0] != 0:
                return False
        return True

    def left(self):
        new_position = (self.position[0] - 1, self.position[1])
        if self.isLegal(self.cur_layout, new_position):
            self.position = new_position
            self.refresh_bircks()

    def right(self):
        new_position = (self.position[0] + 1, self.position[1])
        if self.isLegal(self.cur_layout, new_position):
            self.position = new_position
            self.refresh_bircks()

    def down(self):
        (x, y) = (self.position[0], self.position[1] + 1)
        while self.isLegal(self.cur_layout, (x, y)):
            self.position = (x, y)
            self.refresh_bircks()
            y += 1

    def refresh_bircks(self):
        for (brick, (x, y)) in zip(self.bricks, self.cur_layout):
            brick.position = (self.position[0] + x, self.position[1] + y)

    def stop(self):
        global field_bricks
        global score
        self.stopped = True
        ys = []
        for brick in self.bricks:
            field_bricks.append(brick)
            (x, y) = brick.position
            if y not in ys:
                ys.append(y)
            field_map[y][x] = 1

        eliminate_count = 0
        ys.sort()

        for y in ys:
            if 0 in field_map[y]:
                continue
            eliminate_count += 1
            for fy in range(y, 0, -1):
                field_map[fy] = field_map[fy - 1][:]
            field_map[0] = [0 for i in range(field_width)]

            tmp_field_bricks = []
            for fb in field_bricks:
                (fx, fy) = fb.position
                if fy < y:
                    fb.position = (fx, fy + 1)
                    tmp_field_bricks.append(fb)
                elif fy > y:
                    tmp_field_bricks.append(fb)
            field_bricks = tmp_field_bricks
        if eliminate_count == 1:
            score += 1
        elif eliminate_count == 2:
            score += 2
        elif eliminate_count == 3:
            score += 4
        elif eliminate_count == 4:
            score += 6

    def update(self, time):
        self.draw()
        if time - self.last_move >= self.move_interval:
            new_position = (self.position[0], self.position[1] + 1)
            if self.isLegal(self.cur_layout, new_position):
                self.position = new_position
                self.refresh_bircks()
                self.last_move = time
            else:
                self.stop()

    def rotate(self):
        new_direction = (self.direction + 1) % len(self.bricks_layout)
        new_layout = self.bricks_layout[new_direction]
        if not self.isLegal(new_layout, self.position):
            return
        self.direction = new_direction
        self.cur_layout = new_layout
        for (brick, (x, y)) in zip(self.bricks, self.cur_layout):
            brick.position = (self.position[0] + x, self.position[1] + y)
        self.refresh_bircks()
        self.draw()


# 0: oooo
# 1: oo
#    oo
# 2: o
#   ooo
# 3: o
#    oo
#     o
# 4:  o
#    oo
#    o
# 5: ooo
#    o
# 6: ooo
#      o
bricks_layout_0 = (((0, 0), (0, 1), (0, 2), (0, 3)), ((0, 1), (1, 1), (2, 1), (3, 1)))
bricks_layout_1 = (((1, 0), (2, 0), (1, 1), (2, 1)), )
bricks_layout_2 = (
    ((1, 0), (0, 1), (1, 1), (2, 1)),
    ((0, 1), (1, 0), (1, 1), (1, 2)),
    ((1, 2), (0, 1), (1, 1), (2, 1)),
    ((2, 1), (1, 0), (1, 1), (1, 2)),
)
bricks_layout_3 = (
    ((0, 1), (1, 1), (1, 0), (2, 0)),
    ((0, 0), (0, 1), (1, 1), (1, 2)),
)
bricks_layout_4 = (
    ((0, 0), (1, 0), (1, 1), (2, 1)),
    ((1, 0), (1, 1), (0, 1), (0, 2)),
)
bricks_layout_5 = (
    ((0, 0), (1, 0), (1, 1), (1, 2)),
    ((0, 2), (0, 1), (1, 1), (2, 1)),
    ((1, 0), (1, 1), (1, 2), (2, 2)),
    ((2, 0), (2, 1), (1, 1), (0, 1)),
)
bricks_layout_6 = (
    ((2, 0), (1, 0), (1, 1), (1, 2)),
    ((0, 0), (0, 1), (1, 1), (2, 1)),
    ((0, 2), (1, 2), (1, 1), (1, 0)),
    ((2, 2), (2, 1), (1, 1), (0, 1)),
)

field_width, field_height = 16, 30
brick_size = 4
field_map = [[0 for i in range(field_width)] for i in range(field_height)]
field_bricks = []
score = 0
running = True
threshhold = 400


def drawField():
    for brick in field_bricks:
        brick.draw()


def getBlock():
    block_type = random.randint(0, 6)
    if block_type == 0:
        return Block(bricks_layout_0, random.randint(0, len(bricks_layout_0) - 1))
    elif block_type == 1:
        return Block(bricks_layout_1, random.randint(0, len(bricks_layout_1) - 1))
    elif block_type == 2:
        return Block(bricks_layout_2, random.randint(0, len(bricks_layout_2) - 1))
    elif block_type == 3:
        return Block(bricks_layout_3, random.randint(0, len(bricks_layout_3) - 1))
    elif block_type == 4:
        return Block(bricks_layout_4, random.randint(0, len(bricks_layout_4) - 1))
    elif block_type == 5:
        return Block(bricks_layout_5, random.randint(0, len(bricks_layout_5) - 1))
    elif block_type == 6:
        return Block(bricks_layout_6, random.randint(0, len(bricks_layout_6) - 1))


def run():
    global running
    btn_n_stat, btn_o_stat, btn_t_stat, btn_p_stat = [0] * 4

    while running:

        cur_block = getBlock()

        if not cur_block.isLegal(cur_block.cur_layout, cur_block.position):
            cur_block.draw()
            running = False
            continue

        while not cur_block.stopped:

            oled.fill(0)
            ticks = time.ticks_ms()
            cur_block.update(ticks)
            drawField()
            oled.show()

            if touchPad_T.read() < threshhold and btn_t_stat == 0:
                cur_block.rotate()
                btn_t_stat = 1
            elif touchPad_T.read() >= threshhold:
                btn_t_stat = 0

            if touchPad_P.read() < threshhold and btn_p_stat == 0:
                cur_block.down()
                btn_p_stat = 1
            elif touchPad_P.read() >= threshhold:
                btn_p_stat = 0

            if touchPad_N.read() < threshhold and btn_n_stat == 0:
                cur_block.left()
                btn_n_stat = 1
            elif touchPad_N.read() >= threshhold:
                btn_n_stat = 0

            if touchPad_O.read() < threshhold and btn_o_stat == 0:
                cur_block.right()
                btn_o_stat = 1
            elif touchPad_O.read() >= threshhold:
                btn_o_stat = 0
    oled.fill(0)
    oled.text('Game over!', 25, 20)
    oled.text('Score:%d' % score, 25, 32)
    oled.show()


if __name__ == '__main__':
    run()