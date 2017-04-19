#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#用于去除.xcasssets文件夹下的所有1x图片
import os, json

def batchRemove1xImage(path):
    for x in os.listdir(path):
        abPath = os.path.join(path, x)
        if os.path.isdir(abPath):
            if abPath.endswith('.xcassets'):
                removeImages(abPath)
            else:
                batchRemove1xImage(abPath)


def removeImages(path):
    for x in os.listdir(path):
        abPath = os.path.join(path, x)
        if os.path.isdir(abPath) and abPath.endswith('.imageset'):
            remove1xImage(abPath)
            alterContentsjson(abPath)
        elif os.path.isdir(abPath):
            batchRemove1xImage(abPath)

def remove1xImage(path):

    if len(os.listdir(path)) != 4:
        return

    for x in os.listdir(path):
        abPath = os.path.join(path, x)
        if not (x.find('@') >= 0) and x.endswith('png'):
            os.remove(abPath)

def alterContentsjson(path):

    if len(os.listdir(path)) == 2:
        return

    for x in os.listdir(path):
        if x == 'Contents.json':
            with open(os.path.join(path, x)) as f:
                dic = json.loads(f.read())
                if 'filename' in dic['images'][0]:
                    dic['images'][0].pop('filename')
                str = json.dumps(dic, indent=4, sort_keys=False, ensure_ascii=False)

            with open(os.path.join(path, x), 'w', encoding='utf-8') as f:
                f.write(str)









