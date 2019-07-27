from urllib import request
from urllib import parse
from aip import AipOcr
import  requests
import urllib
import time
import re


def main():

    # 构造初始请求头
    startHeader = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
    }
    header = {}
    while True:
        id, vCode = getVCodeImage(startHeader)
        cookie = '_ga=GA1.3.1307490623.1545140218; username=**********; JSESSIONID=' + id + '; Hm_lvt_87cf2c3472ff749fe7d2282b7106e8f1=1563357606,1563888272,1564029947,1564112702; Hm_lpvt_87cf2c3472ff749fe7d2282b7106e8f1=1564112721'
        header = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Cookie": cookie,
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Origin": "http://jwc.swjtu.edu.cn",
            "Referer": "http://jwc.swjtu.edu.cn/service/login.html",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
        }
        res = login(header, vCode)
        if '登录成功' in str(res):
            print(res)
            break
    jump(header)
    getUserWindow(header)



# 取得验证码 并且写入本地 然后返回该请求的cookie信息（JSESSIONID）
def getVCodeImage(startHeader):

    vCodeUrl = 'http://jwc.swjtu.edu.cn/vatuu/GetRandomNumberToJPEG'
    while True:
        req = requests.get(vCodeUrl, headers=startHeader)
        vCodeImage = req.content
        with open(r'vCodeImage.jpg', 'wb') as f:
            f.write(vCodeImage)

        # 验证码识别模块 此处调用百度AI中通用文字识别接口 可在百度AI官网免费申请
        AppID = "****"
        API_Key = "****"
        Secret_Key = "*****"
        client = AipOcr(AppID, API_Key, Secret_Key)
        with open(r'vCodeImage.jpg', 'rb') as f2:
            image = f2.read()

        result = str(client.basicGeneral(image)).replace(" ","")
        # 利用正则表达式提取识别结果中验证码部分
        pat = re.compile(r"{'words':'(.*?)'}")
        vCodeList = pat.findall(result)
        if len(vCodeList)>0:
            if len(vCodeList[0])==4:
                break

        # 延迟0.5秒后再获取新的验证码
        time.sleep(0.5)

    # 提取JSESSIONID 用于构造以后的请求头
    coo = str(req.cookies)
    # 利用正则表达式解析出 JSESSIONID
    pat = re.compile('JSESSIONID=(.*?) for')
    id = pat.findall(coo)[0]
    print(id)
    return id,vCodeList[0]



# 模拟登录
def login(header, vCode):

    from_data = {
        "username": "**********",
        "password": "**********",
        "url": "http://jwc.swjtu.edu.cn/index.html",
        "returnUrl": "",
        "area": "",
        "ranstring": vCode
    }
    data = urllib.parse.urlencode(from_data).encode(encoding = "UTF-8")
    loginUrl = r'http://jwc.swjtu.edu.cn/vatuu/UserLoginAction'
    req = request.Request(loginUrl, headers=header, data=data)
    res = request.urlopen(req).read().decode()
    return res

# 模拟登录后跳转
def jump(header):

    loadingUrl = 'http://jwc.swjtu.edu.cn/vatuu/UserLoadingAction'
    req = request.Request(loadingUrl, headers = header)
    res = request.urlopen(req).read().decode()
    print(res)

# 取得登录后的用户界面
def getUserWindow(header):

    userUrl = 'http://jwc.swjtu.edu.cn/vatuu/UserFramework'
    req = request.Request(userUrl, headers = header)
    res = request.urlopen(req).read().decode()
    print(res)

if __name__ == '__main__':
    main()