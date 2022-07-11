from bs4 import BeautifulSoup
from time import time
from random import randint
from hashlib import md5
from requests import post,get,exceptions
from requests.exceptions import ConnectionError
def translate_word(word):
    r = get(url='http://dict.youdao.com/w/%s/#keyfrom=dict2.top'%word)
    soup = BeautifulSoup(r.text, "lxml")
    try:
        s = soup.find(class_='trans-container')('ul')[0]('li')
    except Exception:return False
    result = ''
    for item in s:
        if item.text:
            result = result + item.text + "\n"
    if result:return result
    else: return False
def translate_sentence_1(content):
    url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
    data = {}
    data['i']=content
    data['from']='AUTO'
    data['to']='AUTO'
    data['smartresult']='dict'
    data['client']='fanyideskweb'
    data['salt']='1538295833420'
    data['sign']='07'
    data['doctype']='json'
    data['version']='2.1'
    data['keyfrom']='fanyi.web'
    data['action']='FY_BY_REALTIME'
    data['typoResult']='false'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    result = post(url,data,headers=headers)
    trans = result.json()
    tran = trans['translateResult'][0][0]['tgt']
    return tran   
def translate_sentence_2(content):
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "244",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "_ntes_nnid=42c08d6f4cb81c19661cb96d9e68ce77,1568450884973; OUTFOX_SEARCH_USER_ID_NCOO=1931914122.7583647; OUTFOX_SEARCH_USER_ID=-2023454251@121.239.41.15; JSESSIONID=aaaUdV_9lZ0BfcV1Vqfqx; ___rl__test__cookies=1597816439567",
        "Host": "fanyi.youdao.com",
        "Origin": "http://fanyi.youdao.com",
        "Pragma": "no-cache",
        "Referer": "http://fanyi.youdao.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    appVersion = "5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
    url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
    t = md5(appVersion.encode()).hexdigest()
    r = str(int(time()*1000))
    i = r + str(randint(0,9))
    data = {
        "i": content,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": i,
        "sign": md5(("fanyideskweb" + content + i + "]BjuETDhU)zqSxf-=B#7m").encode()).hexdigest(),
        "lts": r,
        "bv":t,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_REALTlME"
    }
    try:
        results = post(url,headers=headers,data=data).json()['translateResult'][0][0]['tgt']
    except ConnectionError:
        results = "网络连接异常!!!"
    return results
def main_translate_sentence(content):
    if content:
        try:result = translate_word(content)
        except Exception:result = translate_sentence_2(content)
        except Exception:result = translate_sentence_1(content)
        if result == False:
            try:result = translate_sentence_2(content)
            except Exception:result = translate_sentence_1(content)
        return result.strip()


if __name__ == "__main__":
    res = main_translate_sentence("剣を握らなければ おまえを守らない 剣を握ったままでは おまえを抱きしめられない ")
    print(res)
    print()
    res = main_translate_sentence("i love you")
    print(res)
    print()
    res = main_translate_sentence("China")
    print(res)
    print()
    res = main_translate_sentence("A friendship founded on business is better than business founded on friendship.")
    print(res)
    print()
    res = main_translate_sentence("牛津词典")
    print(res)
    print()
    res = main_translate_sentence("acclaim")
    print(res)
    print()
    res = main_translate_sentence("ammunition")
    print(res)
    print()
    res = main_translate_sentence("Another study also found eating a high-fat and high-sugar breakfast each day for as little as four days resulted in problems with learning and memory similar to those observed in overweight and obese individuals.")
    print(res)
    print()
    res = main_translate_sentence(" Now a new study has provided another contribution to the debate, uncovering strong evidence that adolescent wellbeing in the United States really is experiencing a decline and arguing that the most likely cause is the electronic riches we have given them.")
    print(res)
    print()
    res = main_translate_sentence("数据稍微复杂了一点儿，因为现实中喜欢社交的孩子们也倾向于进行更多的在线交流，但把不同的例子放在一起就可以清楚地看到，现实世界社交能力与更高的幸福感相关，而在屏幕上或网络上花更多的时间只与更差的幸福指数相关。")
    print(res)
    print()























