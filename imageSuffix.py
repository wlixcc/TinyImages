#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量给iOS图片添加后缀"""

import os, shutil, getopt, sys

inputPath = ''
outputPath = ''
suffix = ''
replace = False

def createOutput(path):
    """
    :param path: 输入path位inputpath,用来计算相对路径
    :return: None
    """
    global outputPath

    # 创建默认输出目录
    if outputPath == '':
        sp = os.path.split(path);
        outputPath = os.path.join(sp[0], sp[1]+'-Sufiix')
    print('\n---输出路径为:%s\n' % outputPath)
    if not os.path.exists(outputPath):
        os.mkdir(outputPath)
    # 父目录, 文件夹名字, 文件名
    for parent, directories, files in list(os.walk(path)):
        for dir in directories:
            # relpath,接收2个参数，第二个参数可选，返回相对路径
            relPath = os.path.relpath(os.path.join(parent, dir), inputPath)
            newPath = os.path.join(outputPath, relPath)
            if not os.path.exists(newPath):
                os.mkdir(newPath)

# 为所有png添加后缀
def addSuffix(path, suffix, replace):
    """
    :param path: input path
    :param suffix: 后缀
    :param replace: 是否直接替换
    :return: None
    """
    suffix = str(suffix)

    for x in os.listdir(path):
        absPath = os.path.join(path, x)

        if os.path.isdir(absPath):
            addSuffix(absPath, suffix, replace)
        elif os.path.splitext(x)[1] == '.png' or os.path.splitext(x)[1] == '.jpg':
            index = x.rfind('@')
            pIndex = x.rfind('.')

            if index == -1:
                newName = x[:pIndex] + suffix + x[pIndex:]
            else:
                newName = x[:index] + suffix + x[index:]
            info = '%s ----> %s' % (x, newName)
            print('\033[1;32;48m' + info + '\033[0m')
            if replace:
                newPath = os.path.join(os.path.split(absPath)[0], newName)
                os.rename(absPath, newPath)
            else:
                relPath = os.path.relpath(path, inputPath)
                newPath = os.path.join(outputPath, relPath, newName)
                shutil.copyfile(absPath, newPath)


def main(path, suffix, output, replace):

    global inputPath, outputPath
    inputPath = path
    outputPath = output

    if not os.path.isdir(path):
        return print('请输入正确文件路径')
    if path in outputPath:
        return print('输出文件不能在子目录中')

    suffix = str(suffix)

    if not replace:
        createOutput(path)
    addSuffix(path, suffix, replace)



try:
    opts = getopt.getopt(sys.argv[1:], 'i:s:o:rh')[0]
    for op, value in opts:
        if op == '-i':
            inputPath = value
        elif op == '-o':
            outputPath = value
        elif op == '-s':
            suffix = value
        elif op == '-r':
            replace = True
        elif op == '-h':
            print('''
              使用方法：  python3 imageSuffix.py -i 输入目录 -s 后缀 [-o 输出目录] [-r]
              例: python3 imageSuffix.py -i /Users/S/Desktop/images -s AA  -o /Users/S/Desktop/newImages
            ''')
except getopt.GetoptError:
    print('命令出错,使用-h获取帮助信息')


if __name__ == '__main__':
    if os.path.isdir(inputPath):
        print('\n---输入路径为:%s\n' % inputPath)
        main(inputPath, suffix, outputPath, replace)




