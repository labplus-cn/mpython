# Pong game for mPython
# MIT license,Copyright (c) 2019 labplus@Tangliufeng

from mpython import *
import music


class Pong():
    def __init__(self):

        self.running = True
        self.start = False
        self.ball_rad = 5
        self.bats_position = 0
        self.bats_width = 15
        self.bats_height = 4

        self.ball_x = self.bats_width // 2
        self.ball_y = 64 - (self.ball_rad + self.bats_height + 1)
        self.inc_x, self.inc_y = 1, 1
        self.score = 0

    def collision(self):

        if self.ball_x >= 128 - self.ball_rad or self.ball_x < self.ball_rad:
            self.inc_x = -self.inc_x
        if self.ball_y >= 64 - (self.ball_rad + self.bats_height) or self.ball_y <= self.ball_rad:
            self.inc_y = -self.inc_y

    def update(self):
        self.ball_x = self.ball_x + self.inc_x
        self.ball_y = self.ball_y + self.inc_y
        self.bats_position = min(max(self.bats_position, 0), 128 - self.bats_width)

    def is_hit(self):
        # print('ball:', self.ball_x, self.ball_y, 'bats:', self.bats_position)
        if self.ball_y >= 64 - (self.ball_rad + self.bats_height):
            if self.ball_x >= self.bats_position + self.bats_width + self.ball_rad or self.ball_x <= self.bats_position - self.ball_rad:

                return False
            self.score += 1
            return True

    def run(self):

        while self.running:
            if button_a.value() == 0 and button_b.value() == 1:
                self.bats_position -= 2
                self.start = True
            if button_a.value() == 1 and button_b.value() == 0:
                self.bats_position += 2
                self.start = True

            if self.start:
                self.update()
                self.collision()

                if self.is_hit() == False:
                    self.running = False
                    continue

            oled.fill(0)
            oled.fill_circle(self.ball_x, self.ball_y, self.ball_rad, 1)
            oled.fill_rect(self.bats_position, 64 - self.bats_height, self.bats_width, self.bats_height, 1)
            oled.show()

        oled.text('Game over!', 20, 20)
        oled.text('Score %d' % self.score, 20, 32)
        oled.show()


if __name__ == '__main__':
    pong = Pong()
    pong.run()