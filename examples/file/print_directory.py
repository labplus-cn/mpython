from machine import Pin, SPI
import machine, sdcard, os

spi = SPI(1, baudrate=10000000, polarity=0, phase=0, sck=Pin(Pin.P13), mosi=Pin(Pin.P15), miso=Pin(Pin.P14))
sd = sdcard.SDCard(spi, Pin(Pin.P16))

os.mount(sd, '/sd')

def print_directory(path, tabs = 0):
    for file in os.listdir(path):
        stats = os.stat(path+"/"+file)
        filesize = stats[6]
        isdir = stats[0] & 0x4000
    
        if filesize < 1000:
            sizestr = str(filesize) + " by"
        elif filesize < 1000000:
            sizestr = "%0.1f KB" % (filesize/1000)
        else:
            sizestr = "%0.1f MB" % (filesize/1000000)
    
        prettyprintname = ""
        for i in range(tabs):
            prettyprintname += "   "
        prettyprintname += file
        if isdir:
            prettyprintname += "/"
        print('{0:<40} Size: {1:>10}'.format(prettyprintname, sizestr))
        
        # recursively print directory contents
        if isdir:
            print_directory(path+"/"+file, tabs+1)


print("Files on filesystem:")
print("====================")
print_directory("/sd")

