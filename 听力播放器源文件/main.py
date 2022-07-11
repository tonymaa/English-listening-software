from tkinter import Tk,Canvas,Button,Label,PhotoImage,Frame,Text
from tkinter.filedialog import askdirectory,askopenfilename
from tkinter.colorchooser import askcolor
from time import sleep
from threading import Thread
from os import _exit,listdir,execl,remove,mkdir
from os.path import exists,split,isfile,isdir

from PIL.Image import fromarray
from PIL.ImageTk import PhotoImage 
from cv2 import imread,resize,imdecode
from numpy import fromfile
from re import findall
from translate import main_translate_sentence
from mutagen.mp3 import MP3
import lib
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer,QMediaContent
from json import loads,dumps
from sys import executable,argv  
from base64 import b64decode
from gc import collect
from ctypes import windll
from struct import calcsize
from windnd import hook_dropfiles
class GeCi:
    def __init__(self,music_path="None"):
        self.geci_dict = {0:""} #{10:"***",....}
        self.geci_time = [0]
        self.geci_path = ""
        main_ui.display_area_frame.ge_ci_canvas.change_geci("")
        main_ui.display_area_frame.all_geci_canvas.clear_all()
        
    def open_geci_file(self,music_path):
        geci_path = ""
        for i in ["txt","lrc","krc"]:
            if exists(music_path[:-3] + i):
                geci_path = music_path[:-3] + i
        if not geci_path:return
        
        self.geci_path = geci_path
        lib.change_geci_time_format(self.geci_path)
        g = lib.open_krc_lrc_file(self.geci_path) 
        for i in g:
            if not i:continue
            self.geci_dict[i[0]] = i[1]
            self.geci_time.append(i[0])
            main_ui.display_area_frame.all_geci_canvas.creat_a_sentence(i[2],i[1])
        if len(self.geci_time) == 1: self.geci_path = ""  
    def get_music_geci(self,music_time):
        for i in range(len(self.geci_time)):
            if self.geci_time[i] > music_time: 
                return self.geci_dict[self.geci_time[i-1]]
        return self.geci_dict[self.geci_time[-1]]
    def get_music_last_sentence(self,music_time):
        if not self.geci_path: return
        for i in range(len(self.geci_time)):
            if self.geci_time[i] > music_time: 
                return self.geci_time[i-2]
        return self.geci_time[-2]
        
    def get_music_next_sentence(self,music_time):
        if not self.geci_path: return
        for i in range(len(self.geci_time)):
            if self.geci_time[i] > music_time:
                return self.geci_time[i]
                
    def get_music_repeat_sentence_start_endtime(self,music_time):
        if not self.geci_path: return
        for i in range(len(self.geci_time)):
            if self.geci_time[i] > music_time: 
                return self.geci_time[i-1],self.geci_time[i]
        return self.geci_time[-1],player.current_music_length - 1.7
        
class Media_Player:
    def __init__(self):
        self.music_dic = {}  
        self.current_music_name = ""
        self.current_music_length = 0
        self.file_directory = ""
        self.sentence_repeat_start_time = ""
        self.sentence_repeat_end_time = ""
        self.player = QMediaPlayer()
        self.set_yingliang(50)
        t = Thread(target=self.update_jindutiao_position)
        t.start()
        self.drop_file = ""
        self.drop_imgfile = ""
    def set_music(self,music_path):
        self.player.stop()
        self.player.setMedia(QMediaContent(QUrl(music_path)))
        self.player.play() 
        geci_obj.__init__()
        geci_obj.open_geci_file(self.file_directory+"/"+self.current_music_name)
    def setPlaybackRate(self,speed):

        self.player.setPlaybackRate(speed)
    def music_pause(self):
        self.player.pause()
    def music_play(self):
        self.player.play()
    def set_position(self,position):
        self.player.setPosition(position)
    def jin_ying(self):
        self.player.setVolume(0)
    def set_yingliang(self,volume):
        self.player.setVolume(volume)
    def update_jindutiao_position(self):
        while True:
            try:
                sleep(0.15)
                if self.current_music_name:
                    music_p = self.player.position() / 1000
                    main_ui.jin_du_tiao.dx = self.current_music_length/main_ui.jin_du_tiao.end
                    main_ui.jin_du_tiao.varying_time["text"] = lib.sec_convert_formatsec(music_p)
                    main_ui.jin_du_tiao.set_scale_place(music_p/main_ui.jin_du_tiao.dx)
                    if main_ui.jin_du_tiao.varying_time["text"] == main_ui.jin_du_tiao.full_time["text"]:self.player.play()
                    if geci_obj.geci_path: main_ui.display_area_frame.ge_ci_canvas.change_geci(geci_obj.get_music_geci(music_p))
                    if main_ui.repeat_stence_btn.current_state == "循环中":
                        if int(self.player.position()/1000) > self.sentence_repeat_end_time: 
                            self.player.setPosition(self.sentence_repeat_start_time*1000)
                            main_ui.button_beisu.time_ = self.sentence_repeat_start_time
                
                if self.drop_file: main_ui.play_dropfile(self.drop_file)
                if self.drop_imgfile: 
                    main_ui.display_area_frame.ge_ci_canvas.delete_img(1)
                    main_ui.display_area_frame.ge_ci_canvas.img_path = self.drop_imgfile
                    main_ui.display_area_frame.ge_ci_canvas.im_orig = cv_img = imdecode(fromfile(main_ui.display_area_frame.ge_ci_canvas.img_path,dtype="uint8"),-1)
                    main_ui.display_area_frame.ge_ci_canvas.im_orig = main_ui.display_area_frame.ge_ci_canvas.im_orig[:, :, ::-1]  
                    main_ui.display_area_frame.ge_ci_canvas.im = resize(main_ui.display_area_frame.ge_ci_canvas.im_orig,(main_ui.display_area_frame.ge_ci_canvas.width,main_ui.display_area_frame.ge_ci_canvas.height))
                    main_ui.display_area_frame.ge_ci_canvas.tkim = PhotoImage(fromarray(main_ui.display_area_frame.ge_ci_canvas.im))            
                    main_ui.display_area_frame.ge_ci_canvas.cv.itemconfig(main_ui.display_area_frame.ge_ci_canvas.bg_img,image=main_ui.display_area_frame.ge_ci_canvas.tkim)
                    with open("db/img_path.txt",mode="w") as w:
                        w.write(self.drop_imgfile)
                    self.drop_imgfile = ""
            except Exception:pass    

'''下一句'''
class Button_Next_Stence:
    def __init__(self,parent,x,y,colour,push_colour,command=None,bg_colour="white"):
        self.cv = Canvas(parent,name="下一句",height=25,width=25,cursor="hand2",bg=bg_colour,highlightthickness=0)
        self.cv.place(x=x,y=y)
        xx = 0
        yy = 0
        self.start_delay_time = 0
        self.end_delay_time = 0

        self.circle = self.cv.create_polygon(7+xx,11+yy,7+xx,23+yy,15+xx,17+yy,fill=colour)
        self.line = self.cv.create_line(17+xx,12+yy,17+xx,23+yy,fill=colour,width=2)
        def push_but(e):
            if "循环中" == main_ui.repeat_stence_btn.current_state:
                main_ui.repeat_stence_btn.push_but(0)
            if not geci_obj.geci_path: return
            current_music_time = (player.player.position() / 1000) 
            next_music_time = geci_obj.get_music_next_sentence(current_music_time) + self.start_delay_time
            # print(next_music_time)
            
            if main_ui.button_beisu.current_state == "有倍速":
                main_ui.button_beisu.time_ = next_music_time
                return
            
            
            if next_music_time == None:next_music_time = 0
            player.set_position(next_music_time * 1000)
            
        def push_but_colour(e):
            self.cv.itemconfig(self.circle, fill=colour)
            self.cv.itemconfig(self.line, fill=colour)
            
        def enter_colour(e):
            self.cv.itemconfig(self.circle, fill=push_colour)
            self.cv.itemconfig(self.line, fill=push_colour)
        def leave_colour(e):
            self.cv.itemconfig(self.circle, fill=colour)
            self.cv.itemconfig(self.line, fill=colour)  
        def start_delay(e):
            if e.state == 262156: 
                self.start_delay_time -= 0.1
                if main_ui.repeat_stence_btn.current_state == "循环中":
                    player.sentence_repeat_start_time -= 0.1
                
                
            elif e.state == 262157:
                self.start_delay_time += 0.1
                if main_ui.repeat_stence_btn.current_state == "循环中":
                    player.sentence_repeat_start_time += 0.1
            print(self.start_delay_time)
        def end_delay(e):
            if e.state == 262156:
                self.end_delay_time += 0.1
                if main_ui.repeat_stence_btn.current_state == "循环中":
                    player.sentence_repeat_end_time += 0.1
                
                
            elif e.state == 262157:
                self.end_delay_time -= 0.1
                if main_ui.repeat_stence_btn.current_state == "循环中":
                    player.sentence_repeat_end_time -= 0.1
                
            print(self.end_delay_time)
            
        self.cv.bind('<Enter>', enter_colour)
        self.cv.bind('<Leave>', leave_colour)
        self.cv.bind('<Button-1>', push_but)
        self.cv.bind_all('<Right>', push_but)

        # self.cv.bind_all("<Control-Left>",start_delay)
        # self.cv.bind_all("<Control-Right>",end_delay)

'''上一句'''
class Button_Last_Stence:
    def __init__(self,parent,x,y,colour,push_colour,command=None,bg_colour="white"):
        self.cv = Canvas(parent,name="上一句",height=25,width=25,cursor="hand2",bg=bg_colour,highlightthickness=0)
        self.cv.place(x=x,y=y)
        xx = 0
        yy = 0
        # self.circle = self.cv.create_polygon(17,11+yy,17,23+yy,9,17+yy,fill=colour)
        self.circle = self.cv.create_polygon(7+xx,17+yy,15+xx,23+yy,15+xx,11+yy,fill=colour)
        self.line = self.cv.create_line(5+xx,12+yy,5+xx,23+yy,fill=colour,width=2)
        def push_but(e):
            if "循环中" == main_ui.repeat_stence_btn.current_state:
                main_ui.repeat_stence_btn.push_but(0)
            if not geci_obj.geci_path: return
            current_music_time = (player.player.position() / 1000)
            last_music_time = geci_obj.get_music_last_sentence(current_music_time)  + main_ui.button_next_stence.start_delay_time
            # print(last_music_time)
            if main_ui.button_beisu.current_state == "有倍速":
                main_ui.button_beisu.time_ = last_music_time
                return

            
            if last_music_time == None:return
            player.set_position(last_music_time * 1000)
            
        def enter_colour(e):
            self.cv.itemconfig(self.circle, fill=push_colour)
            self.cv.itemconfig(self.line, fill=push_colour)
        def leave_colour(e):
            self.cv.itemconfig(self.circle, fill=colour)
            self.cv.itemconfig(self.line, fill=colour)
            
        self.cv.bind('<Button-1>', push_but)
        self.cv.bind('<Enter>', enter_colour)
        self.cv.bind('<Leave>', leave_colour)
        self.cv.bind_all('<Left>', push_but)

'''倍速'''
class Button_beisu:
    def __init__(self,parent,x,y,colour,push_colour,command=None,bg_colour="white"):
        def check_beisu(e):
            def bind_tag(a,b):
                speed = self.lb.itemcget(b,"text")
                self.lb.tag_bind(a,"<Enter>",lambda e:self.lb.itemconfig(a,fill=push_colour))
                self.lb.tag_bind(b,"<Enter>",lambda e:self.lb.itemconfig(a,fill=push_colour))
                self.lb.tag_bind(a,"<Leave>",lambda e:self.lb.itemconfig(a,fill=colour))
                self.lb.tag_bind(b,"<Leave>",lambda e:self.lb.itemconfig(a,fill=colour))
                self.lb.tag_bind(a,"<Button-1>",lambda e:self.check_speed_item(speed))
                self.lb.tag_bind(b,"<Button-1>",lambda e:self.check_speed_item(speed))
            if self.check_state == "隐藏":
                self.check_state = "显示"
                self.lb = Canvas(parent,height=80,width=34,bg=colour,highlightthickness=0)
                self.lb.place(x=self.width+9,y=self.height+10-80-1)
                for i in range(len(self.speed_list)):
                    dy = i * 16
                    a = self.lb.create_rectangle(0,0+dy,34,16+dy,width=1,fill=colour,outline="white")
                    b = self.lb.create_text(17,8+dy,font=["宋体",9],fill="white",anchor="center",text=str(self.speed_list[i])+"X")
                    bind_tag(a,b)
            else:
                self.check_state = "隐藏"
                self.lb.destroy()
        self.cv = Canvas(parent,name="倍速",height=28,width=43,cursor="hand2",highlightthickness=0,bg=bg_colour)
        self.cv.place(x=x,y=y)
        self.time_ = 0
        self.current_state = "无倍速"
        self.check_state = "隐藏"
        self.check_beisu = check_beisu
        self.width = x
        self.height = y
        self.speed_list = [0.75,0.85,1.0,1.25,1.5]
        self.cv_11 = self.cv.create_rectangle(10,10,43,24,width=1,outline=colour,fill=colour)
        self.cv_12 = self.cv.create_text(27,18,font=["宋体",9],fill="white",anchor="center",text="1.0X")
        
        self.cv.bind('<Enter>',lambda e:self.cv.itemconfig(self.cv_11,outline=push_colour,fill=push_colour))
        self.cv.bind('<Leave>',lambda e:self.cv.itemconfig(self.cv_11,outline=colour,fill=colour))
        self.cv.bind('<Button-1>',check_beisu)
        
        a = Thread(target=self.timer_)
        a.start()
    def check_speed_item(self,speed_str):
        speed = float(speed_str.strip("X"))
        if speed == 1: self.current_state = "无倍速"
        else: self.current_state = "有倍速"
        if self.current_state == "有倍速":
            player.setPlaybackRate(speed)
            self.speed = speed
            self.time_ = player.player.position() / 1000
        else:
            player.setPlaybackRate(1)
        self.check_beisu(1)
        self.cv.itemconfig(self.cv_12,text=speed_str)

            # 设置倍数出现的问题：比如以1.5倍速播放10分钟音频，用时6分40秒，但是用position方法
            # 得到的音频位置不准确,理论上应该是每秒播放1.5秒音频长度，实际却每秒播放2.2秒音频长度
            
            
    def timer_(self):
        while True:
            while self.current_state == "有倍速":
                player.player.setPosition(self.time_*1000)
                self.time_ += self.speed
                sleep(1)
                while main_ui.button_play_or_pause.current_state != "暂停":
                    sleep(0.2)
            sleep(0.1)
            
'''播放/暂停 按钮'''
class Button_Play_Or_Pause:
    def __init__(self,parent,x,y,colour,push_colour,bg_colour="white"):
        def push_but(e):
            self.cv.itemconfig(self.btn_play, fill=push_colour)
            self.cv.itemconfig(self.btn_pause_1, fill=push_colour)
            self.cv.itemconfig(self.btn_pause_2, fill=push_colour)

        def play_or_pause_left(e):
            if self.current_state == "暂停":
                player.music_pause()
            else:player.music_play()
            self.cv.itemconfig(self.btn_play, fill=colour)
            self.cv.itemconfig(self.btn_pause_1, fill=colour)
            self.cv.itemconfig(self.btn_pause_2, fill=colour)
            if self.cv.itemcget(self.btn_play,"state") == "hidden":
                self.current_state = "播放"
                self.cv.itemconfig(self.btn_play, state="normal")
                self.cv.itemconfig(self.btn_pause_1, state="hidden")
                self.cv.itemconfig(self.btn_pause_2, state="hidden")
            else:
                self.current_state = "暂停"
                self.cv.itemconfig(self.btn_play, state="hidden")
                self.cv.itemconfig(self.btn_pause_1, state="normal")
                self.cv.itemconfig(self.btn_pause_2, state="normal")
                     
        self.current_state = '暂停'
        self.play_or_pause_left = play_or_pause_left
        self.cv = Canvas(parent,name="播放/停止",height=28,width=28,cursor="hand2",bg=bg_colour,highlightthickness=0)
        self.cv.place(x=x,y=y)
        xx = 0
        yy = 0
        self.btn_pause_1 = self.cv.create_line(13+xx,8+yy,13+xx,25+yy,fill=colour,width=2.2,state="normal")
        self.btn_pause_2 = self.cv.create_line(21+xx,8+yy,21+xx,25+yy,fill=colour,width=2.2,state="normal")
        self.btn_play = self.cv.create_polygon(13.09+xx,7.36+yy,13.09+xx,25.8+yy,25.8+xx,17.2+yy,fill=colour,state="hidden")
        self.cv.bind('<Button-1>', push_but)
        self.cv.bind('<ButtonRelease-1>', play_or_pause_left)
        self.cv.bind_all('<space>', play_or_pause_left)

'''进度条'''
class Jin_Du_Tiao:
    '''当设定时长为4分钟、width=400，实际总长是400-6-5，则需要每秒走 (400-6-5)/(4*60) = 1.62（个像素）'''
    def __init__(self,parent,x,y,colour,push_colour,command=None,width=400,bg_colour="white"):
        def changeSize(e):
            self.end = self.cv.coords(self.loading_line)[2]-11.8
            self.dx = player.current_music_length/self.end
            # print(self.dx)
            self.full_time["text"] = lib.sec_convert_formatsec(player.current_music_length)
        def move_scale(e):
            if e.x < 5 or e.x > self.width-6: return
            self.husuo_flag = True
            # self.current_scale_place = e.x - 5
            self.cv.coords(self.circle,-4+e.x,4,7+e.x,15)
            self.cv.coords(self.loaded_line,2,10,e.x,10)
            self.cv.coords(self.loading_line,e.x+2,10,self.width,10)
            

 
        def enable_set_scale(e):
            if "循环中" == main_ui.repeat_stence_btn.current_state:
                main_ui.repeat_stence_btn.push_but(0)
            self.husuo_flag = False
            
            self.current_scale_place = self.cv.coords(self.loading_line)[0]-7
            
            # self.dx = player.current_music_length/self.end
            if main_ui.button_beisu.current_state == "有倍速":
                main_ui.button_beisu.time_ = self.dx * self.current_scale_place
                return
            player.set_position(self.dx * self.current_scale_place * 1000)
            
            
        self.husuo_flag = False
        self.width = width
        self.cv = Canvas(parent,name="进度条",height=16,width=self.width,cursor="hand2",bg=bg_colour,highlightthickness=0)
        self.cv.place(x=x,y=y)
        self.current_scale_place = 0
        self.loaded_line = self.cv.create_line(2,10,self.width,10,width=4,fill=colour)
        self.loading_line = self.cv.create_line(2,10,self.width,10,width=4,fill="#dcdcdc")
        self.circle = self.cv.create_oval(4-2,4,15-2,15, fill = "white",outline="#b9b9b9")
        self.varying_time = Label(parent,name="当前歌曲时间",bg=bg_colour,text="00:00",fg="#464646")
        self.varying_time.place(x=x-40,y=y-2)
        self.full_time = Label(parent,name="歌曲时间",bg=bg_colour,text="00:00",fg="#464646")
        self.full_time.place(x=x+width+7,y=y-2)
        
        # self.end = self.cv.coords(self.loading_line)[2]-11.8
        self.cv.bind('<Button-1>', move_scale)
        self.cv.bind('<B1-Motion>', move_scale)
        self.cv.bind('<ButtonRelease-1>',enable_set_scale)
        self.cv.bind('<Configure>',changeSize)
    def set_scale_place(self,x):
        if self.husuo_flag: return
        self.cv.coords(self.circle,-4+x+5,4,7+x+5,15)
        self.cv.coords(self.loaded_line,2,10,x+5,10)
        self.cv.coords(self.loading_line,x+5+2,10,self.width,10)  
        self.current_scale_place = x

'''歌曲标题'''
class Music_Title:
    def __init__(self,parent,x,y,colour,push_colour,bg_colour=None,title=""):
        self.mus_title = Label(parent,bg=bg_colour,text=title,fg='#3e3e3e')
        self.mus_title.place(x=x-50,y=y-17)

'''音量条'''
class Yin_Liang_tiao:
    def __init__(self,parent,x,y,colour,push_colour,command=None,bg_colour="white"):
        def changeSize(e):
            self.set_scale_place(player.player.volume() /1.176)
        def move_scale(e):
            if e.x < 5 or e.x > self.width: return
            # print("e.x",e.x,self.current_scale_place)
            self.husuo_flag = True
            self.laba.itemconfig(self.laba_3,outline='#707070',state='normal')
            self.laba.itemconfig(self.laba_4,outline='#707070',state='normal')
            self.current_scale_place = e.x - 5
            self.cv.coords(self.circle,-4+e.x,4,7+e.x,15)
            self.cv.coords(self.loaded_line,5,10,e.x,10)
            self.cv.coords(self.loading_line,e.x+5,10,self.width,10)
            player.set_yingliang(round(self.current_scale_place * 1.176))
        def enable_set_scale(e):
            self.husuo_flag = False
            
        def laba_enter_colour(e):
            self.laba.itemconfig(self.laba_1,fill="#484848")
            self.laba.itemconfig(self.laba_2,fill="#484848")
            self.laba.itemconfig(self.laba_3,outline="#484848")
            self.laba.itemconfig(self.laba_4,outline="#484848")
        def laba_leave_colour(e):
            self.laba.itemconfig(self.laba_1,fill="#707070")
            self.laba.itemconfig(self.laba_2,fill="#707070")
            self.laba.itemconfig(self.laba_3,outline='#707070')
            self.laba.itemconfig(self.laba_4,outline='#707070')
        def jin_ying(e):
            self.set_scale_place(0)
            self.laba.itemconfig(self.laba_3,outline='#707070',state='hidden')
            self.laba.itemconfig(self.laba_4,outline='#707070',state='hidden')
            player.jin_ying()
        self.husuo_flag = False
        self.width = 90
        self.cv = Canvas(parent,name="音量条",height=16,width=self.width,cursor="hand2",bg=bg_colour,highlightthickness=0)
        self.cv.place(x=x,y=y)
        self.current_scale_place = 0
        
        self.loaded_line = self.cv.create_line(5,10,self.width,10,width=4,fill=colour)
        self.loading_line = self.cv.create_line(5,10,self.width,10,width=4,fill="#dcdcdc")
        self.circle = self.cv.create_oval(4-2,4,15-2,15, fill = "white",outline="#b9b9b9",state="hidden")
        
        self.cv.bind('<Button-1>', move_scale)
        self.cv.bind('<B1-Motion>', move_scale)
        self.cv.bind('<ButtonRelease-1>',enable_set_scale)
        self.cv.bind('<Enter>',lambda e: self.cv.itemconfig(self.circle,state="normal"))
        self.cv.bind('<Leave>',lambda e: self.cv.itemconfig(self.circle,state="hidden"))
        
        self.set_scale_place(42)
        
        self.laba = Canvas(parent,name="喇叭",height=18,width=24,cursor="hand2",bg=bg_colour,highlightthickness=0)
        self.laba.place(x=x-25,y=y)
        self.laba_1 = self.laba.create_rectangle(3,6,8,13,fill="#707070",width=0)
        self.laba_2 = self.laba.create_polygon(8,6,14,2,14,17,8,13,fill="#707070")
        self.laba_3 = self.laba.create_arc(22,1,12,18,start=-45,style="arc",outline='#707070')
        self.laba_4 = self.laba.create_arc(18,2,8,17,start=-45,style="arc",outline='#707070')
        self.laba.bind('<Enter>',laba_enter_colour)
        self.laba.bind('<Leave>',laba_leave_colour)
        self.laba.bind('<Button-1>',jin_ying)
        self.laba.bind('<Configure>',changeSize)
    def set_scale_place(self,x):
        if self.husuo_flag: return
        self.current_scale_place = x
        x += 5
        self.cv.coords(self.circle,-4+x,4,7+x,15)
        self.cv.coords(self.loaded_line,5,10,x,10)
        self.cv.coords(self.loading_line,x+5,10,self.width,10)

'''单句循环按钮'''
class Repeat_Stence_Btn:
    def __init__(self,parent,x,y,colour,push_colour,bg_colour="white"):
        def push_but(e):
            if not player.current_music_name:return
            if not geci_obj.geci_path: return
            if self.check_flag:
                self.cv.itemconfig(self.cv_11,state="normal")
                self.cv.itemconfig(self.cv_12,state="normal")
                self.cv.itemconfig(self.cv_13,state="normal")
                self.cv.itemconfig(self.cv_21,state="hidden")
                self.cv.itemconfig(self.cv_22,state="hidden")
                self.check_flag = False
                self.current_state = "循环中"
                if not player.current_music_name: return
                repeat_time = geci_obj.get_music_repeat_sentence_start_endtime(player.player.position()/1000)
                # print(repeat_time)
                player.sentence_repeat_start_time = repeat_time[0] + main_ui.button_next_stence.start_delay_time
                player.sentence_repeat_end_time = repeat_time[1] - 0.5 + main_ui.button_next_stence.end_delay_time
                
            else:
                self.cv.itemconfig(self.cv_11,state="hidden")
                self.cv.itemconfig(self.cv_12,state="hidden")
                self.cv.itemconfig(self.cv_13,state="hidden")
                self.cv.itemconfig(self.cv_21,state="normal")
                self.cv.itemconfig(self.cv_22,state="normal")
                self.check_flag = True
                self.current_state = "无循环"
        def enter_colour(e):
            self.cv.itemconfig(self.cv_11,fill=push_colour)
            self.cv.itemconfig(self.cv_12,fill=push_colour)
            self.cv.itemconfig(self.cv_13,fill=push_colour)
            self.cv.itemconfig(self.cv_21,fill=push_colour)
            self.cv.itemconfig(self.cv_22,fill=push_colour)
        def leave_colour(e):
            self.cv.itemconfig(self.cv_11,fill=colour)
            self.cv.itemconfig(self.cv_12,fill=colour)
            self.cv.itemconfig(self.cv_13,fill=colour)
            self.cv.itemconfig(self.cv_21,fill=colour)
            self.cv.itemconfig(self.cv_22,fill=colour)
        self.check_flag = True
        self.current_state = "无循环"
        self.push_but = push_but
        self.cv = Canvas(parent,name="单句循环按钮",height=28,width=28,cursor="hand2",bg=bg_colour,highlightthickness=0)
        self.cv.place(x=x,y=y)
        
        self.cv_11 = self.cv.create_line(19,13,4,13,4,24,14,24,20,19,fill=colour,width=2,joinstyle='round',state="hidden")
        self.cv_12 = self.cv.create_line(12,9,19,13,12,16,fill=colour,width=2,joinstyle='round',state="hidden")
        self.cv_13 = self.cv.create_line(9,15,9,22,fill=colour,width=2,joinstyle='round',state="hidden")
        
        self.cv_21 = self.cv.create_line(12,11,19,15,4,15,fill=colour,width=2,joinstyle='round')
        self.cv_22 = self.cv.create_line(4,21,19,21,12,24,fill=colour,width=2,joinstyle='round')

        self.cv.bind('<Button-1>', push_but)
        self.cv.bind('<Enter>', enter_colour)
        self.cv.bind('<Leave>', leave_colour)
        self.cv.bind_all('<Down>', push_but)

'''歌词显示/隐藏'''
class Display_Ge_Ci:
    def __init__(self,parent,x,y,colour,push_colour,bg_colour="white"):
        def push_but(e):
            if self.check_flag:
                # self.text_geci = main_ui.display_area_frame.ge_ci_canvas.cv.itemcget(main_ui.display_area_frame.ge_ci_canvas.geci_text,"text")
                self.cv.itemconfig(self.cv_11,fill="white",outline=colour)
                self.cv.itemconfig(self.cv_12,fill=colour)
                self.check_flag = False
                main_ui.display_area_frame.ge_ci_canvas.cv.itemconfig(main_ui.display_area_frame.ge_ci_canvas.geci_text,state="hidden")
                self.cv.bind('<Enter>',enter_colour)
                self.cv.bind('<Leave>',leave_colour)
            else: 
                self.cv.itemconfig(self.cv_11,outline=colour,fill=colour)
                self.cv.itemconfig(self.cv_12,fill="white")
                self.check_flag = True
                main_ui.display_area_frame.ge_ci_canvas.cv.itemconfig(main_ui.display_area_frame.ge_ci_canvas.geci_text,state="normal")
                self.cv.bind('<Enter>', lambda e:self.cv.itemconfig(self.cv_11,outline=push_colour,fill=push_colour))
                self.cv.bind('<Leave>',lambda e:self.cv.itemconfig(self.cv_11,outline=colour,fill=colour))
        def enter_colour(e):      
            self.cv.itemconfig(self.cv_11,outline=push_colour)
            self.cv.itemconfig(self.cv_12,fill=push_colour)
        def leave_colour(e):
            self.cv.itemconfig(self.cv_11,outline=colour)
            self.cv.itemconfig(self.cv_12,fill=colour)
        self.check_flag = True
        self.check_flag_2 = True
        
        
        self.cv = Canvas(parent,name="歌词显示/隐藏",height=28,width=28,cursor="hand2",highlightthickness=0,bg=bg_colour)
        self.cv.place(x=x,y=y)
        
        self.cv_11 = self.cv.create_rectangle(10,10,24,24,width=1,outline=colour,fill=colour)
        self.cv_12 = self.cv.create_text(12,11,font=["宋体",9],fill="white",anchor="nw",text="词")
        
        self.cv.bind('<Button-1>', push_but)
        self.cv.bind_all('<Up>', push_but)
        self.cv.bind('<Enter>', lambda e:self.cv.itemconfig(self.cv_11,outline=push_colour,fill=push_colour))
        self.cv.bind('<Leave>',lambda e:self.cv.itemconfig(self.cv_11,outline=colour,fill=colour))

'''翻译按钮'''
class Translate_But:
    def __init__(self,parent,x,y,colour,push_colour,bg_colour="white"):
        def push_but(e):
            if main_ui.tool_bar.but["中英互译"].tool_bar_but.itemcget(main_ui.tool_bar.but["中英互译"].line,"state") == "hidden":
                main_ui.tool_bar.but["中英互译"].tool_bar_but.itemconfig(main_ui.tool_bar.but["中英互译"].line,state="normal")
                main_ui.tool_bar.but["中英互译"].tool_bar_but["bg"] = "white" 
                for i,j in main_ui.tool_bar.but.items():
                    if i == main_ui.tool_bar.but["中英互译"].name:continue
                    j.tool_bar_but.itemconfig(j.line,state="hidden")
                    j.tool_bar_but["bg"] = "white"
                if main_ui.tool_bar.but["中英互译"].command:main_ui.tool_bar.but["中英互译"].command()
            main_ui.display_area_frame.translation_canvas.input_text.delete('1.0','end')
            insert_text = main_ui.display_area_frame.ge_ci_canvas.cv.itemcget(main_ui.display_area_frame.ge_ci_canvas.geci_text,"text")
            main_ui.display_area_frame.translation_canvas.input_text.insert("end",insert_text)
            main_ui.display_area_frame.translation_canvas.translate_sentence()

        def enter_colour(e):      
            self.cv.itemconfig(self.cv_11,outline=push_colour)
            self.cv.itemconfig(self.cv_12,fill=push_colour)
        def leave_colour(e):
            self.cv.itemconfig(self.cv_11,outline=colour)
            self.cv.itemconfig(self.cv_12,fill=colour) 
        
        self.cv = Canvas(parent,name="翻译按钮",height=28,width=28,cursor="hand2",highlightthickness=0,bg=bg_colour)
        self.cv.place(x=x,y=y)
        
        self.cv_11 = self.cv.create_rectangle(10,10,24,24,width=1,outline=colour,fill=colour)
        self.cv_12 = self.cv.create_text(12,11,font=["宋体",9],fill="white",anchor="nw",text="译")
        
        self.cv.bind('<Button-1>', push_but)
        self.cv.bind_all('<Control-Down>', push_but)
        self.cv.bind('<Enter>', lambda e:self.cv.itemconfig(self.cv_11,outline=push_colour,fill=push_colour))
        self.cv.bind('<Leave>',lambda e:self.cv.itemconfig(self.cv_11,outline=colour,fill=colour))

'''记录按钮'''
class Record_But:
    def __init__(self,parent,x,y,colour,push_colour,bg_colour="white"):
        def push_but(e):
            def rec_a_sentence():
                current_music_time = player.player.position() / 1000
                sentence = geci_obj.get_music_geci(current_music_time)
                sentence_start_time = geci_obj.get_music_repeat_sentence_start_endtime(player.player.position()/1000)[0]
                sentence_rec = { sentence : {
                        "file_audio_path" : player.file_directory + "/" + player.current_music_name,
                        "sentence_start_time" : sentence_start_time,
                        }
                    }
                return sentence_rec
                
            if not player.current_music_name:return
            if not geci_obj.geci_path: return    
                
            sentence_rec = rec_a_sentence()

            for i in sentence_rec.keys():
                current_sentence = i


            for line in main_ui.display_area_frame.my_record_canvas.record_sentence:
                for i in line.keys():
                    if i == current_sentence:
                        return
            main_ui.display_area_frame.my_record_canvas.record_sentence.append(sentence_rec)
            main_ui.display_area_frame.my_record_canvas.save_sentence_to_txt()
            main_ui.display_area_frame.my_record_canvas.creat_a_sentence(current_sentence)

            
            
        def enter_colour(e):      
            self.cv.itemconfig(self.cv_11,outline=push_colour)
            self.cv.itemconfig(self.cv_12,fill=push_colour)
        def leave_colour(e):
            self.cv.itemconfig(self.cv_11,outline=colour)
            self.cv.itemconfig(self.cv_12,fill=colour) 
        
        self.cv = Canvas(parent,name="记录按钮",height=28,width=28,cursor="hand2",highlightthickness=0,bg=bg_colour)
        self.cv.place(x=x,y=y)
        
        self.cv_11 = self.cv.create_rectangle(10,10,24,24,width=1,outline=colour,fill=colour)
        self.cv_12 = self.cv.create_text(12,11,font=["宋体",9],fill="white",anchor="nw",text="记")
        
        self.cv.bind('<Button-1>', push_but)
        self.cv.bind('<Enter>', lambda e:self.cv.itemconfig(self.cv_11,outline=push_colour,fill=push_colour))
        self.cv.bind('<Leave>',lambda e:self.cv.itemconfig(self.cv_11,outline=colour,fill=colour))
        self.cv.bind_all('<Control-Return>',push_but)
        
      
'''改变窗口尺寸'''
class Change_Window_Size:
    def __init__(self,parent,colour,push_colour,bg_colour="white"):
        def resize(e):
            try:
                self.parent.geometry('{}x{}+{}+{}'.format(self.varying_x+e.x-13,self.varying_y+e.y-13,parent.winfo_x(),parent.winfo_y()))
            except Exception:pass
        def remain_cv_place(e):
            self.varying_x = parent.winfo_width()
            self.varying_y = parent.winfo_height()
            self.cv.place(x=self.varying_x-18,y=self.varying_y-18)
            nt_lt_py_but_x = self.varying_x * 0.42
            nt_lt_py_but_y = self.varying_y-40
            '''倍速'''
            main_ui.button_beisu.cv.place(x=nt_lt_py_but_x-140 -48 -15,y=nt_lt_py_but_y)
            main_ui.button_beisu.width = nt_lt_py_but_x-140 -48 -15
            main_ui.button_beisu.height = nt_lt_py_but_y
            if main_ui.button_beisu.check_state == "显示":
                main_ui.button_beisu.check_beisu(1)
            '''播放/暂停'''
            main_ui.button_play_or_pause.cv.place(x=38+nt_lt_py_but_x,y=nt_lt_py_but_y)
            '''下一句'''
            main_ui.button_next_stence.cv.place(x=88+nt_lt_py_but_x,y=nt_lt_py_but_y)
            '''上一句'''
            main_ui.button_last_stence.cv.place(x=nt_lt_py_but_x,y=nt_lt_py_but_y)
            '''重复一句'''
            main_ui.repeat_stence_btn.cv.place(x=nt_lt_py_but_x+130,y=nt_lt_py_but_y)
            '''歌词显示/隐藏'''
            main_ui.display_ge_ci.cv.place(x=nt_lt_py_but_x - 48,y=nt_lt_py_but_y)
            '''翻译按钮'''
            main_ui.translate_but.cv.place(x=nt_lt_py_but_x - 92,y=nt_lt_py_but_y)
            '''记录按钮'''
            main_ui.record_but.cv.place(x=nt_lt_py_but_x - 140,y=nt_lt_py_but_y)
            '''工具栏凑数'''
            parent.children["工具栏"].children["end_frame"]["height"] = self.varying_y - 306
            '''主框架'''
            main_ui.display_area_frame.ge_ci_canvas.width = self.varying_x - 90
            main_ui.display_area_frame.ge_ci_canvas.height = self.varying_y - 101
            parent.children["主显示框架"]["width"] = main_ui.display_area_frame.ge_ci_canvas.width
            parent.children["主显示框架"]["height"] = main_ui.display_area_frame.ge_ci_canvas.height
            '''歌词画布'''
            if main_ui.tool_bar.current_toolbar_state == "歌词画布":
                parent.children["主显示框架"].children["歌词画布"]["width"] = main_ui.display_area_frame.ge_ci_canvas.width
                parent.children["主显示框架"].children["歌词画布"]["height"] = main_ui.display_area_frame.ge_ci_canvas.height
            '''本地音频画布'''
            main_ui.display_area_frame.local_audio_canvas.width = self.varying_x - 90
            main_ui.display_area_frame.local_audio_canvas.height = self.varying_y - 101
            if main_ui.tool_bar.current_toolbar_state == "本地音频画布":
                parent.children["主显示框架"].children["本地音频画布"]["width"] = main_ui.display_area_frame.local_audio_canvas.width
                parent.children["主显示框架"].children["本地音频画布"]["height"] = main_ui.display_area_frame.local_audio_canvas.height
            '''我的记录画布'''
            main_ui.display_area_frame.my_record_canvas.width = self.varying_x - 90
            main_ui.display_area_frame.my_record_canvas.height = self.varying_y - 101
            if main_ui.tool_bar.current_toolbar_state == "我的记录画布":
                parent.children["主显示框架"].children["我的记录画布"]["width"] = main_ui.display_area_frame.my_record_canvas.width
                parent.children["主显示框架"].children["我的记录画布"]["height"] = main_ui.display_area_frame.my_record_canvas.height    
            '''全部歌词画布'''
            main_ui.display_area_frame.all_geci_canvas.width = self.varying_x - 90
            main_ui.display_area_frame.all_geci_canvas.height = self.varying_y - 101
            if main_ui.tool_bar.current_toolbar_state == "全部歌词画布":
                parent.children["主显示框架"].children["全部歌词画布"]["width"] = main_ui.display_area_frame.all_geci_canvas.width
                parent.children["主显示框架"].children["全部歌词画布"]["height"] = main_ui.display_area_frame.all_geci_canvas.height    
            '''中英互译画布'''
            main_ui.display_area_frame.translation_canvas.width = self.varying_x - 90
            main_ui.display_area_frame.translation_canvas.height = self.varying_y - 101
            if main_ui.tool_bar.current_toolbar_state == "中英互译画布":
                parent.children["主显示框架"].children["中英互译画布"]["width"] = main_ui.display_area_frame.translation_canvas.width
                parent.children["主显示框架"].children["中英互译画布"]["height"] = main_ui.display_area_frame.translation_canvas.height 
            
            
            '''进度条'''
            width = self.varying_x * 0.8
            main_ui.jin_du_tiao = Jin_Du_Tiao(parent,x=self.varying_x * 0.1,y=self.varying_y-56,colour=colour,push_colour=push_colour,width=width,bg_colour=bg_colour)
            '''歌曲标题'''
            main_ui.music_title.mus_title.place(x=self.varying_x * 0.1-50,y=self.varying_y-75)
            '''音量条'''
            main_ui.yin_liang_tiao = Yin_Liang_tiao(parent,x=self.varying_x * 0.1 + width-40,y=self.varying_y-65+30,colour=colour,push_colour=push_colour,bg_colour=bg_colour)
            '''下面的控件背景'''
            parent.children["背景"].place(x=0,y=self.varying_y-75)
            '''标题栏'''
            main_ui.title_bar.width = self.varying_x
            parent.children["标题栏"]["width"] = self.varying_x - 48
            main_ui.title_bar.close_but.place(x=self.varying_x -24,y=0)
            main_ui.title_bar.mini_but.place(x=self.varying_x -48,y=0)

        def return_geometry(e):
            self.parent.geometry('{}x{}+{}+{}'.format(self.org_x,self.org_y,parent.winfo_x(),parent.winfo_y()))
        self.parent = parent
        self.remain_cv_place = remain_cv_place
        parent.update()
        # print(parent.winfo_geometry())
        self.org_x = parent.winfo_width()
        self.org_y = parent.winfo_height()
        self.varying_x = parent.winfo_width()
        self.varying_y = parent.winfo_height()
        self.cv = Canvas(parent,width=16,height=16,bg=bg_colour,cursor="sizing",highlightthickness=0)
        self.cv.place(x=self.org_x-18,y=self.org_y-18)
        self.line1 = self.cv.create_line(0,18,18,0,fill=push_colour,width=1)
        self.line1 = self.cv.create_line(0,22,22,0,fill=push_colour,width=1)
        self.line1 = self.cv.create_line(0,26,26,0,fill=push_colour,width=1)
        self.cv.bind("<B1-Motion>",resize)
        self.cv.bind("<ButtonRelease-1>",remain_cv_place)
        self.cv.bind("<Double-Button-1>",return_geometry)

'''标题栏'''
class Title_Bar:
    def __init__(self,parent,x,y,colour,push_colour,width):
        global logo
        def move_window(e):
            self.org_geom_x = parent.winfo_x()
            self.org_geom_y = parent.winfo_y()
            parent.geometry('{}x{}+{}+{}'.format(parent.winfo_width(),parent.winfo_height(),self.org_geom_x + (self.mouse_situation[0]-e.x)*-1,self.org_geom_y + (self.mouse_situation[1]-e.y)*-1))
        def clear_(e):
            self.flag_move = True
        def record_mouse_situation(e):
            self.mouse_situation = (e.x,e.y)
        def enter_colour_1(e):
            self.close_but.itemconfig(self.closeline1,fill="white")
            self.close_but.itemconfig(self.closeline2,fill="white")
        def leave_colour_1(e):
            self.close_but.itemconfig(self.closeline1,fill=push_colour)
            self.close_but.itemconfig(self.closeline2,fill=push_colour)
        def mini_window(e):
            parent.overrideredirect(False)
            parent.wm_withdraw()
            parent.iconify()
            self.current_tk_state = "iconic"
            
        def display_window(e):
            if self.current_tk_state == "iconic":
                parent.overrideredirect(True)
                main_ui.set_appwindow(parent)
            self.current_tk_state = "normal"
                
        def max_window(e):
            if self.flag_max: 
                parent.geometry("{}x{}+{}+{}".format(parent.winfo_screenwidth(),parent.winfo_screenheight()-40,0,0))
                self.flag_max = False
                parent.update()
                main_ui.change_window_size.remain_cv_place(e)  
            else:
                parent.geometry("{}x{}+{}+{}".format(main_ui.change_window_size.org_x,main_ui.change_window_size.org_y,self.org_geom_x,self.org_geom_y))
                self.flag_max = True
                parent.update()
                main_ui.change_window_size.remain_cv_place(e)
        self.org_geom_x = parent.winfo_x()
        self.org_geom_y = parent.winfo_y()
        self.flag_move = True
        self.flag_mini = True
        self.flag_max = True
        self.current_tk_state = "normal"
        # self.mouse_situation = (0,0)
        self.width = width
        self.cv = Canvas(parent,name="标题栏",height=24,width=width-48,bg=colour,highlightthickness=0) 
        self.cv.place(x=0,y=0)
        
        self.close_but = Canvas(parent,name="关闭",height=24,width=24,bg=colour,cursor="hand2",highlightthickness=0)
        self.close_but.place(x=width-24,y=0)
        self.closeline1 = self.close_but.create_line(7,7,18,18,fill=push_colour,width=1)
        self.closeline2 = self.close_but.create_line(18,7,7,18,fill=push_colour,width=1)
        
        self.mini_but = Canvas(parent,name="最小化",height=24,width=24,bg=colour,cursor="hand2",highlightthickness=0)
        self.mini_but.place(x=width-48,y=0)
        self.miniline1 = self.mini_but.create_line(5,12,18,12,fill=push_colour,width=1)
        
        logo = PhotoImage(file="db/logo.gif")
        # with open("img/logo.gif",mode="rb")as rb:print(rb.read())
        self.cv.create_image(14,11,image=logo)
        self.cv.create_text(65,12,text="听力播放器",fill="white",font=["微软雅黑",10,'bold'])
        self.qq_info = self.cv.create_text(200,13,text="E-mail:1605337475@qq.com",fill=push_colour,font=["幼圆",10],state="hidden")
        
        xx = self.width - 90
        self.c = self.cv.create_rectangle(8+xx,2,28+xx,22,fill=colour,outline="")
        self.c1 = self.cv.create_arc(16+xx,4,22+xx,8,extent=100,style="arc",outline=push_colour,start=230)
        self.c2 = self.cv.create_line(16+xx,7,11+xx,11,13+xx,13,15+xx,11,15+xx,18,22+xx,18,22+xx,11,24+xx,13,26+xx,11,21+xx,6,fill=push_colour)
        def changeSize(e):
            xx = self.width - 90
            self.cv.coords(self.c,8+xx,2,28+xx,22)
            self.cv.coords(self.c1,16+xx,4,22+xx,8)
            self.cv.coords(self.c2,16+xx,7,11+xx,11,13+xx,13,15+xx,11,15+xx,18,22+xx,18,22+xx,11,24+xx,13,26+xx,11,21+xx,6)
        def change1(e):
            self.cv.itemconfig(self.c1,outline="white")
            self.cv.itemconfig(self.c2,fill="white")
        def change2(e):
            self.cv.itemconfig(self.c1,outline=push_colour)
            self.cv.itemconfig(self.c2,fill=push_colour)
        def check_change_colour(e):
            def select_colour():
                colour = askcolor()
                if colour[0] == None:return
                button_colour = colour[-1]
                button_push_colour = ("#" + str(hex(int((colour[0][0] * 0.8)))) + str(hex(int((colour[0][1] * 0.8)))) + str(hex(int((colour[0][2] * 0.8))))).replace("0x",'')
                return button_colour,button_push_colour
            col = select_colour()
            if not col: return
            with open("db/colour.txt",mode="w") as w:
                col = dumps(col)
                w.write(col)
            main_ui.record_current_data()
            python = executable 
            execl(python, python, * argv)  
        def close_window(e):
            main_ui.record_current_data()
            _exit(0)
        
        self.cv.tag_bind(self.c1,"<Enter>",change1)
        self.cv.tag_bind(self.c1,"<Button-1>",check_change_colour)
        self.cv.tag_bind(self.c2,"<Enter>",change1)
        self.cv.tag_bind(self.c2,"<Button-1>",check_change_colour)
        self.cv.tag_bind(self.c,"<Enter>",change1)
        self.cv.tag_bind(self.c,"<Button-1>",check_change_colour)
        self.cv.tag_bind(self.c1,"<Leave>",change2)
        self.cv.tag_bind(self.c2,"<Leave>",change2)
        self.cv.tag_bind(self.c,"<Leave>",change2)
        
        
        self.cv.bind("<B1-Motion>",move_window)
        self.cv.bind("<Button-1>",record_mouse_situation)
        
        self.cv.bind("<ButtonRelease-1>",clear_)
        self.cv.bind("<Double-Button-1>",max_window)
        self.cv.bind_all("<KeyPress-Escape>",max_window)
        self.cv.bind_all("<Alt-F4>",close_window)
        
        self.cv.bind("<Configure>",changeSize)
        
        self.cv.bind("<Enter>",lambda e:self.cv.itemconfig(self.qq_info,state="normal"))
        self.cv.bind("<Leave>",lambda e:self.cv.itemconfig(self.qq_info,state="hidden"))
        
        self.close_but.bind("<Enter>",enter_colour_1)
        self.close_but.bind("<Leave>",leave_colour_1)
        self.close_but.bind("<ButtonPress-1>",close_window)
        
        self.mini_but.bind("<Enter>",lambda e:self.mini_but.itemconfig(self.miniline1,fill="white"))
        self.mini_but.bind("<Leave>",lambda e:self.mini_but.itemconfig(self.miniline1,fill=push_colour))
        self.mini_but.bind("<ButtonPress-1>",mini_window)
        self.mini_but.bind("<Map>",display_window)
        
        

'''工具栏里的按钮'''
class But_In_Toolbar:
    def __init__(self,parent,colour,push_colour,name,command=None,bg_colour="white"):
        def check_but(e):
            self.tool_bar_but.itemconfig(self.line,state="normal")
            self.tool_bar_but["bg"] = bg_colour # #e4e4e4 f0f0f0
            for i,j in main_ui.tool_bar.but.items():
                if i == self.name:continue
                j.tool_bar_but.itemconfig(j.line,state="hidden")
                j.tool_bar_but["bg"] = bg_colour
            if self.command:self.command()
        self.name = name
        self.command = command
        self.tool_bar_but = Canvas(parent,name=name,width=90,height=41,bg=bg_colour,cursor="hand2",highlightthickness=0)
        self.tool_bar_but.pack()
        self.line = self.tool_bar_but.create_line(0,0,0,41,width=12,fill=push_colour,state="hidden")
        self.text = self.tool_bar_but.create_text(45,19,text=name,fill="#848383",font=["宋体",10])
        self.tool_bar_but.bind("<Enter>",lambda e: self.tool_bar_but.itemconfig(self.text,fill="#232323"))
        self.tool_bar_but.bind("<Leave>",lambda e: self.tool_bar_but.itemconfig(self.text,fill="#848383"))
        self.tool_bar_but.bind("<ButtonPress-1>",check_but)
        
'''工具栏'''
class Tool_Bar:
    def __init__(self,parent,x,y,colour,push_colour,height,bg_colour="white"):
        self.current_toolbar_state = "本地音频画布"
        self.toolbar_frame = Canvas(parent,name="工具栏",height=1000,width=90,bd=1,)#sunken#groove
        self.toolbar_frame.place(x=x,y=y)
        self.but = {}
        self.but["歌词"] = But_In_Toolbar(self.toolbar_frame,colour,push_colour,name="歌词",bg_colour=bg_colour,command=self.check_ge_ci)
        self.but["本地音频"] = But_In_Toolbar(self.toolbar_frame,colour,push_colour,name="本地音频",bg_colour=bg_colour,command=self.check_local_audio)
        self.but["我的记录"] = But_In_Toolbar(self.toolbar_frame,colour,push_colour,name="我的记录",bg_colour=bg_colour,command=self.check_my_record)
        self.but["全部歌词"] = But_In_Toolbar(self.toolbar_frame,colour,push_colour,name="全部歌词",bg_colour=bg_colour,command=self.check_all_geci)
        self.but["中英互译"] = But_In_Toolbar(self.toolbar_frame,colour,push_colour,name="中英互译",bg_colour=bg_colour,command=self.check_translation)
        Frame(self.toolbar_frame,name="end_frame",width=90,height=height-306,bg=bg_colour).pack()
    def hidden_ge_ci(self):
        main_ui.display_area_frame.ge_ci_canvas.cv["height"] = 0
        main_ui.display_area_frame.ge_ci_canvas.cv["width"] = 0
        for i in main_ui.display_area_frame.ge_ci_canvas.cv.find_all():
            main_ui.display_area_frame.ge_ci_canvas.cv.itemconfig(i,state="hidden")
    def hidden_local_audio(self):
        for i in main_ui.display_area_frame.local_audio_canvas.cv.find_all():
            main_ui.display_area_frame.local_audio_canvas.cv.itemconfig(i,state="hidden")
        main_ui.display_area_frame.local_audio_canvas.cv["height"] = 0
        main_ui.display_area_frame.local_audio_canvas.cv["width"] = 0
    def hidden_my_record(self):
        for i in main_ui.display_area_frame.my_record_canvas.cv.find_all():
            main_ui.display_area_frame.my_record_canvas.cv.itemconfig(i,state="hidden")
        main_ui.display_area_frame.my_record_canvas.cv["height"] = 0
        main_ui.display_area_frame.my_record_canvas.cv["width"] = 0 
    def hidden_all_geci(self):    
        for i in main_ui.display_area_frame.all_geci_canvas.cv.find_all():
            main_ui.display_area_frame.all_geci_canvas.cv.itemconfig(i,state="hidden")
        main_ui.display_area_frame.all_geci_canvas.cv["height"] = 0
        main_ui.display_area_frame.all_geci_canvas.cv["width"] = 0 
    def hidden_translation(self):
        for i in main_ui.display_area_frame.translation_canvas.cv.find_all():
            main_ui.display_area_frame.translation_canvas.cv.itemconfig(i,state="hidden")
        main_ui.display_area_frame.translation_canvas.cv["height"] = 0
        main_ui.display_area_frame.translation_canvas.cv["width"] = 0  
    
    def check_ge_ci(self):
        self.current_toolbar_state = "歌词画布"
        main_ui.display_area_frame.ge_ci_canvas.cv["height"] = main_ui.display_area_frame.ge_ci_canvas.height
        main_ui.display_area_frame.ge_ci_canvas.cv["width"] = main_ui.display_area_frame.ge_ci_canvas.width
        for i in main_ui.display_area_frame.ge_ci_canvas.cv.find_all():
            main_ui.display_area_frame.ge_ci_canvas.cv.itemconfig(i,state="normal")
        if main_ui.display_ge_ci.check_flag == False:main_ui.display_area_frame.ge_ci_canvas.cv.itemconfig(main_ui.display_area_frame.ge_ci_canvas.geci_text,state="hidden")
        self.hidden_local_audio()
        self.hidden_my_record()
        self.hidden_all_geci()
        self.hidden_translation()
        main_ui.display_area_frame.ge_ci_canvas.cv.lift(main_ui.display_area_frame.ge_ci_canvas.geci_text)
        
        
    def check_local_audio(self):
        self.current_toolbar_state = "本地音频画布"
        main_ui.display_area_frame.local_audio_canvas.cv["height"] = main_ui.display_area_frame.local_audio_canvas.height
        main_ui.display_area_frame.local_audio_canvas.cv["width"] = main_ui.display_area_frame.local_audio_canvas.width
        for i in main_ui.display_area_frame.local_audio_canvas.cv.find_all():
            main_ui.display_area_frame.local_audio_canvas.cv.itemconfig(i,state="normal") 
        self.hidden_ge_ci()
        self.hidden_my_record()
        self.hidden_all_geci()
        self.hidden_translation()
    def check_my_record(self):
        self.current_toolbar_state = "我的记录画布"
        main_ui.display_area_frame.my_record_canvas.cv["height"] = main_ui.display_area_frame.my_record_canvas.height
        main_ui.display_area_frame.my_record_canvas.cv["width"] = main_ui.display_area_frame.my_record_canvas.width
        for i in main_ui.display_area_frame.my_record_canvas.cv.find_all():
            main_ui.display_area_frame.my_record_canvas.cv.itemconfig(i,state="normal")

        self.hidden_ge_ci()
        self.hidden_local_audio()
        self.hidden_all_geci()
        self.hidden_translation()
        
        
    def check_all_geci(self):
        self.current_toolbar_state = "全部歌词画布"
        main_ui.display_area_frame.all_geci_canvas.cv["height"] = main_ui.display_area_frame.all_geci_canvas.height
        main_ui.display_area_frame.all_geci_canvas.cv["width"] = main_ui.display_area_frame.all_geci_canvas.width
        for i in main_ui.display_area_frame.all_geci_canvas.cv.find_all():
            main_ui.display_area_frame.all_geci_canvas.cv.itemconfig(i,state="normal")
        self.hidden_local_audio()
        self.hidden_ge_ci()
        self.hidden_my_record()
        self.hidden_translation()
    def check_translation(self):
        self.current_toolbar_state = "中英互译画布"
        main_ui.display_area_frame.translation_canvas.cv["height"] = main_ui.display_area_frame.translation_canvas.height
        main_ui.display_area_frame.translation_canvas.cv["width"] = main_ui.display_area_frame.translation_canvas.width
        for i in main_ui.display_area_frame.translation_canvas.cv.find_all():
            main_ui.display_area_frame.translation_canvas.cv.itemconfig(i,state="normal") 
        self.hidden_local_audio()
        self.hidden_ge_ci()
        self.hidden_my_record()  
        self.hidden_all_geci()

'''主显示框架'''
class Display_Area_Frame:
    def __init__(self,parent,x,y,width,height,colour,push_colour):
        img_path = None
        with open("db/img_path.txt",mode="r") as r:
            path = r.read()
            if exists(path):
                img_path = path

        self.width = width
        self.height = height
        self.main_frame = Frame(parent,name="主显示框架",width=self.width-90,height=self.height-101,bg="#aaaaaa",highlightthickness=0)
        self.main_frame.place(x=x+3,y=y)
        
        self.ge_ci_canvas = Ge_Ci_Canvas(self.main_frame,x=x,y=y,width=self.width,height=self.height,img_path=img_path,colour=colour,push_colour=push_colour)
        
        self.my_record_canvas = My_record_Canvas(self.main_frame,x=x,y=y,width=self.width,height=self.height,colour=colour,push_colour=push_colour)
        
        self.all_geci_canvas = All_Geci_Canvas(self.main_frame,x=x,y=y,width=self.width,height=self.height,colour=colour,push_colour=push_colour)
        
        self.translation_canvas = Translation_Canvas(self.main_frame,x=x,y=y,width=self.width,height=self.height,colour=colour,push_colour=push_colour)
        
        # self.help_canvas = Help_Canvas(self.main_frame,x=x,y=y,width=self.width,height=self.height,colour=colour,push_colour=push_colour)
        
        self.local_audio_canvas = Local_Audio_Canvas(self.main_frame,x=x,y=y,width=self.width,height=self.height,colour=colour,push_colour=push_colour)
              
'''歌词画布'''
class Ge_Ci_Canvas:  
    def __init__(self,parent,x,y,width,height,colour,push_colour,img_path=None):
        def changeSize(e):
            if self.img_path:
                self.im = resize(self.im_orig,(self.width,self.height))
                self.tkim = PhotoImage(fromarray(self.im))
                self.cv.itemconfig(self.bg_img,image=self.tkim)
            self.cv.itemconfig(self.geci_text,width=self.width-10)
        def move_text(e):
            if e.state == 8:
                if e.delta < 0: y = -20
                else :y = 20
                if self.cv.coords(self.geci_text)[1] + y == 40:return
                else: self.cv.move(self.geci_text,0,y)
        def normal_geci_size(e):
            self.cv.coords(self.geci_text,10,20)
            font_info = self.cv.itemcget(self.geci_text,"font")
            if "bold" in font_info:self.cv.itemconfig(self.geci_text,font=["Corbel",15,"bold"])
            else:self.cv.itemconfig(self.geci_text,font=["Corbel",15])
        def open_img_enter_colour(e):
            self.cv.itemconfig(self.open_img_but1,fill=colour)
            self.cv.itemconfig(self.open_img_but2,fill=colour)
            self.cv.itemconfig(self.open_img_but3,fill=colour)
        def open_img_leave_colour(e):
            self.cv.itemconfig(self.open_img_but1,fill=push_colour)
            self.cv.itemconfig(self.open_img_but2,fill=push_colour)
            self.cv.itemconfig(self.open_img_but3,fill=push_colour)
        def delete_img_enter_colour(e):
            self.cv.itemconfig(self.delete_img_but1,fill=colour)
            self.cv.itemconfig(self.delete_img_but2,fill=colour)
            self.cv.itemconfig(self.delete_img_but3,fill=colour)
            self.cv.itemconfig(self.delete_img_but4,fill=colour)
        def delete_img_leave_colour(e):
            self.cv.itemconfig(self.delete_img_but1,fill=push_colour)
            self.cv.itemconfig(self.delete_img_but2,fill=push_colour)
            self.cv.itemconfig(self.delete_img_but3,fill=push_colour)
            self.cv.itemconfig(self.delete_img_but4,fill=push_colour)
        def open_img_path(e):
            img_path = askopenfilename()
            if img_path:
                # print(img_path)
                self.img_path = img_path
                self.im_orig = cv_img = imdecode(fromfile(self.img_path,dtype="uint8"),-1)
                self.im_orig = self.im_orig[:, :, ::-1]  
                self.im = resize(self.im_orig,(self.width,self.height))
                self.tkim = PhotoImage(fromarray(self.im))            
                self.cv.itemconfig(self.bg_img,image=self.tkim)
            with open("db/img_path.txt",mode="w") as w:
                w.write(img_path)
        def delete_img(e):
            # print("删除")
            if self.img_path:
                self.img_path = None
                self.cv.itemconfig(self.bg_img,image="")
                del self.im_orig,self.im,self.tkim
            with open("db/img_path.txt",mode="w") as w:
                w.write("")

            # if player.drop_imgfile: 
                # print("存在")
                # self.open_img_path(1)
            # player.drop_imgfile = ""
            # print("结束")
        def change_geci_colour(e):
            geci_colour = askcolor()
            # print(geci_colour[-1])
            self.cv.itemconfig(self.geci_text,fill=geci_colour[-1])
            with open("db/geci_colour.txt",mode="w") as w:
                if not geci_colour[-1]:return
                w.write(geci_colour[-1])
        def geci_bold_but(e):
            if self.bold_flag:
                self.bold_flag = False
                self.cv.itemconfig(self.geci_text,font=["Corbel",int("".join(findall("([\d]+)",self.cv.itemcget(self.geci_text,"font")))),"bold"])
            else:
                self.bold_flag = True
                self.cv.itemconfig(self.geci_text,font=["Corbel",int("".join(findall("([\d]+)",self.cv.itemcget(self.geci_text,"font"))))])
        def geci_bianda(e):
            font_info = self.cv.itemcget(self.geci_text,"font")
            if "bold" in font_info:self.cv.itemconfig(self.geci_text,font=["Corbel",int("".join(findall("([\d]+)",font_info)))+2,"bold"])  
            else:self.cv.itemconfig(self.geci_text,font=["Corbel",int("".join(findall("([\d]+)",font_info)))+2])   
        def geci_jianxiao(e):
            font_info = self.cv.itemcget(self.geci_text,"font")
            if "bold" in font_info:self.cv.itemconfig(self.geci_text,font=["Corbel",int("".join(findall("([\d]+)",font_info)))-2,"bold"])
            else:self.cv.itemconfig(self.geci_text,font=["Corbel",int("".join(findall("([\d]+)",font_info)))-2])
        self.width = width-90
        self.height = height-101
        self.delete_img = delete_img
        self.img_path = img_path
        # self.img_path = None
        self.bold_flag = True
        self.cv = Canvas(parent,name="歌词画布",width=self.width,height=self.height,bg="#f3f3f3",highlightthickness=0)
        self.cv.place(x=0,y=0)
        
        self.bg_img = self.cv.create_image(0,0,anchor="nw")
        
        if self.img_path:
            self.im_orig = cv_img = imdecode(fromfile(self.img_path,dtype="uint8"),-1)
            # self.im_orig = imread(img_path)
            self.im_orig = self.im_orig[:, :, ::-1]   
            self.bg_img = self.cv.create_image(0,0,anchor="nw") 
        

            
        
        self.geci_text = self.cv.create_text(10,20,width=self.width-10,text="“We wanted to give people an opportunity  to actually see the calories before they purchase the food and make a decision, an informed decision that if they want to make the healthier choice, if they want to eat fewer calories, they can. And we expect this will have a huge impact on obesity. And of course, if it has an impact on obesity, it will have an impact on diabetes and heart disease and high blood pressure. ”",fill="black",font=['Corbel',15],anchor="nw")#nw
        with open("db/geci_colour.txt",mode="r") as r:
            gcColour = r.read()
            if gcColour: self.cv.itemconfig(self.geci_text,fill=gcColour)
                
        self.bigger_font = self.cv.create_line(40,5,40,6,40,5,40,15,40,10,35,10,45,10,44,10,fill=push_colour,width=2)
        self.smaller_font = self.cv.create_line(15,10,10,10,20,10,19,10,fill=push_colour,width=2)    
        
        self.open_img_but1 = self.cv.create_line(60,5,72,5,72,15,60,15,60,5,fill=push_colour,width=1)    
        self.open_img_but2 = self.cv.create_arc(62,10,68,17,fill=push_colour,extent=550,outline="")  
        self.open_img_but3 = self.cv.create_oval(68,7,70,9,fill=push_colour,outline="")  
        self.cv.tag_bind(self.open_img_but1,"<Enter>",open_img_enter_colour)
        self.cv.tag_bind(self.open_img_but2,"<Enter>",open_img_enter_colour)
        self.cv.tag_bind(self.open_img_but3,"<Enter>",open_img_enter_colour)
        self.cv.tag_bind(self.open_img_but1,"<Leave>",open_img_leave_colour)
        self.cv.tag_bind(self.open_img_but2,"<Leave>",open_img_leave_colour)
        self.cv.tag_bind(self.open_img_but3,"<Leave>",open_img_leave_colour)
        self.cv.tag_bind(self.open_img_but1,"<ButtonPress-1>",open_img_path)
        self.cv.tag_bind(self.open_img_but2,"<ButtonPress-1>",open_img_path)
        self.cv.tag_bind(self.open_img_but3,"<ButtonPress-1>",open_img_path)
        
        self.delete_img_but1 = self.cv.create_line(88,5,100,5,100,15,88,15,88,5,fill=push_colour,width=1)    
        self.delete_img_but2 = self.cv.create_arc(90,10,96,17,fill=push_colour,extent=550,outline="")  
        self.delete_img_but3 = self.cv.create_oval(96,7,98,9,fill=push_colour,outline="")
        self.delete_img_but4 = self.cv.create_line(87,3,101,17,fill=push_colour,width=2)        
        self.cv.tag_bind(self.delete_img_but1,"<Enter>",delete_img_enter_colour)
        self.cv.tag_bind(self.delete_img_but2,"<Enter>",delete_img_enter_colour)
        self.cv.tag_bind(self.delete_img_but3,"<Enter>",delete_img_enter_colour)
        self.cv.tag_bind(self.delete_img_but4,"<Enter>",delete_img_enter_colour)
        self.cv.tag_bind(self.delete_img_but1,"<Leave>",delete_img_leave_colour)
        self.cv.tag_bind(self.delete_img_but2,"<Leave>",delete_img_leave_colour)
        self.cv.tag_bind(self.delete_img_but3,"<Leave>",delete_img_leave_colour)
        self.cv.tag_bind(self.delete_img_but4,"<Leave>",delete_img_leave_colour)
        self.cv.tag_bind(self.delete_img_but1,"<ButtonPress-1>",delete_img)
        self.cv.tag_bind(self.delete_img_but2,"<ButtonPress-1>",delete_img)
        self.cv.tag_bind(self.delete_img_but3,"<ButtonPress-1>",delete_img)
        self.cv.tag_bind(self.delete_img_but4,"<ButtonPress-1>",delete_img)
        
        self.text_colour_but1 = self.cv.create_rectangle(116,5,129,16,fill=push_colour,outline="")
        self.text_colour_but2 = self.cv.create_text(122,10,text="TC",anchor="center",font=["Corbel",8],fill="#f1f1f1")
        self.cv.tag_bind(self.text_colour_but2,"<Enter>",lambda e:self.cv.itemconfig(self.text_colour_but1,fill=colour))
        self.cv.tag_bind(self.text_colour_but2,"<Leave>",lambda e:self.cv.itemconfig(self.text_colour_but1,fill=push_colour))
        self.cv.tag_bind(self.text_colour_but2,"<ButtonPress-1>",change_geci_colour)
        
        self.text_bold1 = self.cv.create_rectangle(144,5,157,16,fill=push_colour,outline="")
        self.text_bold2 = self.cv.create_text(150,10,text="B",anchor="center",font=["Corbel",9],fill="#f1f1f1")
        self.cv.tag_bind(self.text_bold2,"<Enter>",lambda e:self.cv.itemconfig(self.text_bold1,fill=colour))
        self.cv.tag_bind(self.text_bold2,"<Leave>",lambda e:self.cv.itemconfig(self.text_bold1,fill=push_colour))
        self.cv.tag_bind(self.text_bold2,"<ButtonPress-1>",geci_bold_but)
        
        self.cv.tag_bind(self.bigger_font,"<Enter>",lambda e: self.cv.itemconfig(self.bigger_font,fill=colour))
        self.cv.tag_bind(self.bigger_font,"<Leave>",lambda e: self.cv.itemconfig(self.bigger_font,fill=push_colour))
        self.cv.tag_bind(self.bigger_font,"<ButtonPress-1>",geci_bianda)
        
        self.cv.tag_bind(self.smaller_font,"<Enter>",lambda e: self.cv.itemconfig(self.smaller_font,fill=colour))
        self.cv.tag_bind(self.smaller_font,"<Leave>",lambda e: self.cv.itemconfig(self.smaller_font,fill=push_colour))
        self.cv.tag_bind(self.smaller_font,"<ButtonPress-1>",geci_jianxiao)
        
        self.cv.bind_all("<Control-MouseWheel>",lambda e:0 if e.state != 12 else (geci_bianda(e) if e.delta < 0 else geci_jianxiao(e)))
        self.cv.bind_all("<Control-Key-->",lambda e: geci_jianxiao(e) if e.keycode == 189 or e.keycode == 109 else 1)
        # self.cv.bind_all("<Control-Key-->",lambda e: print(e.keycode))
        self.cv.bind_all("<Control-Key-+>",lambda e:geci_bianda(e))
        self.cv.bind('<Configure>', changeSize)  
        self.cv.bind('<MouseWheel>',move_text)  
        self.cv.bind('<Double-Button-2>',normal_geci_size)  
        
        # self.cv.bind_all('<Control-Up>',lambda e: main_ui.tool_bar.check_ge_ci()) 
        self.cv.bind_all('<Control-Up>',lambda e: self.display_geci_frame()) 
        
    def change_geci(self,geci):
        self.cv.itemconfig(self.geci_text,text=geci)

    def display_geci_frame(self):
        if main_ui.tool_bar.but["歌词"].tool_bar_but.itemcget(main_ui.tool_bar.but["歌词"].line,"state") == "hidden":
            main_ui.tool_bar.but["歌词"].tool_bar_but.itemconfig(main_ui.tool_bar.but["歌词"].line,state="normal")
            main_ui.tool_bar.but["歌词"].tool_bar_but["bg"] = "white" 
            for i,j in main_ui.tool_bar.but.items():
                if i == main_ui.tool_bar.but["歌词"].name:continue
                j.tool_bar_but.itemconfig(j.line,state="hidden")
                j.tool_bar_but["bg"] = "white"
            if main_ui.tool_bar.but["歌词"].command:main_ui.tool_bar.but["歌词"].command()
        
'''本地音频画布'''
class Local_Audio_Canvas:    
    def __init__(self,parent,x,y,width,height,colour,push_colour):
        def ask_open_file(e):
            file_directory = askdirectory()
            if not file_directory:return
            open_file(file_directory)

        def open_file(file_directory):
            player.file_directory = file_directory
            if player.file_directory:
                self.cv.itemconfig(self.display_file_directory_name,text="%s"%(player.file_directory))
                '''Open File And Display File/crear list'''
                for i in range(len(self.all_file)):
                    self.cv.delete(self.all_file[i][0])
                    self.cv.delete(self.all_file[i][1])
                    self.cv.delete(self.all_file[i][2])
                    self.cv.delete(self.all_file[i][3])
                self.all_file = []   
                for i in listdir(player.file_directory):
                    file_format = i[-3:].lower()
                    if file_format == "mp3" or file_format == "wav":
                        audio = MP3(player.file_directory+"/"+i)
                        player.music_dic[i] = audio.info.length
                        self.creat_a_file(i,lib.sec_convert_formatsec(audio.info.length))
                with open("db/directory.txt",mode="w") as w:
                    w.write(player.file_directory)
                    
        def changeSize(e):
            self.cv.itemconfig(self.display_file_directory_name,width=self.width-2)
            self.cv.coords(self.rectangle_title,80,30,self.width-80,60)
            self.cv.coords(self.rectangle_musiclength,self.width-80,30,self.width,60)
            self.cv.coords(self.music_title,self.width/2,45)
            self.cv.coords(self.music_length,self.width-45,45)

            
            for i in range(len(self.all_file)):
                self.cv.coords(self.all_file[i][0],-1,60+(i*30),self.width,60+(i+1)*30)
                self.cv.coords(self.all_file[i][2],self.width/2,60+(i+1)*30 -15)
                self.cv.coords(self.all_file[i][3],self.width-45,60+(i+1)*30 -15)
        def move_musicfile(e):
            if e.state == 8:
                if e.delta < 0: y = 5
                else :y = -5
                self.cv.yview("scroll", y, "units")
        self.width = width-90
        self.height = height-101
        self.all_file = []
        self.colour = colour
        self.open_file = open_file
        self.cv = Canvas(parent,name="本地音频画布",width=self.width,height=self.height,bg="white",highlightthickness=0,scrollregion=(0,0,self.width,self.height))
        self.cv.place(x=0,y=0)
        # self.local_audio_text = self.cv.create_text(self.width/2-10,15,text="本地音频",fill=push_colour,font=["宋体",12],anchor="center")
        self.open_file_but = self.cv.create_text(7,10,width=self.width-2,text="选择目录",fill=push_colour,font=["宋体",10],anchor="nw")
        self.display_file_directory_name = self.cv.create_text(65,10,width=self.width-2,fill="#878787",font=["宋体",9],anchor="nw")

        self.rectangle_xuhao = self.cv.create_rectangle(-1,30,80,60,fill="white",outline="#e2e0e0")
        self.rectangle_title = self.cv.create_rectangle(80,30,self.width-80,60,fill="white",outline="#e2e0e0")
        self.rectangle_musiclength = self.cv.create_rectangle(self.width-80,30,self.width,60,fill="white",outline="#e2e0e0")
        self.music_title = self.cv.create_text(self.width/2,45,text="文件名",fill="#878787",font=["宋体",10],anchor="center")
        self.music_length = self.cv.create_text(self.width-45,45,text="时长",fill="#878787",font=["宋体",10],anchor="center")
        self.music_xuhao = self.cv.create_text(45,45,text="序号",fill="#878787",font=["宋体",10],anchor="center")
        
        dy = -50
        self.laba_1 = self.cv.create_rectangle(3,6+dy,8,13+dy,fill=self.colour,width=0)
        self.laba_2 = self.cv.create_polygon(8,6+dy,14,2+dy,14,17+dy,8,13+dy,fill=self.colour)
        self.laba_3 = self.cv.create_arc(22,1+dy,12,18+dy,start=-45,style="arc",outline=self.colour)
        self.laba_4 = self.cv.create_arc(18,2+dy,8,17+dy,start=-45,style="arc",outline=self.colour)

        with open("db/directory.txt",mode="r") as r:
            directory = r.read()
        if exists(directory): 
            open_file(directory)
        
        self.cv.bind('<MouseWheel>',move_musicfile)  
        self.cv.tag_bind(self.open_file_but,"<Enter>",lambda e: self.cv.itemconfig(self.open_file_but,fill=colour))
        self.cv.tag_bind(self.open_file_but,"<Leave>",lambda e: self.cv.itemconfig(self.open_file_but,fill=push_colour))
        self.cv.tag_bind(self.open_file_but,"<ButtonPress-1>",ask_open_file)
        self.cv.bind('<Configure>', changeSize)
        self.cv.bind('<Double-Button-2>',lambda e:self.cv.yview("moveto",0)) 
    def check_single_item(self,file_rec_area,filename):
        # print(filename)
        if "循环中" == main_ui.repeat_stence_btn.current_state:
            main_ui.repeat_stence_btn.push_but(0)
        if main_ui.button_play_or_pause.current_state == "播放":
            main_ui.button_play_or_pause.play_or_pause_left(1)
        dy = self.cv.coords(file_rec_area)[1]+6
        self.cv.lift(self.laba_1)
        self.cv.lift(self.laba_2)
        self.cv.lift(self.laba_3)
        self.cv.lift(self.laba_4)
        
        

        
        self.cv.coords(self.laba_1,3,6+dy,8,13+dy)
        self.cv.coords(self.laba_2,8,6+dy,14,2+dy,14,17+dy,8,13+dy)
        self.cv.coords(self.laba_3,22,1+dy,12,18+dy)
        self.cv.coords(self.laba_4,18,2+dy,8,17+dy)
        print("ID:",file_rec_area,"  file name:",filename)
        
        
        if main_ui.button_beisu.current_state == "有倍速":
            main_ui.button_beisu.time_ = 0
        
        '''check File and play,display 1.title 2.歌词 3. 进度条'''
        
        player.current_music_name = filename
        player.current_music_length = player.music_dic[filename]
        # print(player.file_directory +"/" + filename)
        player.set_music(player.file_directory +"/" + filename)
        main_ui.music_title.mus_title["text"] = filename
        main_ui.jin_du_tiao.full_time["text"] = lib.sec_convert_formatsec(player.current_music_length)
        
        if main_ui.button_beisu.current_state == "有倍速":
            main_ui.button_beisu.time_ = 0

        for i in self.all_file:
            self.cv.itemconfig(i[0],fill="white")
        self.cv.itemconfig(file_rec_area,fill="#e8e6e6")
        self.cv.tag_unbind(file_rec_area,"<Leave>")
        self.cv.tag_unbind(file_rec_area,"<Enter>")
        
        main_ui.tool_bar.check_local_audio()
        
    def creat_a_file(self,filename,filelength):
        file_rec_area = self.cv.create_rectangle(-1,60+(len(self.all_file)*30),self.width,60+(len(self.all_file)+1)*30,outline="#e2e0e0",fill="white")
        music_xuhao = self.cv.create_text(45, 60+(len(self.all_file)+1)*30 -15,text=len(self.all_file)+1,fill="#878787",font=["宋体",10],anchor="center")
        music_title = self.cv.create_text(self.width/2,60+(len(self.all_file)+1)*30 -15,text=filename,fill="#878787",font=["宋体",10],anchor="center")
        music_length = self.cv.create_text(self.width-45,60+(len(self.all_file)+1)*30 -15,text=filelength,fill="#878787",font=["宋体",10],anchor="center")
        self.all_file.append((file_rec_area,music_xuhao,music_title,music_length)) 
        
        self.cv.tag_bind(file_rec_area,"<Enter>",lambda e:self.cv.itemconfig(file_rec_area,fill="#f2f1f1"))
        self.cv.tag_bind(file_rec_area,"<Leave>",lambda e:self.cv.itemconfig(file_rec_area,fill="white"))
        self.cv.tag_bind(file_rec_area,"<Double-ButtonPress-1>",lambda e:self.check_single_item(file_rec_area,self.cv.itemcget(music_title,"text")))
        self.cv.tag_bind(music_title,"<Double-ButtonPress-1>",lambda e:self.check_single_item(file_rec_area,self.cv.itemcget(music_title,"text")))
        self.cv.tag_bind(music_length,"<Double-ButtonPress-1>",lambda e:self.check_single_item(file_rec_area,self.cv.itemcget(music_title,"text")))
        self.cv["scrollregion"] = (0,0,self.width,self.cv.coords(self.all_file[-1][0])[-1])
   
'''我的记录画布'''
class My_record_Canvas:    
    def __init__(self,parent,x,y,width,height,colour,push_colour):
        def changeSize(e):
            self.cv.coords(self.seprate_line,0,30,self.width,30)
            self.cv.coords(self.myrecord_text,self.width/2-10,15)
            for i in range(len(self.all_sentence)):
                if not self.all_sentence[i]:continue
                a = self.cv.coords(self.all_sentence[i][0])
                self.cv.coords(self.all_sentence[i][0],a[0],a[1],self.width,a[1]+30)
        def move_seentence(e):
            if e.state == 8:
                if e.delta < 0: y = 5
                else :y = -5
                self.cv.yview("scroll", y, "units")
        def stentence_daoxu(e):
            daoxu_list = []
            id_list = []
            for i in self.all_sentence:
                if not i:continue
                a = []
                for j in i:
                    a.append(self.cv.coords(j))
                daoxu_list.insert(0,a)
                id_list.append(i)
            for i,j in zip(id_list,daoxu_list):
                for s,d in zip(i,j):
                    self.cv.coords(s,d)
            if self.current_shun_xu == "顺序":
                self.current_shun_xu = "倒序"
                self.cv.coords(self.daoxu_but,37,20,51,20,44,13)
            else :
                self.current_shun_xu = "顺序"
                self.cv.coords(self.daoxu_but,38,14,50,14,44,20)
                
                
                
        self.width = width-90
        self.height = height-101
        self.all_sentence = []
        self.record_sentence = []
        self.colour = colour
        self.push_colour = push_colour
        self.parent = parent
        self.stentence_daoxu = stentence_daoxu
        self.push_colour = push_colour
        self.current_shun_xu = "顺序"
        self.move_seentence = move_seentence
        self.changeSize = changeSize
        self.cv = Canvas(self.parent,name="我的记录画布",width=self.width,height=self.height,bg="white",highlightthickness=0,scrollregion=(0,0,self.width,10**30))
        self.cv.place(x=0,y=0)
        self.myrecord_text = self.cv.create_text(self.width/2-10,15,text="我的记录",fill=self.push_colour,font=["宋体",12],anchor="center")
        self.seprate_line = self.cv.create_line(0,30,self.width,30,fill="#e2e0e0")
        self.seprate_daoxu_but = self.cv.create_polygon(-1,-1,90,-1,90,30,-1,30,fill="white",outline="#e2e0e0")
        self.daoxu_but = self.cv.create_polygon(38,14,50,14,44,20,fill=self.colour,activefill=self.push_colour)
        self.cv.tag_bind(self.seprate_daoxu_but,"<Enter>",lambda e:self.cv.itemconfig(self.daoxu_but,fill=self.push_colour))
        self.cv.tag_bind(self.seprate_daoxu_but,"<Leave>",lambda e:self.cv.itemconfig(self.daoxu_but,fill=self.colour))
        self.cv.tag_bind(self.seprate_daoxu_but,"<Button-1>",self.stentence_daoxu)
        self.cv.tag_bind(self.daoxu_but,"<Button-1>",self.stentence_daoxu)
        self.cv.bind('<MouseWheel>',self.move_seentence)  
        self.cv.bind('<Configure>',self.changeSize)
        self.cv.bind('<Double-Button-2>',lambda e:self.cv.yview("moveto",0)) 
        
        self.read_record_sentence()


    def check_single_sentence(self,sentence):
        if "循环中" == main_ui.repeat_stence_btn.current_state:
            main_ui.repeat_stence_btn.push_but(0)
        if main_ui.button_play_or_pause.current_state == "播放":
            main_ui.button_play_or_pause.play_or_pause_left(1)
        # print(sentence)
        sentence_info = ""
        for i in self.record_sentence:
            for s in i.keys():
                if s == sentence:
                    sentence_info = i[s]
        if not sentence_info:return
        '''check File and play,display 1.title 2.歌词 3. 进度条'''
        file_audio_path = sentence_info['file_audio_path'].strip()
        if not isfile(file_audio_path):return
        directory_and_filename = split(file_audio_path)
        

        player.current_music_name = directory_and_filename[1]
        player.file_directory = directory_and_filename[0]
        
        audio = MP3(file_audio_path)
        player.current_music_length = audio.info.length
        player.set_music(file_audio_path)
        main_ui.music_title.mus_title["text"] = player.current_music_name
        main_ui.jin_du_tiao.full_time["text"] = lib.sec_convert_formatsec(player.current_music_length)
        
        if main_ui.button_beisu.current_state == "有倍速":
            main_ui.button_beisu.time_ = sentence_info['sentence_start_time']
        else:
            player.set_position(sentence_info['sentence_start_time'] * 1000)
        
        main_ui.display_area_frame.local_audio_canvas.open_file(directory_and_filename[0])
        
        main_ui.tool_bar.check_my_record()
        
# 1.打开程序时，读取txt所有的句子到内存  2.按下记录按钮先将句子添加到程序列表中，再读取列表中的句子保存到txt中 3.按下删除按钮先将程序中句子删除，再读取列表中句子保存到txt中
    def read_record_sentence(self):
        f = open('db/sentence_rcord.txt','r')
        for line in f:
            sentence_dict = loads(line.strip())
            self.record_sentence.append(sentence_dict)
            for i in sentence_dict.keys():
                # print(bool(i),i)
                self.creat_a_sentence(i)
        f.close()
        
    def save_sentence_to_txt(self):
        with open('db/sentence_rcord.txt','w') as w:
            for line in self.record_sentence:
                w.write(dumps(line)+"\n")

        
    def delete_single_sentence(self,sentence,all_sentence_index):
        flag = False
        if self.current_shun_xu == "倒序":
            self.stentence_daoxu(1)
            flag = True
        print(sentence)
        for i in self.record_sentence:
            for l in i.keys():
                if l == sentence:
                    self.record_sentence.remove(i)
        self.save_sentence_to_txt()
        for i in self.all_sentence[all_sentence_index]:
            self.cv.delete(i)
        for i in range(all_sentence_index,len(self.all_sentence)-1):
            if not self.all_sentence[i+1]:continue
            for j in range(0,7):
                self.cv.move(self.all_sentence[i+1][j],0,-30)
        self.all_sentence[all_sentence_index] = False
        self.pai_xu()
        if self.all_sentence:
            self.cv["scrollregion"] = (0,0,self.width,(len(self.all_sentence)*30+150))
        if flag:self.stentence_daoxu(1)
    def pai_xu(self):
        count = 1
        for i in self.all_sentence:
            if not i:continue
            self.cv.itemconfig(i[4],text="{}.".format(count))
            count += 1
            
    def creat_a_sentence(self,sentence):
        all_sentence_index = len(self.all_sentence) 
        yy = len(self.record_sentence) -1
        sentence_rec_area = self.cv.create_rectangle((-1,30+yy*30),self.width,30+(yy+1)*30,outline="#e2e0e0",fill="white",activefil="#f2f1f1")
        sentence_ = self.cv.create_text(105,30+(yy+1)*30 -20,text=sentence,fill="#878787",font=["宋体",10],anchor="nw")
        
        circle_open_expand = self.cv.create_rectangle(1,30+(yy*30)+1,30,30+(yy+1)*30,outline="",fill="white")
        circle_open = self.cv.create_oval(5,30+(yy+1)*30 -23,22,30+(yy+1)*30 -6,outline="",fill=self.colour)
        
        circle_delete_expand = self.cv.create_rectangle(30,30+(yy*30)+1,60,30+(yy+1)*30,outline="",fill="white")
        circle_delete = self.cv.create_line(40,30+(yy+1)*30 -22,54,30+(yy+1)*30-8,47,30+(yy+1)*30 -15,40,30+(yy+1)*30-8,54,30+(yy+1)*30 -22,fill=self.colour,width=3)
        
        sentence_xuhao = self.cv.create_text(85,30+(yy+1)*30 -20,text="{}.".format(yy+1),fill="#878787",font=["宋体",10],anchor="n")
        
        if self.all_sentence:
            self.cv["scrollregion"] = (0,0,self.width,(len(self.all_sentence)*30+150))
        
        self.cv.tag_bind(circle_open,"<Enter>",lambda e:self.cv.itemconfig(circle_open,fill=self.push_colour))
        self.cv.tag_bind(circle_open_expand,"<Enter>",lambda e:self.cv.itemconfig(circle_open,fill=self.push_colour))
        self.cv.tag_bind(circle_open,"<Leave>",lambda e:self.cv.itemconfig(circle_open,fill=self.colour))
        self.cv.tag_bind(circle_open_expand,"<Leave>",lambda e:self.cv.itemconfig(circle_open,fill=self.colour))
        
        self.cv.tag_bind(circle_open,"<ButtonPress-1>",lambda e:self.check_single_sentence(sentence))
        self.cv.tag_bind(circle_open_expand,"<ButtonPress-1>",lambda e:self.check_single_sentence(sentence))
        
        self.cv.tag_bind(sentence_rec_area,"<Double-ButtonPress-1>",lambda e:self.check_single_sentence(sentence))
        self.cv.tag_bind(sentence_,"<Double-ButtonPress-1>",lambda e:self.check_single_sentence(sentence))
        self.cv.tag_bind(sentence_,"<Enter>",lambda e:self.cv.itemconfig(sentence_rec_area,fill="#f2f1f1"))
        self.cv.tag_bind(sentence_,"<Leave>",lambda e:self.cv.itemconfig(sentence_rec_area,fill="white"))
        self.cv.tag_bind(sentence_xuhao,"<Double-ButtonPress-1>",lambda e:self.check_single_sentence(sentence))
        
        self.cv.tag_bind(circle_delete,"<Enter>",lambda e:self.cv.itemconfig(circle_delete,fill=self.push_colour))
        self.cv.tag_bind(circle_delete_expand,"<Enter>",lambda e:self.cv.itemconfig(circle_delete,fill=self.push_colour))
        self.cv.tag_bind(circle_delete,"<Leave>",lambda e:self.cv.itemconfig(circle_delete,fill=self.colour))
        self.cv.tag_bind(circle_delete_expand,"<Leave>",lambda e:self.cv.itemconfig(circle_delete,fill=self.colour))
        self.cv.tag_bind(circle_delete,"<ButtonPress-1>",lambda e:self.delete_single_sentence(sentence,all_sentence_index))
        self.cv.tag_bind(circle_delete_expand,"<ButtonPress-1>",lambda e:self.delete_single_sentence(sentence,all_sentence_index))
        
        self.all_sentence.append([sentence_rec_area,sentence_,circle_open,circle_delete,sentence_xuhao,circle_open_expand,circle_delete_expand])
        
'''全部歌词画布'''
class All_Geci_Canvas:    
    def __init__(self,parent,x,y,width,height,colour,push_colour):
        def changeSize(e):
            self.cv.coords(self.allgeci_text,self.width/2-10,15)
            for i in range(len(self.all_sentence)):
                if self.all_sentence[i]:
                    self.cv.coords(self.all_sentence[i][0],-1,30+(i*30),self.width,30+(i+1)*30)
        def move_seentence(e):
            if e.state == 8:
                if e.delta < 0: y = 8
                else :y = -8
                self.cv.yview("scroll", y, "units")
    
        self.width = width-90
        self.height = height-101
        self.all_sentence = []
        self.move_seentence = move_seentence
        self.changeSize = changeSize
        self.parent = parent
        self.push_colour = push_colour
        self.cv_init_()
    def cv_init_(self):
        self.cv = Canvas(self.parent,name="全部歌词画布",width=self.width,height=self.height,bg="white",highlightthickness=0,scrollregion=(0,0,self.width,self.height))
        self.cv.place(x=0,y=0)
        self.allgeci_text = self.cv.create_text(self.width/2-10,15,text="全部歌词",fill=self.push_colour,font=["宋体",12],anchor="center")
        self.seprate_line = self.cv.create_line(0,30,self.width,30,fill="#e2e0e0")
        self.cv.bind('<MouseWheel>',self.move_seentence)  
        self.cv.bind('<Configure>', self.changeSize)
        self.cv.bind('<Double-Button-2>',lambda e:self.cv.yview("moveto",0)) 
    def check_single_sentence(self,sentence_time,sentence):
        if "循环中" == main_ui.repeat_stence_btn.current_state:
            main_ui.repeat_stence_btn.push_but(0)
        if main_ui.button_play_or_pause.current_state == "播放":
            main_ui.button_play_or_pause.play_or_pause_left(1)
        if main_ui.button_beisu.current_state == "有倍速":
            main_ui.button_beisu.time_ = lib.min_to_sec(sentence_time + ":00")
            return
        player.set_position(lib.min_to_sec(sentence_time + ":00") * 1000)
        
    def clear_all(self):
        if self.all_sentence:
            # for i in self.all_sentence:
                # for j in i:
                    # self.cv.delete(j)
            self.cv_init_()
            # main_ui.tool_bar.check_local_audio()
            self.all_sentence = []

    def creat_a_sentence(self,sentence_time,sentence):
        sentence_rec_area = self.cv.create_rectangle(-1,30+(len(self.all_sentence)*30),self.width,30+(len(self.all_sentence)+1)*30,outline="#e2e0e0",fill="white",activefil="#f2f1f1")
        sentence_ = self.cv.create_text(70,30+(len(self.all_sentence)+1)*30 -20,text=sentence,fill="#878787",font=["宋体",10],anchor="nw")
        sentencetime_ = self.cv.create_text(15,30+(len(self.all_sentence)+1)*30 -20,text=sentence_time,fill="#878787",font=["宋体",10],anchor="nw")
        
        self.all_sentence.append([sentence_rec_area,sentence_,sentencetime_])
        self.cv["scrollregion"] = (0,0,self.width,self.cv.coords(self.all_sentence[-1][0])[-1])

        self.cv.tag_bind(sentence_,"<Enter>",lambda e:self.cv.itemconfig(sentence_rec_area,fill="#f2f1f1"))
        self.cv.tag_bind(sentence_,"<Leave>",lambda e:self.cv.itemconfig(sentence_rec_area,fill="white"))
        self.cv.tag_bind(sentencetime_,"<Enter>",lambda e:self.cv.itemconfig(sentence_rec_area,fill="#f2f1f1"))
        self.cv.tag_bind(sentencetime_,"<Leave>",lambda e:self.cv.itemconfig(sentence_rec_area,fill="white"))
        self.cv.tag_bind(sentence_rec_area,"<Double-Button-1>",lambda e:self.check_single_sentence(sentence_time,sentence))
        self.cv.tag_bind(sentence_,"<Double-Button-1>",lambda e:self.check_single_sentence(sentence_time,sentence))
        self.cv.tag_bind(sentencetime_,"<Double-Button-1>",lambda e:self.check_single_sentence(sentence_time,sentence))

'''中英互译画布'''
class Translation_Canvas:
    def __init__(self,parent,x,y,width,height,colour,push_colour):
        def changeSize(e):     
            self.cv.coords(self.translation_text,self.width/2-10,15)
            self.input_text["width"] = int(self.width*0.11)
            self.input_text["height"] = self.height*0.02
            self.output_text["width"] = int(self.width*0.11)
            self.output_text["height"] = self.height*0.02
            self.cv.coords(self.output_text_window,1,self.height)
        self.width = width-90
        self.height = height-101
        self.fanyi = False
        self.translate_thread = Thread(target=self.translate_target)
        self.translate_thread.start()
        
        self.cv = Canvas(parent,name="中英互译画布",width=self.width,height=self.height,bg="white",highlightthickness=0,scrollregion=(0,0,self.width,self.height))
        self.cv.place(x=0,y=0)
        self.translation_text = self.cv.create_text(self.width/2-10,15,text="中英互译",fill=push_colour,font=["宋体",12],anchor="center")
        
        self.but_translation1 = self.cv.create_rectangle(5,4,60,26,fill=colour,outline="")
        self.but_translation2 = self.cv.create_text(32,15,anchor="center",fill="white",text="翻译")
        
        self.input_text = Text(self.cv,width=int(self.width*0.11), height=self.height*0.02,bd=0,bg='#f3f3f3',font=["微软雅黑",12],selectbackground="#bce5ff",selectforeground="black",undo=True)
        self.input_text_window = self.cv.create_window(1,30,window=self.input_text,anchor="nw")
        self.input_text.insert(1.0,"此框输入需要翻译的内容")
        
        self.output_text = Text(self.cv,width=int(self.width*0.11), height=self.height*0.02,bd=0,bg='#f3f3f3',font=["微软雅黑",12],selectbackground="#bce5ff",selectforeground="black")
        self.output_text_window = self.cv.create_window(1,self.height,window=self.output_text,anchor="sw")
        
        self.cv.bind('<Configure>', changeSize)
        self.cv.tag_bind(self.input_text_window,'<Control-KeyPress-Z>', lambda e:self.input_text.undo())
        self.cv.tag_bind(self.but_translation1,"<Enter>",lambda e:self.cv.itemconfig(self.but_translation1,fill=push_colour))
        self.cv.tag_bind(self.but_translation2,"<Enter>",lambda e:self.cv.itemconfig(self.but_translation1,fill=push_colour))
        self.cv.tag_bind(self.but_translation1,"<Leave>",lambda e:self.cv.itemconfig(self.but_translation1,fill=colour))
        self.cv.tag_bind(self.but_translation2,"<Leave>",lambda e:self.cv.itemconfig(self.but_translation1,fill=colour))
        self.cv.tag_bind(self.but_translation1,"<Button-1>",lambda e:self.translate_sentence())
        self.cv.tag_bind(self.but_translation2,"<Button-1>",lambda e:self.translate_sentence())
    def translate_sentence(self):
        self.fanyi = True
    def translate_target(self):
        while True:
            sleep(0.2)
            if self.fanyi:
                content = self.input_text.get(1.0,"end")
                if content.strip("\n\n\n") == "":return
                result = main_translate_sentence(content)
                self.output_text.delete('1.0','end')
                self.output_text.insert("end",result)
                self.fanyi = False
    
'''主UI'''
class Main_UI:
    def __init__(self,col = ["#ff8080","#cc6666"]):
        self.creat_new_directory()
        with open("db/colour.txt",mode="r") as r:
            info = r.read()
            if info: col = loads(info)
        self.col = col
        self.bg_colour = "white"
        self.win = Tk()
        
        # self.win.attributes("-transparentcolo","#f3f3f3")
        hook_dropfiles(self.win,func=self.tuodong_mp3_file)
        self.win.protocol('WM_DELETE_WINDOW', lambda: _exit(0))
        # self.win.minsize(height=350,width=566)
        self.win.minsize(height=310,width=470)
        self.win.geometry('566x350+500+100') 
        # with open("db/icon2.txt",mode="r") as a:
            # content = a.read()
        content = "AAABAAEAQEAAAAEAIAAoQgAAFgAAACgAAABAAAAAgAAAAAEAIAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAzDgAAMqlAADJ8wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyfMAAMqlAADMOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADOFAAAyqkAAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMqpAADOFAAAAAAAAAAAAAAAAAAAAAAAAAAAAADMJAAAyd8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyd8AAMwkAAAAAAAAAAAAAAAAAADOFAAAyd8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ3wAAzhQAAAAAAAAAAAAAyqsAAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMqrAAAAAAAAzDgAAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAzDgAAMqlAADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/EBDM/w8Py/8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/Dg7L/xERzP8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMqlAADJ8wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wMDyf9qat3/2Nj1//39/v/9/f7/2dn1/2xt3f8DA8n/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wICyf9oaN3/1dX0//39/v/+/v7/3d32/3R03/8GBsn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ8wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wMDyf+rq+r////+////////////////////////////sLDr/wQEyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wMDyf+srOr/////////////////////////////////vb3u/wkJyv8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf9yct3//v7+//////////////////////////////////7+/v9xcd3/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf9ubt3//v7+//////////////////////////////////////+Li+P/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8CAsn/4eH2////////////////////////////////////////////4+P2/wMDyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8DA8n/4uL2////////////////////////////////////////////8vL6/wsLyv8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wQEyf84ONP/OTnS//7+/v////////////////////////////////////////////7+/v8oKM7/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/KCjO//7+/v////////////////////////////////////////////////9MTNb/OjrU/wUFyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AgLJ/2Zl3P/g3/b//////5WV5////////////////////////////////////////////////////v7/NTXR/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/zQ00P///v7/////////////////////////////////////////////////lZXn///////i4ff/YmLb/wEByf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/AADJ/wAAyf8AAMn/EhLM/7y77v/+/v7///////////+Wluf//////////////////////////////////////////////////////zo60v8AAMn/AADJ/wAAyf8AAMr/AADJ/wAAyf8AAMr/AADK/wAAyv8AAMr/AADK/wAAyv8AAMr/AADK/wAAyv8AAMr/AADK/wAAyv86OtL////+/////////////////////////////////////////////////5WV5/////////////7+/v+xsOz/CwvM/wAAyv8AAMr/AADK/wAAyv8AAMr/AADK/wAAyv8AAMr/AADK/wAAyv8AAMr/Dg7M/8/O8v//////////////////////lpbo//////////////////////////////////////////////////////87O9P/AADL/wAAy/8AAMv/AADL/wAAy/8AAMv/AADL/wAAy/8AAMv/AADL/wAAy/8AAMv/AADL/wAAy/8AAMv/AADL/wAAy/8AAMv/OjrT//////////////////////////////////////////////////////+Wluj//////////////////////7m57v8EBMz/AADM/wAAzP8AAMz/AADM/wAAzP8AAMv/AADL/wAAy/8AAMv/AADM/6Cg6P///////////////////////////5aW6P//////////////////////////////////////////////////////OzvU/wAAzP8AAMz/AADM/wAAzP8AAMz/AADM/wAAzP8AAMz/AADM/wAAzP8AAMz/AADM/wAAzP8AAMz/AADM/wAAzP8AAMz/AADM/zo61f//////////////////////////////////////////////////////lpbp///////////////////////+/v7/d3fi/wAAzf8AAM3/AADN/wAAzf8AAM3/AADN/wAAzf8AAM3/AADN/zQ01f/9/f7///////////////////////////+Wlun//////////////////////////////////////////////////////zs71v8AAM7/AADO/wAAzv8AAM7/AADO/wAAzv8AAM7/AADO/wAAzv8AAM7/AADO/wAAzv8AAM7/AADO/wAAzv8AAM7/AADO/wAAzv86Otb//////////////////////////////////////////////////////5aW6f////////////////////////////Lx+/8SEtH/AADP/wAAz/8AAM//AADP/wAAz/8AAM//AADP/wAAz/+amur/////////////////////////////////lpbp//////////////////////////////////////////////////////87O9f/AADP/wAAz/8AAM//AADP/wAAz/8AAM//AADP/wAAz/8AAM//AADQ/wAA0P8AAND/AADQ/wAA0P8AAND/AADQ/wAA0P8AAND/OjrX//////////////////////////////////////////////////////+Wlur/////////////////////////////////aWni/wAA0P8AANH/AADR/wAA0f8AAND/AADQ/wAA0P8AAND/4OD3/////////////////////////////////5aW6v//////////////////////////////////////////////////////OzvY/wAA0f8AANH/AADR/wAA0f8AANH/AADR/wAA0f8AANH/AADR/wAA0f8AANH/AADR/wAA0f8AANL/AADR/wAA0v8AANL/AADS/zo62f//////////////////////////////////////////////////////lpbr/////////////////////////////////62t7/8AANL/AADS/wAA0v8AANP/AADS/wAA0v8AANL/CQnT//7+/v////////////////////////////////+Wluv//////////////////////////////////////////////////////zs72v8AANP/AADT/wAA0/8AANP/AADT/wAA0/8AANP/AADT/wAA0/8AANP/AADT/wAA0/8AANP/AADU/wAA0/8AANT/AADU/wAA1P86Otr//////////////////////////////////////////////////////5aW6//////////////////////////////////S0vb/AADU/wAA1P8AANT/AADV/wAA1P8AANT/AADU/xwc1v/+/v//////////////////////////////////lpbs//////////////////////////////////////////////////////87O9v/AADV/wAA1f8AANX/AADV/wAA1f8AANX/AADV/wAA1f8AANX/AADV/wAA1f8AANX/AADV/wAA1f8AANb/AADW/wAA1v8AANb/Ojrc//////////////////////////////////////////////////////+Wluz/////////////////////////////////5uX4/wAA1v8AANb/AADX/wAA1/8AANb/AADW/wAA1v8JCdf//v7+/////////////////////////////////5aW7f//////////////////////////////////////////////////////Ozvd/wAA1/8AANf/AADX/wAA1/8AANf/AADX/wAA1/8AANj/AADX/wAA2P8AANj/AADY/wAA2P8AANj/AADY/wAA2P8AANj/AADY/zo63f//////////////////////////////////////////////////////lpbt/////////////////////////////////9PT9/8AANn/AADZ/wAA2f8AANn/AADY/wAA2P8AANn/AADZ/+Pj+f////////////////////////////////+Wlu3//////////////////////////////////////////////////////zs73/8AANn/AADZ/wAA2f8AANr/AADa/wAA2f8AANr/AADa/wAA2v8AANr/AADa/wAA2v8AANr/AADa/wAA2v8AANr/AADa/wAA2v86Ot///////////////////////////////////////////////////////5aW7v////////////////////////////////+wsPL/AADb/wAA2/8AANv/AADb/wAA2/8AANv/AADb/wAA2/+Zme7/////////////////////////////////lpbu//////////////////////////////////////////////////////87O+D/AADc/wAA3P8AANz/AADc/wAA3P8AANz/AADc/wAA3P8AANz/AADc/wAA3P8AANz/AADc/wAA3P8AANz/AADc/wAA3P8AANz/Ojrh//////////////////////////////////////////////////////+Wlu//////////////////////////////////aWnp/wAA3f8AAN3/AADd/wAA3f8AAN3/AADd/wAA3f8AAN3/KSnh//r6/f///////////////////////////5aW7///////////////////////////////////////////////////////Ozvi/wAA3v8AAN7/AADe/wAA3v8AAN7/AADe/wAA3v8AAN7/AADe/wAA3v8AAN7/AADe/wAA3v8AAN7/AADf/wAA3/8AAN//AADf/zo64///////////////////////////////////////////////////////lpbw////////////////////////////6en7/w0N4P8AAOD/AADg/wAA4P8AAOD/AADf/wAA3/8AAN//AADf/wAA3/+Qj+7///////////////////////////+WlvD//////////////////////////////////////////////////////zs75P8AAOD/AADg/wAA4P8AAOD/AADg/wAA4f8AAOH/AADh/wAA4f8AAOH/AADh/wAA4f8AAOH/AADh/wAA4f8AAOH/AADh/wAA4f86OuT//////////////////////////////////////////////////////5aW8f/////////////////////////+/2dn6/8AAOL/AADi/wAA4v8AAOL/AADi/wAA4v8AAOL/AADi/wAA4v8AAOL/Cgni/8XF9v//////////////////////lpbx//////////////////////////////////////////////////////87O+b/AADj/wAA4/8AAOP/AADj/wAA4/8AAOP/AADj/wAA4/8AAOP/AADj/wAA4/8AAOP/AADj/wAA4/8AAOP/AADj/wAA4/8AAOP/Ojrm//////////////////////////////////////////////////////+WlvL//////////////////////6+u9P8CAuT/AADk/wAA5P8AAOT/AADk/wAA5P8AAOT/AADk/wAA5P8AAOT/AADk/wAA5P8NDeX/sLD0///+/v///////////5aW8v//////////////////////////////////////////////////////Ojrn/wAA5f8AAOX/AADl/wAA5f8AAOX/AADl/wAA5f8AAOX/AADl/wAA5v8AAOX/AADl/wAA5v8AAOb/AADm/wAA5v8AAOb/AADm/zo66P////7/////////////////////////////////////////////////lZXz/////////////v7+/6Sk9P8ICOf/AADn/wAA5/8AAOf/AADn/wAA5/8AAOf/AADm/wAA5v8AAOf/AADm/wAA5/8AAOf/AADn/25t7v/x8Pr/1NT5//7+/v+VlfP///////////////////////////////////////////////////7+/zQ06f8AAOf/AADn/wAA6P8AAOj/AADo/wAA6P8AAOj/AADo/wAA6P8AAOj/AADo/wAA6P8AAOj/AADo/wAA6P8AAOj/AADo/wAA6P80NOn///7+/////////////////////////////////////////////////5SU9P///v7/2tr5//r6/P9WVu7/AADp/wAA6f8AAOn/AADp/wAA6f8AAOn/AADp/wAA6f8AAOn/AADp/wAA6f8AAOn/AADp/wAA6f++vfn///7+/x4e6f81NOz/NDTr//7+/v////////////////////////////////////////////7+/v8qKur/AADq/wAA6v8AAOr/AADq/wAA6v8AAOr/AADq/wAA6v8AAOr/AADq/wAA6v8AAOr/AADq/wAA6v8AAOr/AADq/wAA6v8AAOr/KSnq//7+/v////////////////////////////////////////////////9HR+7/ODfu/zo57f//////o6P3/wAA6/8AAOv/AADr/wAA6/8AAOv/AADr/wAA7P8AAOv/AADr/wAA6/8AAOv/AADr/wAA6/8AAOv/wsL6//////88PPD/AADs/wIC6//f3/r////////////////////////////////////////////m5vv/BQXs/wAA7P8AAOz/AADs/wAA7P8AAOz/AADs/wAA7P8AAOz/AADs/wAA7P8AAOz/AADt/wAA7f8AAO3/AADt/wAA7f8AAO3/AADt/wQE7P/l5fr////////////////////////////////////////////w8Pz/Cgrt/wAA7f9WVvP//////6en+f8AAO3/AADt/wAA7v8AAO7/AADu/wAA7v8AAO7/AADt/wAA7f8AAO3/AADt/wAA7v8AAO7/AADu/8LC+v//////T07x/wAA7v8AAO7/a2vx//////////////////////////////////////////7/b2/y/wAA7v8AAO7/AADu/wAA7v8AAO7/AADu/wAA7v8AAO//AADv/wAA7/8AAO//AADv/wAA7/8AAO//AADv/wAA7/8AAO//AADv/wAA7/8AAO//a2vz///+/v//////////////////////////////////////g4P0/wAA7/8AAPD/amn0//////+np/n/AADw/wAA8P8AAPD/AADw/wAA8P8AAPD/AADw/wAA8P8AAPD/AADw/wAA8P8AAPD/AADw/wAA8P/Cwvv//////1pa8/8AAPD/AADw/wEB8P+kpPb//v7+//////////////////////////7/paX2/wIC8P8AAPD/AADw/wAA8f8AAPH/AADx/wAA8f8AAPH/AADx/wAA8f8AAPH/AADx/wAA8f8AAPH/AADx/wAA8f8AAPH/AADx/wAA8f8AAPH/AADx/wIC8f+goPb//v7+////////////////////////////trb4/wYG8f8AAPL/AADy/3V19v//////p6f6/wAA8v8AAPL/AADy/wAA8v8AAPL/AADy/wAA8v8AAPL/AADy/wAA8v8AAPL/AADy/wAA8v8AAPL/wsL8//////92dvb/AADy/wAA8v8AAPL/AgLy/2Ji9f/Ozvv//Pz+//39/v/R0fv/ZWX1/wIC8v8AAPP/AADz/wAA8/8AAPP/AADz/wAA8/8AAPP/AADz/wAA8/8AAPP/AADz/wAA8/8AAPP/AADz/wAA8/8AAPP/AADz/wAA8/8AAPP/AADz/wAA8/8AAPP/AQHz/2Fh9v/Nzfv//Pz+//39/v/U1Pv/bGz2/wQE8/8AAPT/AAD0/wAA9P+QkPj//////6en+/8AAPT/AAD0/wAA9P8AAPT/AAD0/wAA9P8AAPT/AAD0/wAA9P8AAPT/AAD0/wAA9P8AAPT/AAD0/8LC/P//////mpr5/wAA9P8AAPT/AAD0/wAA9P8AAPT/AAD0/wEB9P8CAvT/AAD0/wAA9P8AAPX/AAD1/wAA9f8AAPX/AAD1/wAA9f8AAPX/AAD1/wAA9f8AAPX/AAD1/wAA9f8AAPX/AAD1/wAA9f8AAPX/AAD1/wAA9f8AAPX/AAD1/wAA9f8AAPX/AAD1/wAA9f8AAPX/AAD1/wIC9f8CAvX/AAD2/wAA9v8AAPb/AAD2/wAA9v8AAPb/tbT6//////+np/v/AAD2/wAA9v8AAPb/AAD2/wAA9v8AAPb/AAD2/wAA9v8AAPb/AAD2/wAA9v8AAPb/AAD2/wAA9v+0s/v//////9DP+v8AAPb/AAD2/wAA9v8AAPb/AAD2/wAA9v8AAPb/AAD2/wAA9v8AAPb/AAD2/wAA9v8AAPb/AAD3/wAA9/8AAPf/AAD3/wAA9/8AAPf/AAD3/wAA9/8AAPf/AAD3/wAA9/8AAPf/AAD3/wAA9/8AAPf/AAD3/wAA9/8AAPf/AAD3/wAA9/8AAPf/AAD3/wAA9/8AAPf/AAD3/wAA9/8AAPf/AAD3/wAA9/8AAPf/AgL3/+jo/P//////mZn7/wAA+P8AAPj/AAD4/wAA+P8AAPj/AAD4/wAA+P8AAPj/AAD4/wAA+P8AAPj/AAD4/wAA+P8AAPj/mpr7///////7+/7/FBT2/wAA+P8AAPj/AAD4/wAA+P8AAPj/AAD4/wAA+P8AAPj/AAD4/wAA+P8AAPj/AAD4/wAA+P8AAPj/AAD4/wAA+P8AAPj/AAD4/wAA+P8AAPn/AAD5/wAA+f8AAPn/AAD5/wAA+f8AAPn/AAD5/wAA+f8AAPn/AAD5/wAA+f8AAPn/AAD5/wAA+f8AAPn/AAD5/wAA+f8AAPn/AAD5/wAA+f8AAPn/AAD5/ywr+P/+/v7//////39/+/8AAPn/AAD5/wAA+f8AAPn/AAD5/wAA+f8AAPn/AAD5/wAA+f8AAPn/AAD5/wAA+f8AAPn/AAD5/3h3+v///////////1pa+P8AAPr/AAD6/wAA+v8AAPr/AAD6/wAA+v8AAPr/AAD6/wAA+v8AAPr/AAD6/wAA+v8AAPr/AAD6/wAA+v8AAPr/AAD6/wAA+v8AAPr/AAD6/wAA+v8AAPr/AAD6/wAA+v8AAPr/AAD6/wAA+v8AAPr/AAD6/wAA+v8AAPr/AAD7/wAA+/8AAPv/AAD6/wAA+/8AAPv/AAD7/wAA+/8AAPv/AAD7/wAA+/91dPr///////////9dXfr/AAD7/wAA+/8AAPv/AAD7/wAA+/8AAPv/AAD7/wAA+/8AAPv/AAD7/wAA+/8AAPv/AAD7/wAA+/9LS/v///////////+urfr/AAD7/wAA+/8AAPv/AAD7/wAA+/8AAPv/AAD7/wAA+/8AAPv/AAD7/wAA+/8AAPv/AAD7/wAA+/8AAPv/AAD8/wAA/P8AAPz/AAD8/wAA/P8AAPz/AAD8/wAA/P8AAPz/AAD8/wAA/P8AAPz/AAD8/wAA/P8AAPz/AAD8/wAA/P8AAPz/AAD8/wAA/P8AAPz/AAD8/wAA/P8AAPz/AAD8/wAA/P8AAPz/yMf7////////////MTD7/wAA/P8AAPz/AAD8/wAA/P8AAPz/AAD8/wAA/P8AAPz/AAD8/wAA/P8AAPz/AAD8/wAA/P8AAPz/HRz7//7+/v//////+fj9/xkY+v8AAPz/AAD8/wAA/f8AAP3/AAD9/wAA/f8AAP3/AAD9/wAA/f8AAP3/AAD9/wAA/f8AAP3/AAD9/wAA/f8AAP3/AAD9/wAA/f8AAP3/AAD9/wAA/f8AAP3/AAD9/wAA/f8AAP3/AAD9/wAA/f8AAP3/AAD9/wAA/f8AAP3/AAD9/wAA/f8AAP3/AAD9/wAA/f8AAP3/AAD9/wAA/f8AAP3/Li37//7+/v//////9/f9/wkJ/f8AAP7/AAD9/wAA/v8AAP7/AAD+/wAA/v8AAP7/AAD9/wAA/f8AAP3/AAD+/wAA/v8AAP7/AAD+/wEB/f/g3/z///////////+Mi/v/AAD+/wAA/v8AAP7/AAD+/wAA/v8AAP7/AAD+/wAA/v8AAP7/AAD+/wAA/v8AAP7/AAD+/wAA/v8AAP7/AAD+/wAA/v8AAP7/AAD+/wAA/v8AAP7/AAD+/wAA/v8AAP7/AAD+/wAA/v8AAP7/AAD+/wAA/v8AAP7/AAD+/wAA/v8AAP7/AAD+/wAA/v8AAP7/AAD+/wAA/v8AAP7/AAD+/6al+////////////8bG/P8AAP7/AAD+/wAA/v8AAP7/AAD+/wAA/v8AAP7/AAD+/wAA/v8AAP7/AAD+/wAA/v8AAP7/AAD+/wAA/v8AAP7/mZn8////////////8/P9/xgY/f8AAP7/AAD+/wAA/v8AAP7/AAD+/wAA/v8AAP//AAD+/wAA/v8AAP7/AAD+/wAA/v8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//ysq/P/7+/7///////////9/fvz/AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//0VF/P/+/v7///////////+cm/v/AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA/v+2tfv////////////+/v7/Kyv8/wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8DA/7/4uL8/////////////fz+/0NC+/8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//9cW/v//v7+////////////zMv8/wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//3h3+//////////////////m5f3/Hx78/wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8uLvz/8fD9/////////////////15d+/8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8PDv3/6Oj8/////////////////9XV/f8XF/3/AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8kJPz/4+P9/////////////////9fW/P8FBf7/AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//2tq+///////////////////////0dD6/xYV/P8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8iIfv/4N/7///////////////////+/v9QT/v/AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8EA/7/z878///////////////////////V1fz/Hx78/wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8sK/z/4+P9//////////////////////+5uPv/AAD+/wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//zMy/P/39/7//////////////////////+bm/f88PPz/AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA/v9OTfv/7+/9///////////////////////v7v3/ISD8/wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//a2r7//7+/v//////////////////////+fn+/39/+/8HB/7/AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//w0N/f+RkPv//f3+///////////////////////8/P7/U1L7/wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA/v+Qj/v//v7+////////////////////////////3t39/2Jh+/8FBf7/AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//CQn9/29u+//n5v3////////////////////////////+/v7/dnX7/wAA/v8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AQH+/5GQ/P///v7/////////////////////////////////4uH9/3t7/P8dHP3/AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA/v8vLvv/h4f8/+np/f/////////////////////////////////+/v7/eHf8/wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8BAf7/goH6//7+/v///////////////////////////////////////Pz+/8PD/f+BgP3/TEz9/x0d/f8CAv7/AAD//wAA//8AAP//AAD//wIC/v8hIf3/UVH9/4mI/P/T0vv//v7+///////////////////////////////////////8/P7/a2r6/wAA/v8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//9qavv/+vn+////////////////////////////////////////////////////////////9PT8/+jo/v/o6P7/6Oj+/+jo/v/09P3////////////////////////////////////////////////////////////09P3/VVT7/wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//zs6/P/c2/z////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////Pz/z/LCz8/wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//Cgr9/4OC/P/19P3//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////+7u/f90c/z/BQX+/wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA/u0AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//Gxv8/4uK/P/s7P3/////////////////////////////////////////////////////////////////////////////////////////////////5uX9/35+/P8TE/3/AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA/u0AAP6bAAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//CAj+/1RU/f+mpf3/6+r9/////////////////////////////////////////////////////////////////+Xl/f+enf3/S0r9/wUE/v8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP6bAAD8LAAA/v0AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wIC/v8yMf3/Z2b9/5GQ/f+srP7/wMD//8DA///AwP//wMD+/6mp/v+MjP3/Y2L+/yoq/f8BAf7/AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP79AAD8LAAAAAAAAP6ZAAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD+mQAAAAAAAAAAAAD7DAAA/tEAAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD+0QAA+wwAAAAAAAAAAAAAAAAAAPwYAAD+zQAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD+zQAA/BgAAAAAAAAAAAAAAAAAAAAAAAAAAAAA+goAAP6PAAD++QAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP75AAD+jwAA+goAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/CIAAP6JAAD+3QAA/v8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD+/wAA/t0AAP6JAAD8IgAAAAAAAAAAAAAAAAAAAAAAAAAA/AAAAAAAAD/wAAAAAAAAD+AAAAAAAAAHwAAAAAAAAAOAAAAAAAAAAYAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAYAAAAAAAAABwAAAAAAAAAPgAAAAAAAAB/AAAAAAAAAP/AAAAAAAAD8=''"
        tmp = open("tmp.ico", "wb+")
        tmp.write(b64decode(content))
        tmp.close()
        self.win.title('听力播放器')
        self.win.iconbitmap("tmp.ico")
        remove("tmp.ico")
        
        self.win.overrideredirect(True)   
        self.win.update()
        
        self.bg_label = Label(self.win,name="背景",width=600,height=50,bg=self.bg_colour).place(x=0,y=self.win.winfo_height()-75)
        self.change_window_size = Change_Window_Size(self.win,colour=self.col[0],push_colour=self.col[1],bg_colour=self.bg_colour)
        
        self.win_width = self.win.winfo_width() 
        self.win_height = self.win.winfo_height()
        
        self.nt_lt_py_but_x = self.win_width * 0.42
        self.nt_lt_py_but_y = self.win_height - 40
        self.title_bar = Title_Bar(self.win,x=0,y=0,colour=self.col[0],push_colour=self.col[1],width=self.win_width)
        self.button_play_or_pause = Button_Play_Or_Pause(self.win,x=self.nt_lt_py_but_x +38,y=self.nt_lt_py_but_y,colour=self.col[0],push_colour=self.col[1],bg_colour=self.bg_colour)
        self.button_next_stence = Button_Next_Stence(self.win,x=self.nt_lt_py_but_x +88,y=self.nt_lt_py_but_y,colour=self.col[0],push_colour=self.col[1],bg_colour=self.bg_colour)
        self.button_last_stence = Button_Last_Stence(self.win,x=self.nt_lt_py_but_x ,y=self.nt_lt_py_but_y,colour=self.col[0],push_colour=self.col[1],bg_colour=self.bg_colour)
        self.jin_du_tiao = Jin_Du_Tiao(self.win,x=self.win_width * 0.1,y=self.win_height-56,colour=self.col[0],push_colour=self.col[1],width=self.win_width*0.8,bg_colour=self.bg_colour)
        self.music_title = Music_Title(self.win,x=self.win_width * 0.1,y=self.win_height-58,colour=self.col[0],push_colour=self.col[1],bg_colour=self.bg_colour)
        self.yin_liang_tiao = Yin_Liang_tiao(self.win,x=self.win_width * 0.1 + self.win_width*0.8 -40,y=self.win_height-65+30,colour=self.col[0],push_colour=self.col[1],bg_colour=self.bg_colour)
        self.repeat_stence_btn = Repeat_Stence_Btn(self.win,x=self.nt_lt_py_but_x+130,y=self.nt_lt_py_but_y,colour=self.col[0],push_colour=self.col[1],bg_colour=self.bg_colour)
        self.display_ge_ci = Display_Ge_Ci(self.win,x=self.nt_lt_py_but_x - 48,y=self.nt_lt_py_but_y,colour=self.col[0],push_colour=self.col[1],bg_colour=self.bg_colour)
        self.translate_but = Translate_But(self.win,x=self.nt_lt_py_but_x - 92,y=self.nt_lt_py_but_y,colour=self.col[0],push_colour=self.col[1],bg_colour=self.bg_colour)
        self.record_but = Record_But(self.win,x=self.nt_lt_py_but_x - 140,y=self.nt_lt_py_but_y,colour=self.col[0],push_colour=self.col[1],bg_colour=self.bg_colour)
        self.button_beisu = Button_beisu(self.win,x=self.nt_lt_py_but_x -140 -48-15,y=self.nt_lt_py_but_y,colour=self.col[0],push_colour=self.col[1],bg_colour=self.bg_colour)
        self.tool_bar = Tool_Bar(self.win,x=0,y=24,colour=self.col[0],push_colour=self.col[1],height=self.win_height,bg_colour=self.bg_colour)
        self.display_area_frame = Display_Area_Frame(self.win,x=90,y=24,width=self.win_width,height=self.win_height,colour=self.col[0],push_colour=self.col[1])
        
 
    def mainloop(self):
        self.win.after(10, lambda: self.set_appwindow(self.win))
        self.win.mainloop() 
        
    def set_appwindow(self,root):
        bit = calcsize("P") * 8
        hwnd = windll.user32.GetParent(root.winfo_id())
        if bit == 64:
            style = windll.user32.GetWindowLongPtrW(hwnd, -20)
            style = style & ~0x00000080
            style = style | 0x00040000
            res = windll.user32.SetWindowLongPtrW(hwnd, -20, style)
        else:
            style = windll.user32.GetWindowLongW(hwnd, -20)
            style = style & ~0x00000080
            style = style | 0x00040000
            res = windll.user32.SetWindowLongW(hwnd, -20, style)  
        root.wm_withdraw()
        root.after(10, lambda: root.wm_deiconify())
    
    def creat_new_directory(self):
        def creat_logo():
            with open("db/logo.gif",mode="wb") as wb:
                wb.write(b'GIF89a\x16\x00\x16\x00\xd5\x00\x00\x00\x00\x00\xff\xff\xff\xff\xfe\xff\xfd\xfe\xff\xfa\xfd\xff\xf1\xfa\xff\xf7\xfc\xff\xef\xf9\xfe\xf5\xfb\xfe\xf9\xfd\xff\xfc\xfe\xff\xee\xf9\xfe\xf1\xfa\xfe\xd7\xf2\xfd\xea\xf8\xfe\xf5\xfc\xff\xd1\xf0\xfc\xe3\xf6\xfd\xe8\xf8\xfe\xeb\xf8\xfd\xef\xfa\xfe\xf3\xfb\xfe\xee\xfa\xfe\xf2\xfb\xfe\xf6\xfc\xfe\xfb\xfe\xff\xeb\xf9\xfd\xf1\xfb\xfe\xf4\xfc\xfe\xec\xfa\xfd\xf1\xfb\xfd\xf2\xfb\xfd\xf8\xfd\xfe\xf5\xfd\xfe\xf4\xfc\xfd\xee\xfb\xfc\xe7\xfa\xfb\xe4\xf9\xfa\xe7\xfb\xfb\xea\xfb\xfb\xef\xfc\xfc\xf2\xfd\xfd\xf6\xfd\xfd\xf9\xfe\xfe\xf8\xfd\xfd\xfa\xfe\xfe\xf9\xfd\xfd\xfb\xfe\xfe\xfd\xff\xff\xfe\xff\xff\xfd\xfe\xfe\xed\xfc\xfb\xf1\xfd\xfc\xf2\xfd\xfc\xf6\xfe\xfd\xf7\xfe\xfd\xfd\xff\xfe\xff\xff\xfe\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00!\xf9\x04\x01\x00\x00:\x00,\x00\x00\x00\x00\x16\x00\x16\x00\x00\x06\x94@\x9dpH,\x1a\x8f\xc8\xe4\xb1\x12\x0b\x0c8\xca"&\x90I\xc4\x08\x89\x00(\xaa\x0b\x186\xc5\xc5#\xa0\xcc\\\x92\x94\x01\xd2!\x89F(G\x04WW1N\x1as\x88\xa5\xc8\x98\x0b\x0fE\x05~:\x80F4\x01)G(\x017:\x1fE\x1a60\x01/G/\x01\x01*\x1dE\n8\x93-G+\x0112\nD,\x94\x9f\xa1\xa3\x97.C\x02\xa9\x01\xa0F\xa21\x97dB#\xb1\xb3E\xb5\x97\x1eD"\xa3\xb2\xab19!F%2\xc4\xb4\x98$H3\x01\'G&\x015\x83\xd8\xd9:A\x00;')
        if not isdir("db"): mkdir("db")
        for file in ["colour.txt","directory.txt","geci_colour.txt","img_path.txt","music_init.txt","sentence_rcord.txt","logo.gif"]:
            if not isfile("db"+"/"+file):
                if file == "logo.gif": 
                    creat_logo()
                    continue
                with open("db/"+file,mode="w",encoding="utf-8") as a:
                    pass
                
                
    def record_current_data(self):
        music_path = player.file_directory + "/" + player.current_music_name
        music_time = player.player.position() / 1000
        music_volume = player.player.volume()
        music_data = {"歌曲路径":music_path,"歌曲时间":music_time,"音量":music_volume}
        with open("db/music_init.txt",mode="w",encoding="utf-8") as w:
            w.write(dumps(music_data))
            
    def music_init_(self):
        with open("db/music_init.txt",mode="r",encoding="utf-8") as r:
            music_data = r.read()
            if music_data: music_data = loads(music_data)
            else: return
        if not isfile(music_data["歌曲路径"]): return
        filename = music_data["歌曲路径"].split("/")[-1]
        player.current_music_name = filename
        try:
            audio = MP3(music_data["歌曲路径"])
        except Exception:
            with open("db/music_init.txt",mode="w") as w:
                w.write("")
            return
        mp3_length = audio.info.length
        player.current_music_length = mp3_length
        player.set_music(music_data["歌曲路径"])
        main_ui.music_title.mus_title["text"] = filename
        main_ui.jin_du_tiao.full_time["text"] = lib.sec_convert_formatsec(player.current_music_length)
        player.set_position(music_data["歌曲时间"] * 1000)
        self.button_play_or_pause.play_or_pause_left(1)
        player.set_yingliang(music_data["音量"])
        
    def tuodong_mp3_file(self,files_path):
        player.drop_file = ""
        player.drop_imgfile = ""
        for file_path in files_path:
            print(1)
            file_path = file_path.decode("GBK")
            if file_path[-3:].upper() == "MP3":
                player.drop_file = file_path
                return
            elif file_path[-3:].upper() == "PNG" or file_path[-3:].upper() == "JPG":    
                player.drop_imgfile = file_path
                return
            elif isdir(file_path):
                for f in listdir(file_path):
                    if f[-3:].upper() == "MP3":
                        player.drop_file = file_path + "\\" + f
                        return
            
    def play_dropfile(self,file_audio_path):
        # print(file_audio_path)
        if not isfile(file_audio_path):return
        file_audio_path = file_audio_path.replace("\\","/").strip()
        directory_and_filename = split(file_audio_path)
        player.current_music_name = directory_and_filename[1]
        player.file_directory = directory_and_filename[0]
        

        main_ui.display_area_frame.local_audio_canvas.open_file(directory_and_filename[0])
        
        audio = MP3(file_audio_path)
        player.current_music_length = audio.info.length
        main_ui.music_title.mus_title["text"] = player.current_music_name
        main_ui.jin_du_tiao.full_time["text"] = lib.sec_convert_formatsec(player.current_music_length)
        if main_ui.button_beisu.current_state == "有倍速":
            main_ui.button_beisu.time_ = 0
            
        player.drop_file = ""
        if "循环中" == main_ui.repeat_stence_btn.current_state:
            main_ui.repeat_stence_btn.push_but(0)
        if main_ui.button_play_or_pause.current_state == "播放":
            main_ui.button_play_or_pause.play_or_pause_left(1)
        player.set_music(file_audio_path)
        main_ui.tool_bar.check_local_audio()
        if main_ui.tool_bar.but["本地音频"].tool_bar_but.itemcget(main_ui.tool_bar.but["本地音频"].line,"state") == "hidden":
            main_ui.tool_bar.but["本地音频"].tool_bar_but.itemconfig(main_ui.tool_bar.but["本地音频"].line,state="normal")
            main_ui.tool_bar.but["本地音频"].tool_bar_but["bg"] = "white" 
            for i,j in main_ui.tool_bar.but.items():
                if i == main_ui.tool_bar.but["本地音频"].name:continue
                j.tool_bar_but.itemconfig(j.line,state="hidden")
                
        main_ui.display_area_frame.local_audio_canvas.cv.move(main_ui.display_area_frame.local_audio_canvas.laba_1,0,-1000)
        main_ui.display_area_frame.local_audio_canvas.cv.move(main_ui.display_area_frame.local_audio_canvas.laba_2,0,-1000)
        main_ui.display_area_frame.local_audio_canvas.cv.move(main_ui.display_area_frame.local_audio_canvas.laba_3,0,-1000)
        main_ui.display_area_frame.local_audio_canvas.cv.move(main_ui.display_area_frame.local_audio_canvas.laba_4,0,-1000)
        
if __name__ == "__main__":
    player = Media_Player()
    main_ui = Main_UI()
    geci_obj = GeCi()
    main_ui.music_init_()
    if argv[-1][-3:].upper() == "MP3": main_ui.play_dropfile(argv[-1])
    main_ui.mainloop()

