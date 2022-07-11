from json import loads,dumps
from os import listdir
from tkinter import Tk,Button,Label,Listbox
from tkinter.filedialog import askdirectory,askopenfilename
from chardet import detect
class Application:
    def __init__(self):
        self.make_app()
        self.directory_name = ""
        self.file_name = ""
    def make_app(self):
        self.app = Tk()
        self.app.title('修改“我的记录”中句子的播放路径')
        self.app.geometry('380x420+500+100') 
        self.label = Label(self.app,
            name = 'up_wenzi',
            text = '''由于歌曲的路径的改变会导致“我的记录”中句子的播放路径失效，选择新的“我的记录”中句子的音频所在目录，即可修复“我的记录”的页面打不开句子的问题。\n
修复步骤：
1.点击“打开歌词文件”按钮，打开听力播放器所在的目录中，之后选择“db”文件夹中的   “sentence_rcord.txt”文件。\n      
2.点击“打开音频所在目录”按钮，打开音频所在的目录。
3.点击“修复”按钮，完成修复。
            ''',
            anchor = 'center',
            font = ["楷体",12],
            wraplength = 350,
        ).pack(side="top",fill="both")

        self.label1 = Label(text="音频所在目录:",name="label1",anchor="w").pack(fill="x",side="top",anchor="center")
        self.label2 = Label(text="歌词文件:",name="label2",anchor="w").pack(fill="x",side="top",anchor="center")

        self.button_0 = Button(self.app,height=2,width=15,text='修复',command=self.but_xiufu)
        self.button_0.pack(side="bottom",fill="x")

        self.button_2 = Button(self.app,height=2,width=15,text='打开歌词文件',command=self.open_file)
        self.button_2.pack(side="bottom",fill="x")

        self.button_1 = Button(self.app,height=2,width=15,text='打开音频所在目录',command=self.open_directory)
        self.button_1.pack(side="bottom",fill="x")
        
    def mainloop(self):
        self.app.mainloop()    

    def open_directory(self):
        directory_name = askdirectory()
        if not directory_name: return
        self.app.children["label1"]["text"] = "音频所在目录: " + directory_name
        self.directory_name = directory_name

    def open_file(self):
        file_name = askopenfilename()
        if not file_name: return
        self.file_name = file_name
        self.app.children["label2"]["text"] = "歌词文件: " + file_name
    
    def but_xiufu(self):
        if (not self.directory_name) or (not self.file_name): return
        self.xiufu(self.file_name,self.directory_name)
    def xiufu(self,file_name,new_audio_directory):
        with open(file_name,mode="r",encoding="utf-8") as r:
            sentence_record_list = []
            for line in r:
                sentence_record_list.append(loads(line))
        index_ = 0
        for line in sentence_record_list:
            for item in line.values():
                audio_name = item["file_audio_path"].split("/")[-1]
                for new_auido_name in listdir(new_audio_directory):
                    if new_auido_name == audio_name:
                        item["file_audio_path"] = new_audio_directory  + "/" + new_auido_name

        with open(file_name,mode="w",encoding="utf-8") as w:
            for i in sentence_record_list:
                w.write(dumps(i) + "\n")
app = Application()
app.mainloop()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
  
    
    
    
    
    
    
    
    
    
    
    
    