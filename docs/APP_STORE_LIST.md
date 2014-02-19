#应用商店分析
##[Google Play]（推荐爬取）
###介绍
Google Play前名为Android Market，是一个由Google为Android设备开发的在线应用程序商店。一个名为“Play Store”的应用程序会预载在允许使用Google Play的手机上，可以让用户去浏览、下载及购买在Google Play上的第三方应用程序。
但由于中国政策问题，Google没有提供支付的服务，所以所有需要支付的应用在国内的googleplay是看不到的，从而造就出国内种种安卓市场
但是免费应用还是占据不少比例的，所以推荐爬去
###应用数量
应用数量不确定
###应用分类
*	个性化          
*	交通运输        
*	体育            
*	健康与健身      
*	动态壁纸        
*	动漫            
*	医药            
*	商务            
*	图书与工具书    
*	天气            
*	娱乐            
*	媒体与视频      
*	小部件          
*	工具            
*	摄影            
*	效率            
*	教育            
*	新闻杂志        
*	旅游与本地出行  
*	生活时尚        
*	社交            
*	财务            
*	购物            
*	软件与演示          
*	通讯            
*	音乐与音频      
*	游戏            
###链接详情
	https://play.google.com/store/apps/details?id=com.hrs.b2c.android
googleplay应用是通过下发到手机去安装所以获取不到apk
##[小米商店]（推荐爬取）
###介绍
小米商店用户主要为小米手机和miui ＲＯＭ，小米手机在２０１３年上半年就已经售出７０３万台，２０１２年为７１９万台，拥有大量的用户群体，并且大多数小米用户会通过小米自带应用商店下载应用，推荐爬取
###应用数量
应用数量不确定
###应用分类
*	影音视听
*	图书与阅读
*	效率办公
*	生活
*	摄影摄像
*	体育运动
*	娱乐消遣
*	实用工具
*	聊天与社交
*	学习与教育
*	时尚与购物
*	旅行与交通
*	医疗与健康
*	新闻
*	理财
*	游戏

	*	策略
	*	竞速
	*	棋牌
	*	音乐游戏
	*	飞行模式
	*	动作冒险
	*	角色扮演
	*	体育运动
	*	益智解密
	*	重力感应


###链接详情
应用页面链接：<br>
	`http://app.xiaomi.com/detail/197`<br>
发送请求：

	http://app.xiaomi.com/download/197

apk地址(Response Hearder:location)：

	http://file.market.xiaomi.com/download/AppStore/ba4dd95d-9721-43a4-960b-4e4c2de974cf/%E7%99%BE%E5%BA%A6%E8%A7%86%E9%A2%91.apk
##[天翼空间]
###介绍
应用总量虽然比较多 但是用户下载量太少
主要面向电信用户
下载需要验证码
###应用数量：215436（2013/12/30）

##[移动应用商店]
###介绍
主要面向移动定制机用户，下载量不大
###应用数量：48958（2013/12/30）
游戏：10468

* 免费游戏：7347<br>
* 付费游戏：3121<br>

软件：34575

* 免费软件：18312
* 付费软件：16263
主题软件：3915
* 免费主题：2949
* 付费主题：966
###链接详情
app下载地址：<br>
	`http://mm.10086.cn/download/android/13915?from=www`

##[沃商店]
###介绍
下载需要登录
主要用户为联通定制手机用户
###应用数量
应用数量不确定

##[应用宝]
###介绍
应用宝是腾讯旗下的应用商店，由于腾讯的大量用户，其应用商店下载量也是十分大的，加上众多QQ游戏是由应用宝首发，导致用户必须拥有应用宝才能下载，从而导致用户量大量上涨
###应用数量
应用数量不确定

*	腾讯软件
*	社交
*	系统
*	安全
*	工具
*	音乐
*	视频
*	娱乐
*	阅读
*	美化
*	生活
*	导航
*	通讯
*	摄影
*	理财
*	教育
*	健康
*	购物
*	办公
*	新闻
*	旅游
*	儿童
*	游戏

	* 休闲
	* 棋牌
	* 动作
	* 战略
	* 射击
	* 赛车
	* 角色
	* 冒险
	* 儿童
	* 格斗
	* 体育
	* 网游
###链接详情
	<a class="downtopc" href="/android/down.jsp?appid=49367&amp;pkgid=17002426&amp;icfa=15144052049367001000&amp;lmid=2031&amp;g_f=0&amp;actiondetail=0&amp;downtype=1&amp;transactionid=&amp;topicid=-1&amp;softname=" onclick="_gaq.push(['_trackPageview', '/virtual/insite/downapp/2031/detail/49367']);pingHotag('downapp.2031.detail.49367');" title="免费下载QQ浏览器5.0.0.650到电脑"><span class="hide-clip">免费下载QQ浏览器5.0.0.650到电脑</span></a>

##[91助手]
###介绍
91助手已经被百度收购，从而其本身拥有的应用通过百度应用都可以下载到
###应用数量
应用数量不确定
###链接详情
	'http://apk.91.com/soft/Controller.ashx?Action=Download&id=40250790&m=e02dc68aba90c7593de7eae52127179c'<br>

response header:location:

	http://dl1.91rb.com/4d9ccfa630d208b2f647dafca4fd0bdf/91sdkgame/PapaSG_1.6.0_91.apk
##[百度应用]（推荐抓取）
###介绍
通过百度在国内搜索第一的名头，大多数新手会通过百度去下载应用，同时百度的应用助手在手机上也占有很大的份额，加上收购91助手，百度在应用方面是很全面的
###应用数量
应用数量不确定


*	系统安全
*	壁纸美化
*	聊天通讯
*	生活实用
*	书籍阅读
*	影音图像
*	学习办公
*	网络社区
*	地图导航
*	理财购物
*	其他软件
*	游戏

	* 休闲益智
	* 角色冒险
	* 策略游戏
	* 飞行射击
	* 经营养成
	* 动作格斗
	* 体育竞速
	* 卡片棋牌
	* 其他游戏

###链接详情
应用地址：

	'http://as.baidu.com/a/item?docid=3116267
	http://gdown.baidu.com/data/wisegame/ac338107f5725110/ZooPuzzle2in1.apk'
##[机锋市场]
###介绍
机锋市场也是中国最早最大的Android市场之一，其主要用户是机锋论坛中的用户，通过首页的下载情况来看已经不是很流行了。
###应用数量
游戏：38776
应用：88227
###链接详情
应用下载地址<br>

	http://api.gfan.com/market/api/apk?type=APK&cid=99&uid=-1&pid=j/bfjbbJc2eKqqfJdILJnQ==&sid=PcWL3pLIP03H3B4YIbXu+g==
response header location:<br>

	http://cdn2.down.apk.gfan.com/asdf/Pfiles/2013/12/19/625446_6a527cb9-6947-4a02-80ba-d17e4ebb43a8.apk
##[360手机助手]
###介绍
通过首页上的下载排行，最高只为1805万次相比于其他应用市场要小很多，所以不建议抓取
###应用数量
应用数量不确定
###链接详情
	<a sid="5427" marketid="360market" href="zhushou360://type=apk&amp;name=微信&amp;url=http://shouji.360tpcdn.com/131112/6629285f3ba25409cbf570caafde49c5/com.tencent.mm_355.apk" class="dbtn normal js-downLog">一键安装</a>
##[智汇云应用市场]
###介绍
智汇云是华为官方售价应用下载平台，知道这个平台的主要为华为用户，如果客户为华为，可以进行抓取
###应用数量
应用数量不确定
###链接详情
	<a class="mkapp-btn mab-download" title="下载到电脑" href="javascript:void(0);" onclick="zhytools.downloadApp('SC10056988',
                        '魔法消灭', 
                        'appdetail_dl',
                        '15',
                        '休闲游戏' , 
                        'http://appdl.hicloud.com/dl/appdl/application/apk/00/002e84c3304c4a93b5237f5623c4226f/com.otrescs.perish.1308161753.apk?sign=portal@portal1387529954960&amp;source=portalsite' ,
                         '3.8.2');">
                     <b class="b-lt"></b><span><em class="flt pc"></em>下载到电脑</span><b class="b-rt"></b>
                 </a>
##[木蚂蚁应用市场]
###介绍
木蚂蚁应用市场，主要专注的应用的汉化，汉化一般是不会更改应用的package的，所以对于应用抓取影响不大，最近的市场份额也没有以前那个大了

###应用数量
游戏：1006
###链接详情
木蚂蚁应用链接格式<br>

	http://www.mumayi.com/android-459761.html<br>
	http://down.mumayi.com/459761
Location:

	http://apk.mumayi.com/2013/12/10/45/459761/zhangshangjijin_V2.7.0_mumayi_c48a0.apk
##[安卓市场]（推荐爬取）
###介绍
安卓市场是国内最早最大的安卓软件，通过搜索寻找一些安卓下载市场，其结果是也是十分靠前的，所以其拥有的用户群体是相对的很多的
###应用数量
应用数量不确定

*	浏览器
*	输入法
*	健康
*	效率
*	教育
*	理财
*	阅读
*	个性化
*	购物
*	资讯
*	生活
*	工具
*	出行
*	通讯
*	拍照
*	社交
*	影音
*	安全
*	游戏
	
	* 休闲
	* 棋牌
	* 益智
	* 射击
	* 体育
	* 儿童
	* 网游
	* 角色
	* 策略
	* 经营
	* 竞速
###链接详情
应用链接：

	http://apk.hiapk.com/Download.aspx?aid=2030781&rel=nofollow&module=4&info=
Cookie:

	bdshare_firstime=1387532344540; CNZZDATA30060492=cnzz_eid%3D1059252000-1387530812-%26ntime%3D1387530812%26cnzz_a%3D5%26ltime%3D1387530813462; CNZZDATA30033867=cnzz_eid%3D1219993882-1387530811-%26ntime%3D1387530811%26cnzz_a%3D7%26ltime%3D1387530813399; CNZZDATA3121686=cnzz_eid%3D1089718215-1387530812-%26ntime%3D1387530812%26cnzz_a%3D5%26ltime%3D1387530813805
Location:

	http://cdn.market.hiapk.com/data/upload/2013/11_27/20/com.familyroomgames.piratesvsninjasdeluxe_205007.apk
##[拇指玩]（推荐爬取）
###介绍
主要提供破解大型游戏，由于国内Google Play的限制，大部分精彩的游戏在中国是找不到的，所以拇指玩提供了大量破解版游戏，从而吸引了大量游戏玩家，同时也是在MAM上，需要重视的地方，毕竟大型游戏会影响到员工的工作质量。
###应用数量
应用数量不确定

*	休闲益智
*	动作射击
*	体育竞技
*	角色扮演
*	网络游戏
*	棋牌游戏
*	赛车竞速
*	策略塔防
*	模拟经营
###链接详情
	http://www.muzhiwan.com/index.php?action=common&opt=downloadstat&type=1&vid=94298&url=http://gslb.coop.letv.com//2013/12/20/com.ratrodstudio.skateparty252b402165fec3.gpk
##[应用汇]（推荐爬取）
###介绍
“应用汇”是国内唯一一家承诺对用户进行第三方赔付的Android应用商店。“AppChina应用汇”是一款基于Android系统的本土化应用商店，可以通过手机客户端，Web端、Wap端以及Pad版等多个途径使用，每月的应用下载量超过1亿。
###应用数量
“应用汇”现在提供超过4万款手机应用供Android手机用户免费下载

*	输入法
*	浏览器
*	动态壁纸
*	系统工具
*	便捷生活
*	影音播放
*	通话通讯
*	社交网络
*	主题插件
*	拍摄美化
*	新闻资讯
*	图书阅读
*	学习办公
*	网购支付
*	金融理财

###链接详情
	http://www.appchina.com/app/com.snda.wifilocating/
[小米商店]:http://app.xiaomi.com/
[天翼空间]:http://www.189store.com/soft.html
[移动应用商店]:http://mm.10086.cn/
[沃商店]:http://store.wo.com.cn/
[应用宝]:http://android.myapp.com/
[91助手]:http://apk.91.com/
[百度应用]:http://as.baidu.com/
[机锋市场]:http://apk.gfan.com/
[360手机助手]:http://zhushou.360.cn/
[智汇云应用市场]:http://app.vmall.com/
[木蚂蚁应用市场]:http://www.mumayi.com/
[安卓市场]:http://apk.hiapk.com/
[拇指玩]:http://www.muzhiwan.com/
[Google Play]:https://play.google.com/store
[应用汇]:http://www.appchina.com/
