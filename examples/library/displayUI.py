from mpython import oled

class UI():

    
    def ProgressBar(self, x, y, width, height, progress):

        radius = int(height / 2)
        xRadius = x + radius
        yRadius = y + radius
        doubleRadius = 2 * radius
        innerRadius = radius - 2

        oled.RoundRect(x,y,width,height,radius,1)
        maxProgressWidth = int((width - doubleRadius + 1) * progress / 100)
        oled.fill_circle(xRadius, yRadius, innerRadius,1)
        oled.fill_rect(xRadius + 1, y + 2, maxProgressWidth, height - 3,1)
        oled.fill_circle(xRadius + maxProgressWidth, yRadius, innerRadius,1)

    def stripBar(self, x, y, width, height, progress,dir=1,frame=1):

        oled.rect(x,y,width,height,frame)
        if  dir:
            Progress=int(progress/100 *width)
            oled.fill_rect(x,y,Progress,height,1)
        else:
            Progress=int(progress/100 *height)
            oled.fill_rect(x,y+(height-Progress),width,Progress,1)