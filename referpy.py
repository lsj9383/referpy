# _*_ coding:utf-8 _*_
import sys
import scholar
import os
import time
import services

def main():
    debug = False
    if(len(sys.argv) == 1):
        raise Exception("【异常】 没有输入期望检索的目录和文件")
    if(len(sys.argv)==3 and (sys.argv[2]=="-debug" or sys.argv[2]=="-d" or \
                            sys.argv[2]=="-DEBUG" or sys.argv[2]=="-D")):
        debug = True

    # 快速查询模式
    if(sys.argv[1].startswith("paper:")):
        try:
            title = sys.argv[1][6:]
            print("search \"{0}\"".format(title))
            mapper = services.retryWrapper(scholar.searchRef, 3)(title, debug)  # 重试3次
        except Exception as e:  raise e
        else:
            print("【APA】："+mapper["APA"])
            print("【GBT7714A】："+mapper["GBT7714"])
            print("【MLA】："+mapper["MLA"])
            return
    
    # 目录/文件查询模式
    if ((not os.path.isfile(sys.argv[1])) and (not os.path.isdir(sys.argv[1]))):
        raise Exception("【异常】 没有找到该目录或文件：\"{0}\"".format(sys.argv[1]))
    lineNumber = 0
    haveExceptionNote=False
    files = services.openall("wb", "apa.txt", "gbt7714.txt", "mla.txt")
    for title in services.paperTitleItera(sys.argv[1]):
        lineNumber += 1
        print("search \"{0}\"".format(title))
        try:
            mapper = services.retryWrapper(scholar.searchRef, 3)(title, debug)  # 重试3次
        except Exception as e:       # 出现异常，将错误进行记录
            files["apa.txt"].write("[{0}] {1} \n".format(lineNumber, str(e)).encode("utf8"))
            files["gbt7714.txt"].write("[{0}] {1} \n".format(lineNumber, str(e)).encode("utf8"))
            files["mla.txt"].write("[{0}] {1} \n".format(lineNumber, str(e)).encode("utf8"))
            haveExceptionNote = True
        else:
            files["apa.txt"].write("[{0}] {1} \n".format(lineNumber, mapper['APA']).encode("utf8"))
            files["gbt7714.txt"].write("[{0}] {1} \n".format(lineNumber, mapper['GBT7714']).encode("utf8"))
            files["mla.txt"].write("[{0}] {1} \n".format(lineNumber, mapper['MLA']).encode("utf8"))
        services.flushall(files)
        time.sleep(0.01)
    services.closeall(files)
    if(haveExceptionNote):
        raise Exception("【注意】某些论文文献格式获取存在异常，请打开文件检查")
            


if __name__ == "__main__":
    try:    main()
    except: print(sys.exc_info()[1])
    else:   print("【成功】")