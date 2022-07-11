from chardet import detect
from re import findall
def sec_convert_formatsec(sec): # '''秒转分，例：65.66 >>> 01:05:66'''
    # print(sec)
    sec = int(str(int(sec * 100))) // 100
    fen = str(sec // 60)
    if len(fen) < 2 :fen = '0' + fen
    miao = str(round(float('0' + '.' + str(sec/60).split('.')[1]) * 60))
    if len(miao) < 2 :
        miao = '0' + miao
    return fen + ':'  + miao
    
def min_to_sec(fen_zhong):  # '''分转秒， 例：01:05:66 >>> 65.66'''
    if fen_zhong[0:2].isdigit() and fen_zhong[3:5].isdigit() and fen_zhong[6:8].isdigit():
        # print(fen_zhong[0:2],fen_zhong[3:5],fen_zhong[6:8])
        miao = float((int(fen_zhong[0:2]) * 60 ) + int(fen_zhong[3:5]) + float('0'+ '.' +fen_zhong[6:8]))
    else : 
        return False
    # print(miao)
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
            # print(len(a))
            if not time or len(a) != 8 :continue
            # print(time)
            yield (time,"".join(findall("\[.*?\](.*)",line)).strip(),a[:-3])

def change_geci_time_format(file_path): # [00:00.000] >>> [00:00:00]
    with open(file=file_path,mode='rb') as obj:# 以二进制模式读取文件
        content = obj.read()
        try:
            content = content.decode(encoding='gb18030')
        except UnicodeDecodeError:
            result = detect(content) # 检测文件内容
            content = content.decode(encoding=result["encoding"])
        # print(content)
        length = len((findall("\[(.*?)\]",content))[0])
        if length == 9:
            file_path = file_path
            line_list = ["[00:00.00]-"]
            for line in content.splitlines():
                line_list.append(line[0:9] + line[10:])
                # print(line)
            # print(line_list)
            with open(file_path,mode="w",encoding="utf-8") as w:
                for line in line_list:
                    w.write(line+"\n")
        
if __name__ == "__main__":
    # a = open_krc_lrc_file("2017年12月四级真题（二）.txt")
    # a = open_krc_lrc_file("北京东路的日子-汪源、刘千楚、徐逸昊、鲁天舒、姜玮珉、胡梦原、张鎏依、梁竞元、游彧涵、金书援、许一璇、张夙西.lrc")
    # for i in a: 
        # i
        # print(i)
    # change_geci_time_format("北京东路的日子-汪源、刘千楚、徐逸昊、鲁天舒、姜玮珉、胡梦原、张鎏依、梁竞元、游彧涵、金书援、许一璇、张夙西.lrc")
    change_geci_time_format("2017年12月四级真题（二）.txt")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    