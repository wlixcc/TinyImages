#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量给iOS图片添加后缀"""
import sys
import os
import shutil
import getopt

inputPath = ''
outputPath = ''
gSuffix = ''
gReplace = False


def create_output_dirs(in_dir, out_dir):
    """
    根据输入路径创建输出文件夹
    :param in_dir: 输入路径
    :param out_dir: 输出路径
    :return: 输出路径
    """
    # 创建默认输出目录
    if out_dir == '':
        (parent, child) = os.path.split(in_dir)
        out_dir = os.path.join(parent, '{0}-sufiix'.format(child))
    print('\n---输出路径为:%s\n' % out_dir)
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    # 父目录, 文件夹名字, 文件名
    for parent, directories, files in list(os.walk(in_dir)):
        for dirname in directories:
            # relpath,接收2个参数，第二个参数可选，返回相对路径
            rel_path = os.path.relpath(os.path.join(parent, dirname), in_dir)
            new_path = os.path.join(out_dir, rel_path)
            if not os.path.exists(new_path):
                os.mkdir(new_path)
    return out_dir


# 为所有png添加后缀
def add_suffix(path, suffix, replace):
    """
    :param path: input path
    :param suffix: 后缀
    :param replace: 是否直接替换
    :return: None
    """
    suffix = str(suffix)

    for x in os.listdir(path):
        abs_path = os.path.join(path, x)

        if os.path.isdir(abs_path):
            add_suffix(abs_path, suffix, replace)
        elif os.path.splitext(x)[1] == '.png' or os.path.splitext(x)[1] == '.jpg':
            index = x.rfind('@')
            p_index = x.rfind('.')

            if index == -1:
                new_name = x[:p_index] + suffix + x[p_index:]
            else:
                new_name = x[:index] + suffix + x[index:]
            info = '%s ----> %s' % (x, new_name)
            print('\033[1;32;48m' + info + '\033[0m')
            if replace:
                new_path = os.path.join(os.path.split(abs_path)[0], new_name)
                os.rename(abs_path, new_path)
            else:
                rel_path = os.path.relpath(path, inputPath)
                new_path = os.path.join(outputPath, rel_path, new_name)
                shutil.copyfile(abs_path, new_path)


def main():
    global outputPath
    if not os.path.isdir(inputPath):
        return print('请输入正确文件路径')
    if inputPath in outputPath:
        return print('输出文件不能在子目录中')

    if not gReplace:
        outputPath = create_output_dirs(inputPath, outputPath)
    add_suffix(inputPath, gSuffix, gReplace)


try:
    opts = getopt.getopt(sys.argv[1:], 'i:s:o:rh')[0]
    for op, value in opts:
        if op == '-i':
            inputPath = value
        elif op == '-o':
            outputPath = value
        elif op == '-s':
            gSuffix = value
        elif op == '-r':
            gReplace = True
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
        main()
