#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, stat

def wlpyfileconfig(path):
    for x in os.listdir(path):
        abPath = os.path.join(path,x)
        if os.path.splitext(x)[1] == '.py':
            changeMode(abPath)
            addAnnotation(abPath)
        elif os.path.isdir(abPath):
            wlpyfileconfig(abPath)



# 修改权限
def changeMode(path):
    os.chmod(path, stat.S_IRWXU | stat.S_IXGRP | stat.S_IXOTH)   #711权限

# 添加注释
def addAnnotation(path):
    with open(path, 'r+', encoding='utf-8') as f:
        if not f.readline().startswith('#!/usr/bin/env python3'):
            f.seek(0, 0)
            s = f.read()
            a = s.split('\n')
            a.insert(0, '#!/usr/bin/env python3')
            a.insert(1, '# -*- coding: utf-8 -*-')
            s = '\n'.join(a)
            f.seek(0, 0)
            f.write(s)
            print('success-->', path)



wlpyfileconfig('/Users/S/Desktop/workMaterial/Python')

