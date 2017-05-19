# 图片处理脚本

### 为了减小app体积,写了一些脚本用来批量处理

> 准备工作

- 脚本使用python3编写,确认你的操作系统安装的python3
- Mac上安装Python3, 推荐使用Homebrew安装, `brew install python3`, brew装好python3时候会自动安装pip3(python的包管理工具),部分脚本可能会使用到第三方模块。

> 脚本使用方法

#### `tinyImages.py`批量图片压缩脚本
- 该脚本使用[tinypng](https://tinypng.com/)提供的接口进行图片压缩,压缩前后图片质量基本没有差距,大小一般可以缩小50%左右,使用前需要[获取API key](https://tinypng.com/developers),只要填写邮箱就可以了。获取到APIKey后就可以使用脚本进行批量压缩了。网站限制为每个月调用500次接口，不够用换一个邮箱注册就可以了。

1. 使用前面提到的pip3安装第三方模块`$ pip3 install aiohttp`

2. 可以直接运行脚本`python3 tinyImages.py`,会提示你输入文件夹路径和APIkey,输入结束后直接开始图片压缩(不覆盖原文件),压缩的图片会保存在`你的图片文件夹名称-tiny`目录下

3. 使用命令行参数:` python3 tinyImages.py  -i 输入路径 -a APIKey [-o 输出路径] [-r(直接替换原文件)]`

	-i参数后面带图片文件夹路径,-a参数后面是APIKey。如果输入-r(可选)参数,直接替换原文件， -o(可选)参数可自定义输出目录
	
	比如你想压缩`/Users/S/Desktop/Assets.xcassets`下的所有图片并且直接替换:`$ python3 tinyImages.py -i /Users/S/Desktop/Assets.xcassets -a wwj8jDJZG0Y7b80jMakg3SJm64BrK8wR -r`

> 如使用-r参数,使用前请备份图片文件，以免出现网络断开，压缩数量超过限制等意外情况。

- 目前一次性替换最大数量为500,后续版本应该会添加多个APIkey的支持,一个apikey使用达到上限后自动切换。突破压缩数量最大为500的限制


#### `remove1xImage.py`批量删除.xcassets目录下的1x的图片
- iOS有两倍图,三倍图,实际项目中如果3种图片都有的时候1x图片是使用不到的,可以通过脚本批量删除。当图片不是1x,2x,3x都有的时候不会进行删除操作，比如只有一张1x图，2x,3x图片都是没有的情况下会直接跳过，以免误删。
- 会自动搜索项目下的`.xcassets`文件夹目录

2. `python3 remove1xImage.py -i 项目路径`  
	例：`$ python3 remove1xImage.py -i /Users/S/Desktop/testAPP`
	

#### `imageSuffix.py`批量给图片添加后缀
- 针对iOS的图片处理写的，对@2x,@3x图片也能正确添加后缀

1. `python3 imageSuffix.py -i 输入目录 -s 后缀名 [-o 输出目录] [-r]`
	
	例，给所有图片添加`test`后缀:`$ python3 imageSuffix.py -i /Users/S/Desktop/images -s test`
	

#### `imageSize.py`按大小输出图片文件名字
- 统计文件夹下图片大小，输出文件路径,默认输出前10

1. `python3 imageSize.py -i 项目路径 [-l 打印数量默认为10]`
	
	例: `python3 imageSize.py -i /Users/S/Desktop/images -l 20`
