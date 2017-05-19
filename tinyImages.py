"""
使用 https://tinypng.com/developers/reference#compressing-images 提供的接口进行图片压缩
"""

import os, sys, getopt
from base64 import b64encode
import asyncio
import aiohttp
# import logging

# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S',
#                     filename='tinyimage.log',
#                     filemode='a+')

# authKey = 'PX-pm9lAY3siS8cHIWz44zWFZHj6TtYX'
apiAdress = 'https://api.tinify.com/shrink'
authKey = ''
authHedder = {}
inputPath = ''
outputPath = ''
replace = False
imgPaths = []

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

def generatePath(path, replace):
    """
       :param path: 文件路径
       :param replace: 是否直接替换
       :return: None
    """
    for x in os.listdir(path):
        absPath = os.path.join(path, x)

        if os.path.isdir(absPath):
            generatePath(absPath, replace)
        elif os.path.splitext(x)[1] == '.png' or os.path.splitext(x)[1] == '.jpg':
            if replace:
                newPath = absPath
            else:
                relPath = os.path.relpath(path, inputPath)
                newPath = os.path.join(outputPath, relPath, x)
            imgPaths.append((absPath, newPath))

async def tinyImage(from_file, to_file, session):

    sp = os.path.split(to_file)
    print('\033[1;34;48m准备上传-->:' + sp[1] + '\033[0m')
    url = ''

    with open(from_file, 'rb') as source_img:
        async with session.post(apiAdress, data=source_img, headers=authHedder) as response:
            status = response.status
            if status == 201:
                json = await response.json()
                # wirteToFile(json)
                url = json['output']['url']
                await wirteImg(to_file, url, session)
            elif status == 429:
                print('本月数量已超过限制-->%s转换失败' % sp[1])
            else:
                print('api接口调用出错:%s' % status)
                url = '1'

    if not url == '':
        await wirteImg(to_file, url, session)

# def wirteToFile(info):
#     logging.debug(info)

async def wirteImg(to_file, url, session):
    async with session.get(url, headers={'Content-Type': 'application/json'}) as response:
        newImg = await response.read()
        with open(to_file, 'wb') as compress_img:
            compress_img.write(newImg)
            info = '成功----> %s' % to_file
            print('\033[1;32;48m' + info + '\033[0m')


opts = getopt.getopt(sys.argv[1:], 'i:o:a:rh')[0]
for opt, value in opts:
    if opt == '-i':
        inputPath = value
    elif opt == '-o':
        outputPath = value
    elif opt == '-r':
        replace = True
    elif opt == '-a':
        authKey = value
        authHedder['Authorization'] = 'Basic %s' % b64encode(bytes('api:'+authKey, 'ascii')).decode('ascii')
    elif opt == '-h':
        print('''
            python3 tinyImages.py  -i 输入路径 -a authKey [-o 输出路径] [-r(直接替换原文件)]
        ''')


async def main(loop, fileNums):
    # 限制同一之间任务数量，打开过多的文件会有异常抛出
    limit = 150
    tasks = []
    # 根据图片文件数量计算长连接保持时间
    timeout = min(fileNums * 2, 200)
    tcpConnector = aiohttp.TCPConnector(keepalive_timeout=timeout, loop=loop)
    async with aiohttp.ClientSession(loop=loop, connector=tcpConnector) as session:
        # 生成任务
        for i, o in imgPaths:
            tasks.append(tinyImage(i, o, session))
        # 限制一次性执行任务的数量
        start = 0
        end = min(len(imgPaths), limit)
        while True:
            once = tasks[start:end]
            await asyncio.wait(once)
            if end == len(imgPaths):
                break
            else:
                start = end
                end = min(len(imgPaths), limit+end)


if __name__ == '__main__':
    if inputPath == '':
        inputPath = input('请输入图片文件夹路径：')
    if authKey == '':
        authKey = input('请输入API key, 到https://tinypng.com/developers获取:')
        authHedder['Authorization'] = 'Basic %s' % b64encode(bytes('api:' + authKey, 'ascii')).decode('ascii')
    if not replace:
        createOutput(inputPath)
    generatePath(inputPath, replace)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop, fileNums=len(imgPaths)))
    loop.close()

