音乐盒
==========

使用music模块内置歌曲结合掌控板的a,b按键，实现对歌曲的切换。这样就能完成个简单的音乐播放盒！

::

    from mpython import *
    import music

    aStatus=1
    bStatus=1
    index=0

    song=[music.DADADADUM,music.ENTERTAINER,music.PRELUDE,music.ODE,music.NYAN,music.RINGTONE,
        music.BLUES,music.BIRTHDAY,music.WEDDING,music.FUNERAL,music.PUNCHLINE,music.PYTHON,music.BADDY
        ]
    def displaySong():
        oled.fill(0)
        oled.DispChar("歌曲:%d" %(index+1),45,25)
        oled.show()
        

    while True:
        if button_b.value()==0 and aStatus==1:
                music.play(song[index],wait=False)
                oled.show()
                displaySong()
                index+=1
                aStatus=0
                if index>=len(song):
                    index=0
        elif button_b.value()==1:
            aStatus=1
        
            oled.show()
        if button_a.value()==0 and bStatus==1:
                music.play(song[index],wait=False)
                displaySong()
                index-=1
                bStatus=0
                if index<0:
                    index=len(song)-1
        elif button_a.value()==1:
            bStatus=1


除了播放music内置的歌曲以外，你还可以自编乐谱哦！