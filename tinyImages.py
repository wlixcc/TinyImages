"""
使用 https://tinypng.com/developers/reference#compressing-images 提供的接口进行图片压缩
"""

import os
import sys
import getopt
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
taskNum = 0


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
        out_dir = os.path.join(parent, '{0}-Tiny'.format(child))
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


def generate_paths(path):
    """
       生成输入输出路径列表
       :param path: 文件路径
       :return None
    """
    for x in os.listdir(path):
        abs_path = os.path.join(path, x)

        if os.path.isdir(abs_path):
            generate_paths(abs_path)
        elif os.path.splitext(x)[1] == '.png' or os.path.splitext(x)[1] == '.jpg':
            if replace:
                new_path = abs_path
            else:
                rel_path = os.path.relpath(path, inputPath)
                new_path = os.path.join(outputPath, rel_path, x)
            imgPaths.append((abs_path, new_path))


async def tiny_image(from_file, to_file, session):
    sp = os.path.split(to_file)
    # print('\033[1;34;48m准备上传-->:' + sp[1] + '\033[0m')
    url = ''

    with open(from_file, 'rb') as f:
        source_img = f.read()

    try:
        async with session.post(apiAdress, data=source_img, headers=authHedder) as response:
            status = response.status
            if status == 201:
                print('\033[1;34;48m上传完成-->:' + sp[1] + '\033[0m')
                json = await response.json()
                # wirteToFile(json)
                url = json['output']['url']
            elif status == 429:
                print('本月数量已超过限制-->%s转换失败' % sp[1])
            else:
                print('api接口调用出错:%s' % status)
    except Exception as e:
        print('上传异常:' % e)

    if not url == '':
        await wirte_img(to_file, url, session)


# def wirteToFile(info):
#     logging.debug(info)

async def wirte_img(to_file, url, session):
    global taskNum
    async with session.get(url, headers={'Content-Type': 'application/json'}) as response:
        new_img = await response.read()
        with open(to_file, 'wb') as compress_img:
            compress_img.write(new_img)
        taskNum -= 1
        info = '成功(剩余任务数量：%s)----> %s' % (taskNum, to_file)
        print('\033[1;32;48m' + info + '\033[0m')


async def main():
    tasks = []
    # 根据图片文件数量计算长连接保持时间
    tcp_connector = aiohttp.TCPConnector(loop=loop)
    async with aiohttp.ClientSession(loop=loop, connector=tcp_connector) as session:
        # 生成任务
        for i, o in imgPaths:
            tasks.append(tiny_image(i, o, session))
        await asyncio.wait(tasks)


try:
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
            authHedder['Authorization'] = 'Basic %s' % b64encode(bytes('api:' + authKey, 'ascii')).decode('ascii')
        elif opt == '-h':
            print('''
                python3 tinyImages.py  -i 输入路径 -a authKey [-o 输出路径] [-r(直接替换原文件)]
            ''')
except getopt.GetoptError:
    print('命令出错,使用-h获取帮助信息')

if __name__ == '__main__':
    if inputPath == '':
        inputPath = input('请输入图片文件夹路径：').strip()
        while True:
            r = input('是否直接替换(yes/no): ').lower()
            if r == 'yes':
                replace = True
                break
            elif r == 'no':
                break
            else:
                print('请输入yes/no')
    if authKey == '':
        authKey = input('请输入API key, 到https://tinypng.com/developers获取:').strip()
        authHedder['Authorization'] = 'Basic %s' % b64encode(bytes('api:' + authKey, 'ascii')).decode('ascii')
    if not os.path.isdir(inputPath):
        print('目录不正确')
        exit()
    if not replace:
        outputPath = create_output_dirs(inputPath, outputPath)
        print('图片文件输出到 %s' % outputPath)
    generate_paths(inputPath)
    taskNum = len(imgPaths)
    if taskNum > 500:
        r = input('任务数量为%s,超过500', taskNum)
        exit()
    else:
        print('任务数量%s' % taskNum)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
