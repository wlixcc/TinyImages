"""
使用 https://tinypng.com/developers/reference/python 提供的接口进行图片缩小
    pip3 install --upgrade tinify
"""

import os, sys, getopt
import tinify
# from multiprocessing import Pool
import asyncio

tinify.key = 'PX-pm9lAY3siS8cHIWz44zWFZHj6TtYX'

def createOutput(path):
    """
    :param path: 输入path位inputpath,用来计算相对路径
    :return: None
    """
    global outputPath

    # 创建默认输出目录
    if outputPath == '':
        sp = os.path.split(path);
        outputPath = os.path.join(sp[0], sp[1]+'-Tiny')
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

async def tinyImages(path, replace):
    """
       :param path: 文件路径
       :param replace: 是否直接替换
       :return: None
    """
    for x in os.listdir(path):
        absPath = os.path.join(path, x)

        if os.path.isdir(absPath):
            tinyImages(absPath, replace)
        elif os.path.splitext(x)[1] == '.png' or os.path.splitext(x)[1] == '.jpg':
            if replace:
                newPath = absPath
            else:
                relPath = os.path.relpath(path, inputPath)
                newPath = os.path.join(outputPath, relPath, x)
            await tinyImage(absPath, newPath)




async def tinyImage(source, to_file):
    # await source = tinify.from_file(source)
    # await source.to_file(to_file)
    await asyncio.sleep(1)
    info = '%s ----> %s' % (source, to_file)
    print('\033[1;32;48m' + info + '\033[0m')

inputPath = ''
outputPath = ''
replace = False
# p = Pool(4)

opts = getopt.getopt(sys.argv[1:], 'i:o:rh')[0]
for opt, value in opts:
    if opt == '-i':
        inputPath = value
    elif opt == '-o':
        outputPath = value
    elif opt == '-r':
        replace = True
    elif opt == '-h':
        print('''
            python3 tinyImages.py  -i 输入路径 [-o 输出路径] [-r(直接替换原文件)]
        ''')


if __name__ == '__main__':
    if inputPath == '':
        print('请输入图片文件夹路径,使用-h获取帮助')
    else:
        createOutput(inputPath)
        loop = asyncio.get_event_loop()
        loop.run_until_complete( tinyImages(inputPath, replace))
        loop.close()

        # print('等待所有图片转换')
        # p.close()
        # p.join()
        # print('所有任务完成')