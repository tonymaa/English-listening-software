from tkinter import Tk,Button,Label,Listbox
from tkinter.filedialog import *
from chardet import detect
class Application:
    def __init__(self):
        self.make_app()
        self.all_file_list = []
    def make_app(self):
        self.app = Tk()
        self.app.title('合并歌词断句 v0.1')
        self.app.geometry('360x320+500+100') 
        self.button_convert = Button(self.app,height=2,width=15,name='button_convert',text='全部转换',command=self.all_hebing)
        self.button_convert.pack(side="bottom",fill="both")
        self.button_open_file = Button(self.app,height=2,width=15,name='button_open_file',text='打开文件',command=self.open_file)
        self.button_open_file.pack(side="bottom",fill="both")
        self.label = Label(self.app,
            name = 'up_wenzi',
            text = '打开文件选择需要转换的文件（lrc/txt格式文件）',
            anchor = 'center',
            font = ["楷体",12],
            wraplength = 200,
        ).pack(side="top",fill="both")
        self.lb = Listbox(self.app,width="50")
    def mainloop(self):
        self.app.mainloop()    
    def open_file(self):
        file_name = askopenfilenames()
        if not file_name: return
        self.lb.pack(expand=True,fill="both")
        self.lb.delete(0,"end")
        for i in file_name:
            if i[-3:].upper() == "TXT" or i[-3:].upper() == "LRC":
                self.all_file_list.append(i)
                self.lb.insert("end",i.split("/")[-1])
    def all_hebing(self):
        if not self.all_file_list: return
        for i in range(len(self.all_file_list)):
            self.he_bing(self.all_file_list[i])
            self.lb.delete(i)
            self.lb.insert(i,"(转换完成)"+self.all_file_list[i].split("/")[-1])
        self.all_file_list = []    
            
    def he_bing(self,file_path):
        save_path = file_path
        save_name = save_path.split("/")[-1]

        with open(file_path,mode="rb") as code:
            result = detect(code.read())
            encoding_result = result["encoding"]
        # print(encoding_result)
        with open (file_path,mode='r',encoding=encoding_result) as geci_object:
            geci = geci_object.read()
        with open (file_path,mode='w',encoding=encoding_result) as ob:
            ob.write('')
        geci_list = geci.split('\n')
        list_shan = []
        for i in geci_list:
            ju_last_three = i[len(i)-3:]
            if '.' in ju_last_three or '?' in ju_last_three :
                list_shan.append(i)
        for i in list_shan:
            geci = geci.replace(i,'{}################'.format(i))
        org_ju_zi = geci.split('################')
        kai_tou = []
        zi_ju = []
        kai_tou_new = []
        for i in org_ju_zi:
            zi_ju_old = i.split('\n')
            zi_ju.append(zi_ju_old)
        for i in range(len(zi_ju)-1):
            for j in range(len(zi_ju[i])-1):
                if len(zi_ju[i][j]) < 5:
                    del zi_ju[i][j]
        ssss = open (save_path,mode='a+',encoding=encoding_result)  
        ssss.truncate(0)   
        for dan in zi_ju:
            dan_tou_new = dan[0]
            wei_con = ''
            for wei in range(1,len(dan)):
                wei_con = wei_con +' ' + dan[wei][10:]
            new_content = dan_tou_new + ' ' + wei_con 
            if len(new_content) > 5 :  
                ssss.write('{}\n'.format(new_content))
        ssss.close()
        with open(save_path,mode='r+',encoding=encoding_result) as ssss:  
            content = ssss.read().strip()
            ssss.truncate(0)
            ssss.seek(0)
            ssss.write(content)
app = Application()
app.mainloop()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
  
    
    
    
    
    
    
    
    
    
    
    
    