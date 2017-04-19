#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re

# 为所有png添加后缀
def addSuffix(path, text):
    for x in os.listdir(path):

        abPath = os.path.join(path,x)

        if os.path.isdir(abPath):
            addSuffix(abPath, text)

        elif os.path.splitext(x)[1] == '.png':
            sp = re.split(r'[@.]', x)

            if len(sp) == 2:
                newname = sp[0] + text + '.png'
            else:
                newname = sp[0] + text + '@' + sp[1] + '.png'
            print(newname)
            newPath = os.path.join(os.path.split(abPath)[0], newname)
            os.rename(abPath, newPath)



addSuffix('/Users/S/Desktop/wlwork/workCode/Car项目/魔盒资料/ios全家福蓝色/爱车管理轨迹','-blue')


