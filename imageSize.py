#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按图片尺寸从大到小打印图片相对路径,默认打印最大的10张图片,数量可以通过-l参数更改, -i参后带项目路径"""

import sys, getopt
import os

def orderBySize(path):
    for x in os.listdir(path):
        abPath = os.path.join(path, x)
        if os.path.isdir(abPath):
            if abPath.endswith('.xcassets'):
                order(abPath)
            else:
                orderBySize(abPath)


def order(path):
    for x in os.listdir(path):
        abPath = os.path.join(path, x)
        if os.path.isdir(abPath) and abPath.endswith('.imageset'):
            addinfo(abPath)
        elif os.path.isdir(abPath):
            order(abPath)



def addinfo(path):
    for x in os.listdir(path):
        abPath = os.path.join(path, x)
        relPath = abPath[pathLength:]
        if os.path.splitext(x)[1] == '.png':
            info = (relPath, os.path.getsize(abPath))
            list.append(info)

projectPath = ''
list = []
pathLength = 0
limit = 10

try:
    opts = getopt.getopt(sys.argv[1:], 'i:h')[0]
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
    print('使用-h获取帮助信息')

if __name__=='__main__':
    if os.path.isdir(projectPath):
        pathLength = len(projectPath)
        orderBySize(projectPath)
        list.sort(key=lambda x: x[1], reverse=True)
        for x in list[:limit]:
            print(x)