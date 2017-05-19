#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按图片尺寸从大到小打印图片相对路径,默认打印最大的10张图片,数量可以通过-l参数更改, -i参后带项目路径"""

import sys, getopt
import os

projectPath = ''
sizeList = []
pathLength = 0
limit = 10

def orderBySize(path):
    for x in os.listdir(path):
        abPath = os.path.join(path, x)
        if os.path.isdir(abPath):
            orderBySize(abPath)
        else:
            addinfo(abPath)


def addinfo(path):
    relPath = path[pathLength:]
    suffix = os.path.splitext(path)[1]
    if suffix == '.png' or suffix == '.jpg':
        info = (relPath, os.path.getsize(path))
        sizeList.append(info)



try:
    opts = getopt.getopt(sys.argv[1:], 'i:l:h')[0]
    for op, value in opts:
        if op == '-i':
            print('工程路径:%s\n' % value)
            projectPath = value
        elif op == '-l' and int(value) > 0:
            limit = int(value)
        elif op == '-h':
            print('''
              使用方法：  python3 imageSize.py -i 项目路径 [-l 打印数量]
            ''')
except getopt.GetoptError:
    print('命令错误,使用-h获取帮助信息')

if __name__=='__main__':
    if os.path.isdir(projectPath):
        pathLength = len(projectPath)
        orderBySize(projectPath)
        sizeList.sort(key=lambda x: x[1], reverse=True)
        for x in sizeList[:limit]:
            print(x)