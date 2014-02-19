#PolySpider安装流程

##1. CentOS 6.4 64Bit下Scrapy环境搭建

###Pre-requisites
*	update centOS lib to latest version by `yum -y update`
*	install development tools by `yum groupinstall -y development`
*	install additional pakage `yum install -y zlib-dev openssl-devel sqlite-devel bzip2-devel`
*	download python v2.7.6 `wget http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tar.xz`
*	unzip downloaded file <br>
	`xz -d Python-2.7.6.tar.xz`<br>	
	`tar -xvf Python-2.7.6.tar.xz`
*	step into Python file by `cd Python-2.7.6`
*	take installation by `./configure` and then `make && make altinstall`

###Fix Yum python-2.7 unsurpported problem
*	`mv /usr/bin/python /usr/bin/python2.6.6`
*	`ln -s /usr/local/bin/python2.7 /usr/bin/python`
*	`vim /usr/bin/yum`
*	change the first line code `#!/usr/bin/python` to `#!/usr/bin/python2.6.6`

###setuptools and pip installation
	# Download the installation file using wget:
	wget --no-check-certificate https://pypi.python.org/packages/source/s/setuptools/setuptools-1.4.2.tar.gz
	
	# Extract the files from the archive:
	tar -xvf setuptools-1.4.2.tar.gz
	
	# Enter the extracted directory:
	cd setuptools-1.4.2
	
	# Install setuptools using the Python we've installed (2.7.6)
	python setup.py install
	
	# Install pip
	easy_install pip
	#alternative
	curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python2.7 -

###Fix lxml installation error problem
	yum install libxslt-devel

###Scrapy Installation
	pip install scrapy

###Dependencies
	pip install supervisor #用来监控爬虫
	pip install redis #redis-py，python访问redis的封装库
	pip install upyun #又拍云接口库
	pip install pybcs #百度云接口库
	pip install progressbar #自己实现了一个文件上传和下载的进度条，其为依赖库

###Support Log Monitor
    yum install python-devel
    easy_install -U setuptools
    pip install twisted
    pip install autobahn
    pip install sh

---

##2. 配置并启动PolySpider项目
PolySpider项目地址, 点击[这里](https://github.com/wh1100717/PolySpider/tree/0.3)查看

(Note: 其为私有GitHub Repository,需要加入小组才能看到)

supervisor是一个用来统一管理python程序的工具，其配有相应的控制前端页面，并可以实现爬虫结束重爬等功能，利用其可以轻松管理多个spider以及其他python程序。

*   配置PolySpider/src/config/Config.py中的一些配置信息。
    *   Redis的配置信息
    *   Tor的配置信息(目前不可用，会在v0.5版本中完成)
    *   AppStart的配置信息(默认就好，不需要更改)
    *   BaiduYun和UpYun的配置信息(目前下载apk的功能已实现但暂不需要，故留空就好)
*   PolySpider/src/PolySpider/settings.py中包含一些信息:
    *   `LOG_LEVEL` 默认为`DEBUG` 用于测试和开发，如果线上跑数据则改成`INFO`
    *   `DOWNLOAD_DELAY` 默认为3秒，scrapy会随机1~3秒抓访问一次网页来抓取数据，主要用来防止被网站Ban掉
    *   `RANDOMIZE_DOWNLOAD_DELAY`默认为true,和`DOWNLOAD_DELAY`配合使用
*   由于supervisor会往`PolySpider/src/tmp`及`PolySpider/src/tmp/log`目录下写日志文件，如果没有该文件夹会报错，故需要提前建立这两个文件夹
*   supervisor.conf文件放在PolySpider/src/目录下,如需更改请直接参考已有默认配置

###启动supervisor
    #进入PolySpider/src/目录下
	supervisord -c supervisor.conf
	#如果想实现开机自启动可以查看supervisor的文档

接下来可以通过`localhost:9001`来查看具体的爬虫状态，用户名为`poly_admin`，密码为`poly123`(可以在supervisor.conf中更改和配置)

###启动Log Monitor
two files should be included in your log system -- server.py(which would generate a server watching the log file and broadcast the data to the browser) and log.html(it contains the html and js code which would be included in your website.)
* just step into the directory that contains the server.py and use command `python server.py log_path port`(log_path means the absolute path of the log file which you want to bring to the web; port means the server port you specified.)
* modify the log.html with your own ip address(or hostname) and port and put the code in some page of your website.
* Then, just wath the page in browser and see what will happen!
* If you want to stop the server, just use `ctrl+c` to stop it. NEVER use `ctrl+d`, there is a thread process which will not be killed in this way(well, u can use `ps -ef | grep server.py` to see whch one should be killed and then use `kill -9 process_id`. THAT is NOT recommended!).

---

##3. 服务器端Redis环境搭建

###下载，解压和安装：

	$ wget http://download.redis.io/releases/redis-2.8.5.tar.gz
	$ tar xzf redis-2.8.5.tar.gz
	$ cd redis-2.8.5
	$ make

编译后的可执行文件在src目录中，可以使用下面的命令运行Redis:`$ .src/redis-server`

如果需要查看redis的运行状态，可以安装Redmon监控，具体的安装步骤如下：
###安装Ruby
	$ \curl -sSL https://get.rvm.io | bash -s stable --ruby
###安装Redmon
	gem install redmon
###启动Redmon
	$ redmon -r redis_ip:redis_port
	#e.g. $ redmon -r 192.168.1.202:6379

---

##4. 搭建PolySpiderFrontend
Python的搭建环境与PolySpider相同，额外需要安装`pip install web.py`

PolySpiderFrontend项目地址, 点击[这里](https://github.com/wh1100717/PolySpiderFrontend)查看

(Note: 私有GitHub Repository,需要加入小组才能看到)

启动PolySpiderFrontend项目:

*   更改`PolySpiderFrontend/web/config/Config.py`中Redis服务器的配置
*   进入`PolySpiderFrontend/web/`目录
*   执行`python web-server.py` #默认端口为8080
*   服务器开启，直接本地执行localhost:8080即可查看
*   Note: web.py自带的服务器只适合用在请求量较少或者demo演示的场景，如果需要处理大并发量，必须更换服务器，具体请参考[这里](http://webpy.org/cookbook/)的Deployment Session.

---
