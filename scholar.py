#-*-coding:utf-8-*-

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import json
import re
import services
			

def searchRef(paperName, debug=False):
    jsonBytes = searchRefJson(paperName, debug)
    if(debug): print('parser json')
    try:
        jsonObject = json.loads(jsonBytes.decode('gb2312'))
        if(debug): print('regualr')
        mapper={'APA':None, 'MLA':None, 'GBT7714':None}
        mapper['APA'] = re.sub('#i{|}', '', jsonObject['sc_APA'])
        mapper['GBT7714'] = re.sub('#i{|}', '', jsonObject['sc_GBT7714'])
        mapper['MLA'] = re.sub('#i{|}', '', jsonObject['sc_MLA'])
    except Exception as e:
        services.log("【异常】Json解析错误:"+str(jsonObject))
        #raise e
    if(debug): print('--------------')
    return mapper

def searchRefJson(paperName, debug=False):
    if(debug): print("request paper html")
    page = pageBytes(paperName)
    if(debug): print("parser html")
    soup = BeautifulSoup(page, "html.parser")
    tags = soup.find_all(class_='sc_q')
    if(debug): print("request reference type json")
    refs = refBytes(tags[0]['data-link'], tags[0]['data-sign'])
    return refs

def pageBytes(paperName):
    params = urllib.parse.urlencode({
        "wd" : paperName,                           # 论文名称
        "tn" : "SE_baiduxueshu_c1gjeupa",           # 百度学术搜索
        "ie" : "utf-8"})                            # 编码格式
    url = "http://xueshu.baidu.com/s?{0}".format(params)    # GET参数拼接
    response = urllib.request.urlopen(url, timeout=2).read()           # 读取二进制字节
    return response
    
def refBytes(link, sign):
    params = urllib.parse.urlencode({
        "sign" : sign,
        "url"  : link,
        "t"    : "cite"})                            
    url = "http://xueshu.baidu.com/u/citation?{0}".format(params)   # GET参数拼接
    response = urllib.request.urlopen(url, timeout=2).read()                   # 读取二进制字节
    return response