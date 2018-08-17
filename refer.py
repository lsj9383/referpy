# _*_ coding:utf-8 _*_
import sys
import os
import time
import pyargv
import services
from referpy import searchRef

@pyargv.parse(
    pyargv.KeyValue("paper", "-p", default=""),
    pyargv.KeyValue("fd", "-f" , default=""),
    pyargv.Boolean("debug"),
    )
def main(paper, fd, debug):
    # 快速查询模式
    if(paper):
        try:
            title = sys.argv[1][6:]
            print("search \"{0}\"".format(paper))
            mapper = services.retryWrapper(searchRef, 3)(paper, debug)  # 重试3次
        except Exception as e:  raise e
        else:
            print("【APA】："+mapper["APA"])
            print("【GBT7714A】："+mapper["GBT7714"])
            print("【MLA】："+mapper["MLA"])
            return
    
    # 目录/文件查询模式
    if ((not fd) or (not os.path.exists(fd))):
        raise Exception("【异常】 没有找到该目录或文件：\"{0}\"".format(fd))
    lineNumber = 0
    haveExceptionNote=False
    files = services.openall("wb", "apa.txt", "gbt7714.txt", "mla.txt")
    for title in services.paperTitleItera(fd):
        lineNumber += 1
        print("search \"{0}\"".format(title))
        try:
            # 重试3次
            mapper = services.retryWrapper(searchRef, 3)(title, debug)
        except Exception as e:
            # 出现异常，将错误进行记录
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
    main()
    print("【成功】")