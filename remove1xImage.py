#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用于去除.xcasssets文件夹下的所有1x图片"""

import os
import sys
import getopt
import json


def batch_remove_1ximage(path):
    if not isinstance(path, str) or not os.path.isdir(path):
        return
    for abpath in [os.path.join(path, x) for x in os.listdir(path)]:
        if os.path.isdir(abpath) and abpath.endswith('.xcassets'):
            search_images(abpath)
        else:
            batch_remove_1ximage(abpath)


def search_images(path):
    if not os.path.isdir(path):
        return
    for abpath in [os.path.join(path, x) for x in os.listdir(path)]:
        if os.path.isdir(abpath) and abpath.endswith('.imageset'):
            remove1ximage(abpath)
        else:
            search_images(abpath)  # 子文件夹处理


def remove1ximage(path):
    if len(os.listdir(path)) != 4:
        return
    for abpath in [os.path.join(path, x) for x in os.listdir(path)]:
        if not (abpath.find('@') >= 0) and not abpath.endswith('.json'):
            os.remove(abpath)
            print('del----->%s' % abpath)
        if abpath.endswith('.json'):
            alter_json(abpath)


def alter_json(path):
    with open(path) as f:
        dic = json.loads(f.read())
        if 'filename' in dic['images'][0]:
            dic['images'][0].pop('filename')
        jsonstr = json.dumps(dic, indent=4, sort_keys=False, ensure_ascii=False)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(jsonstr)


inputPath = ''

try:
    opts = getopt.getopt(sys.argv[1:], 'i:h')[0]
    for opt, value in opts:
        if opt == '-i':
            inputPath = value
        elif opt == '-h':
            print("""
               python3 remove1xImage.py -i 项目路径
            """)

except getopt.GetoptError:
    print('使用-h获取帮助信息')

if __name__ == '__main__':
    if inputPath == '':
        inputPath = input('请输入项目路径:')
    if not os.path.isdir(inputPath):
        print('输入路径有误')
        exit()
    batch_remove_1ximage(inputPath)
