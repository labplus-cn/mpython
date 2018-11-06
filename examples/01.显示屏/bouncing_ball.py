
from mpython import *
# initial center of the circle
center_x = 63
center_y = 15
# how fast does it move in each direction
x_inc = 1
y_inc = 1
# what is the starting radius of the circle
radius = 8

# start with a blank screen
display.fill(0)
# we just blanked the framebuffer. to push the framebuffer onto the display, we call show()
display.show()
while True:
    # undraw the previous circle
    display.fill_circle(center_x, center_y, radius, 0)
    # if bouncing off right
    if center_x + radius >= 128:
        # start moving to the left
        x_inc = -1
    # if bouncing off left
    elif center_x - radius < 0:
        # start moving to the right
        x_inc = 1

    # if bouncing off top
    if center_y + radius >= 64:
        # start moving down
        y_inc = -1
    # if bouncing off bottom
    elif center_y - radius < 0:
        # start moving up
        y_inc = 1

    # go more in the current direction
    center_x += x_inc
    center_y += y_inc

    # draw the new circle
    display.fill_circle(center_x, center_y, radius,1)
    # show all the changes we just made
    display.show()