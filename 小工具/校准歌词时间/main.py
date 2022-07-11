from chardet import detect
from re import findall
def sec_convert_formatsec(sec): # '''秒转分，例：65.66 >>> 01:05:66'''
    ms = str(sec).split(".")[-1]
    if len(ms) < 2: ms = ms + "0"
    sec = int(str(int(sec * 100))) // 100
    fen = str(sec // 60)
    if len(fen) < 2 :fen = '0' + fen
    miao = str(round(float('0' + '.' + str(sec/60).split('.')[1]) * 60))
    if len(miao) < 2 :
        miao = '0' + miao
    # print(sec)
    return fen + ':'  + miao + "." + ms
def min_to_sec(fen_zhong):  # '''分转秒， 例：01:05:66 >>> 65.66'''
    if fen_zhong[0:2].isdigit() and fen_zhong[3:5].isdigit() and fen_zhong[6:8].isdigit():
        miao = float((int(fen_zhong[0:2]) * 60 ) + int(fen_zhong[3:5]) + float('0'+ '.' +fen_zhong[6:8]))
    else : 
        return False
    return miao 
def open_krc_lrc_file(file_name):
    with open(file=file_name,mode='rb') as obj:# 以二进制模式读取文件
        for line in obj.readlines():
            try:
                line = line.decode(encoding='gb18030')
            except UnicodeDecodeError:
                result = detect(line) # 检测文件内容
                line = line.decode(encoding=result["encoding"])
            a = "".join(findall("\[(.*?)\]",line))
            time = min_to_sec(a)
            # print(time,"".join(findall("\[.*?\](.*)",line)).strip())
            if not time or len(a) != 8 :continue
            # print(time,"".join(findall("\[.*?\](.*)",line)).strip())
            yield (time,"".join(findall("\[.*?\](.*)",line)).strip())
if __name__ == "__main__":
    file_path = "tomorrow will be better.lrc"
    g = open_krc_lrc_file(file_path)
    start_delay_time = -0.4
    # end_delay_time = 0
    time_list = []
    format_time_list = []
    geci_list = []
    for i in g:
        # print(i,1)
        t = i[0] + start_delay_time
        if t < 0: t = 0
        time_list.append(round(t,2))
        geci_list.append(i[1])
    fp = open(file_path.split("/")[-1][0:-3]+"txt",mode="w")#encoding="utf-8"
    for i,j in zip(time_list,geci_list):
        
        mus_t = "[" + sec_convert_formatsec(i) + "]"
        print(mus_t + j + "\n")
        fp.write(mus_t + j + "\n")
    fp.close()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    