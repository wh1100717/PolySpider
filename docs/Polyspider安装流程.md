
#PolySpider安装流程
##1.CentOS 6.4 64Bit下Scrapy服务器环境搭建

###Pre-requisites
*	update centOS lib to latest version by `yum -y update`
*	install development tools by `yum groupinstall -y development`
*	install additional pakage `yum install -y zlib-dev openssl-devel sqlite-devel bzip2-devel`
*	download python v2.7.6 `wget http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tar.xz`
*	unzip downloaded file <br>
	`xz -d Python-3.3.3.tar.xz`<br>	
	`tar -xvf Python-3.3.3.tar`
*	step into Python file by `cd Python-2.7.6`
*	take installation by `./configure` and then `make && make altinstall`

###Fix Yum python-2.7 unsurpported problem
`mv /usr/bin/python /usr/bin/python2.6.6`
`ln -s /usr/local/bin/python2.7 /usr/bin/python`<br>
change the first line code `#!/usr/bin/python` to `#!/usr/bin/python2.6.6`

###setuptools and pip installation
	# Let's download the installation file using wget:
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

###其他依赖包

	pip install Redis
###配置supervisor
安装supervisor

	pip install supervisor
配置supervisor


	[inet_http_server]  
	port=0.0.0.0:9001
	username=poly_admin
	password=poly123
	
	[supervisord]
	logfile=tmp/supervisord.log ; (main log file;default $CWD/supervisord.log)
	logfile_maxbytes=50MB        ; (max main logfile bytes b4 rotation;default 50MB)
	logfile_backups=10           ; (num of main logfile rotation backups;default 10)
	loglevel=info                ; (log level;default info; others: debug,warn,trace)
	pidfile=tmp/supervisord.pid ; (supervisord pidfile;default supervisord.pid)
	nodaemon=false               ; (start in foreground if true;default false)
	minfds=1024                  ; (min. avail startup file descriptors;default 1024)
	minprocs=200                 ; (min. avail process descriptors;default 200)
	
	[program:hiapk_spider]
	command=scrapy crawl hiapk
	stderr_logfile=tmp/log/hiapk_std.log        ; stderr log path, NONE for none; default AUTO
	autostart=true
	autorestart=true
	
	[program:baidu_spider]
	command=scrapy crawl baidu
	stderr_logfile=tmp/log/baidu_std.log        ; stderr log path, NONE for none; default AUTO
	autostart=true
	autorestart=true
	
	[program:xiaomi_spider]
	command=scrapy crawl xiaomi
	stderr_logfile=tmp/log/xiaomi_std.log        ; stderr log path, NONE for none; default AUTO
	autostart=true
	autorestart=true
	
	[program:appchina_spider]
	command=scrapy crawl appchina
	stderr_logfile=tmp/log/appchina_std.log        ; stderr log path, NONE for none; default AUTO
	autostart=true
	autorestart=true
	
	[program:googleplay_spider]
	command=scrapy crawl googleplay
	stderr_logfile=tmp/log/googleplay_std.log        ; stderr log path, NONE for none; default AUTO
	autostart=true
	autorestart=true
	
	[program:muzhiwan_spider]
	command=scrapy crawl muzhiwan
	stderr_logfile=tmp/log/muzhiwan_std.log        ; stderr log path, NONE for none; default AUTO
	autostart=true
	autorestart=true
	
	;[program:theprogramname]
	;command=/bin/cat              ; the program (relative uses PATH, can take args)
	;process_name=%(program_name)s ; process_name expr (default %(program_name)s)
	;numprocs=1                    ; number of processes copies to start (def 1)
	;directory=/tmp                ; directory to cwd to before exec (def no cwd)
	;umask=022                     ; umask for process (default None)
	;priority=999                  ; the relative start priority (default 999)
	;autostart=true                ; start at supervisord start (default: true)
	;autorestart=unexpected        ; whether/when to restart (default: unexpected)
	;startsecs=1                   ; number of secs prog must stay running (def. 1)
	;startretries=3                ; max # of serial start failures (default 3)
	;exitcodes=0,2                 ; 'expected' exit codes for process (default 0,2)
	;stopsignal=QUIT               ; signal used to kill process (default TERM)
	;stopwaitsecs=10               ; max num secs to wait b4 SIGKILL (default 10)
	;stopasgroup=false             ; send stop signal to the UNIX process group (default false)
	;killasgroup=false             ; SIGKILL the UNIX process group (def false)
	;user=chrism                   ; setuid to this UNIX account to run the program
	;redirect_stderr=true          ; redirect proc stderr to stdout (default false)
	;stdout_logfile=/a/path        ; stdout log path, NONE for none; default AUTO
	;stdout_logfile_maxbytes=1MB   ; max # logfile bytes b4 rotation (default 50MB)
	;stdout_logfile_backups=10     ; # of stdout logfile backups (default 10)
	;stdout_capture_maxbytes=1MB   ; number of bytes in 'capturemode' (default 0)
	;stdout_events_enabled=false   ; emit events on stdout writes (default false)
	;stderr_logfile=/a/path        ; stderr log path, NONE for none; default AUTO
	;stderr_logfile_maxbytes=1MB   ; max # logfile bytes b4 rotation (default 50MB)
	;stderr_logfile_backups=10     ; # of stderr logfile backups (default 10)
	;stderr_capture_maxbytes=1MB   ; number of bytes in 'capturemode' (default 0)
	;stderr_events_enabled=false   ; emit events on stderr writes (default false)
	;environment=A="1",B="2"       ; process environment additions (def no adds)
	;serverurl=AUTO                ; override serverurl computation (childutils)

###启动supervisor
	sudo /etc/init.d/supervisor start
###启动Scrapy
*	进入http://localhost:9001
*	输入用户名：poly_admin 密码：poly123
*	点击start，启动Scrapy

##2.Redis服务器环境搭建

###下载，解压和安装：

	$ wget http://download.redis.io/releases/redis-2.8.5.tar.gz
	$ tar xzf redis-2.8.5.tar.gz
	$ cd redis-2.8.5
	$ make

编译后的可执行文件在src目录中，可以使用下面的命令运行Redis:

	$ ./redis-server
##3.Redmon Redis监控服务器
###安装Ruby
	$ \curl -sSL https://get.rvm.io | bash -s stable --ruby
###安装Redmon
	gem install redmon
###启动Redmon
	$ redmon -r 192.168.1.202:6379  后面为redis的ip地址和端口号
##4.Frontend服务器搭建
###需要的依赖包
	pip install web.py
	pip install Redis
###启动Frontend
	$ python web-server.py
