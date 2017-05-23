#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import stat


def pyfile_config(path):
    for abPath in [os.path.join(path, x) for x in os.listdir(path)]:
        if os.path.splitext(abPath)[1] == '.py':
            change_mode(abPath)
            add_annotation(abPath)
        elif os.path.isdir(abPath):
            pyfile_config(abPath)


# 修改权限
def change_mode(path):
    os.chmod(path, stat.S_IRWXU | stat.S_IXGRP | stat.S_IRGRP | stat.S_IROTH | stat.S_IXOTH)  # 755权限


# 添加注释
def add_annotation(path):
    with open(path, 'r+', encoding='utf-8') as f:
        if not f.readline().startswith('#!/usr/bin/env python3'):
            f.seek(0, 0)
            a = f.readlines()
            a.insert(0, '#!/usr/bin/env python3\n')
            a.insert(1, '# -*- coding: utf-8 -*-\n')
            s = ''.join(a)
            f.seek(0, 0)
            f.write(s)
            print('success-->', path)
