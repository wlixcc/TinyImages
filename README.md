# 图片处理脚本

### 为了减小app体积,写了一些脚本用来批量处理

- 脚本使用python3编写,确认你的操作系统安装了python3
- Mac上安装Python3, 推荐使用Homebrew安装,
	
		$ brew install python3
	 brew装好python3时候会自动安装pip3(python的包管理工具),`tinyImages.py`脚本使用前需要先安装第三方模块。


#### <font color=#0099ff>`tinyImages.py`批量图片压缩脚本</font>


1. 使用前面提到的pip3安装第三方模块
		
		$ pip3 install aiohttp

2. 直接运行脚本,根据提示输入内容即可。
	    
	    $ python3 tinyImages.py
	  如果直接替换图片,使用前最好备份,以免出现接口调用上限等意外情况造成只有部分图片压缩的情况。

- 运行示例
	![运行示例](http://oqc26haeb.bkt.clouddn.com/tinyimageShot.jpeg)

	>  该脚本使用[tinypng](https://tinypng.com/)提供的接口进行图片压缩,压缩前后图片质量基本没有差距,大小一般可以缩小50%左右,使用前需要[获取API key](https://tinypng.com/developers),只要填写邮箱就可以了。获取到APIKey后就可以使用脚本进行批量压缩了。网站限制为每个月调用500次接口，不够用换一个邮箱注册就可以了。

- 更多设置,使用命令行参数:

        $ python3 tinyImages.py  -i 输入路径 -a APIKey [-o 输出路径] [-r(直接替换原文件)]

	
	比如你想压缩`/Users/S/Desktop/Assets.xcassets`下的所有图片并且输出到`/Users/S/Desktop/newImages`:
    
        $ python3 tinyImages.py -i /Users/S/Desktop/Assets.xcassets -a wwj8jDJZG0Y7b80jMakg3SJm64BrK8wR -o /Users/S/Desktop/newImages



- 目前一次性替换最大数量为500,后续版本应该会添加多个APIkey的支持,一个apikey使用达到上限后自动切换。突破压缩数量最大为500的限制


#### <font color=#0099ff>`remove1xImage.py`批量删除.xcassets目录下的1x的图片</font>
1.  直接运行脚本
	   
	    $ python3 remove1xImage.py


    > iOS有两倍图,三倍图,实际项目中如果3种图片都有的时候1x图片是使用不到的,可以通过脚本批量删除。当图片不是1x,2x,3x都有的时候不会进行删除操作，比如只有一张1x图，2x,3x图片都是没有的情况下会直接跳过，避免出现误删的情况。

- 也可以使用命令行参数`python3 remove1xImage.py -i 项目路径`  

	    $ python3 remove1xImage.py -i /Users/S/Desktop/testAPP
	

#### <font color=#0099ff>`imageSuffix.py`批量给图片添加后缀</font>
- 针对iOS的图片处理写的，对@2x,@3x图片也能正确添加后缀

        $ python3 imageSuffix.py -i 输入目录 -s 后缀名 [-o 输出目录] [-r]
	    #给/Users/S/Desktop/images路径下的所有图片添加'test'后缀
	    $ python3 imageSuffix.py -i /Users/S/Desktop/images -s test
	

#### <font color=#0099ff>`imageSize.py`按大小输出图片文件名字</font>
- 统计文件夹下图片大小，输出文件路径,默认输出前10

        $ python3 imageSize.py -i 项目路径 [-l 打印数量默认为10]
		#打印/Users/S/Desktop/images路径下最大的20张图片的路径
        $ python3 imageSize.py -i /Users/S/Desktop/images -l 20
