# _*_ coding:utf-8 _*_

# 多个文件打开
def openall(mod, *files):
    mapper={}
    for fil in files:
        mapper[fil] = open(fil, mod)
    return mapper

# 刷新多个文件
def flushall(files):
    for key, value in files.items():
        value.flush()

# 关闭多个文件
def closeall(files):
    for key, value in files.items():
        value.close()

# 重试方法封装器
def retryWrapper(method, times):
    def retryMethod(*args, **kwargs):
        nonlocal times
        while(times):
            times-=1
            try:
                return method(*args, **kwargs)
            except Exception as e:
                if(times==0):   raise Exception("【异常】\"{0}\".若无法解决请手动查询该文献，或是和本人联系:asirlu@foxmail.com".format(str(e))) # 不可重试，抛出异常
        
    return retryMethod

# 论文标题迭代器,根据路径是目录或是文件才去不同的迭代方式
def paperTitleItera(path):
    import os
    import sys
    if(os.path.isfile(path)):
        papersFile = open(path, "rb")
        for titleBytes in papersFile:             # 遍历文件
            title = titleBytes.decode("utf8").strip()
            if(len(title)==0):   continue
            yield title
        papersFile.close()
        return
    else:
        for fileName in os.listdir(path):    # 遍历文件夹
            if(os.path.isdir(path+"/"+fileName)):continue
            (title, suffix) = os.path.splitext(fileName)    # 除去后缀
            title = title.strip()
            if(len(title)==0):   continue
            yield title
        return

def log(output):
    logfile = open("log", "ab")
    logfile.write((output+"\n").encode("utf8"))
    logfile.flush()
    logfile.close()