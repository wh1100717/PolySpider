#Pipeline流程
##1、CategorizingPipeline （分类初始化）
*	判断传入的item是否为空如果为空抛弃该item
*	通过CategoryUtil.get_category_id_by_name初始化category
	*	通过传入的category_name，在CATEGORY_ID中查找，如果没有该分类，先在un_record_category.txt获取其中的内容进行对比，如果已经有这个缺省分类记录，则不作处理，否则在un_record_category.txt中添加该分类名称，便于下次在CATEGORY_ID添加该分类，然后通过CATEGORY_ID.get(category_name)返回分类值
*	初始化<br>
	*	item['DROP_APP'] = False  是否抛弃item<br>
	*	item['NEW_APP'] = False  是否为新App<br>
	*	item['UPDATE_APP'] = False  是否需要更新App<br>

<img src="http://wh1100717.github.io/PolySpider/images/flowchart/CategorizingPipeline.jpg"  alt="">
##2、CheckAppPipeline （检查app相关内容）
*	通过AppDao.get_app_by_app_name()判断是否存在该app，如果不存在返回None，如果存在返回app数据
	*	如果app为空，生成item['category']，并通过AppDao.insert_app()向'app::data'中添加数据，同时在'app::category'和'app::index'中添加该应用id并对item['NEW_APP']赋值为True
	*	如果app不为空，item['UPDATE_APP']赋值为True
*	判断如果从'app::data'中获取到的author为空，而抓取到的item['author']不为空，则执行AppDao.update_app_author()更新app_author
*	判断如果从'app::data'中获取到的package_name为空，而抓取到的item['package_name']不为空，则执行AppDao.update_app_packagename()更新package_name

<img src="http://wh1100717.github.io/PolySpider/images/flowchart/CheckAppPipeline.jpg"  alt="">
##3、CheckAppDetailsPipeline（检查app详细内容）
*	通过AppDao.get_app_detail_by_app_name方法获取app_detail_list的详细信息
	*	如果app_detail_list为None，item['DROP_APP']赋值为True，返回item
	*	对app_detail_list里的app_detail做判断，如果版本和平台都已经存在，item['DROP_APP']赋值为True，返回item。如果不存在通过 AppDao.insert_app_detail向'app::data'添加数据
	

<img src="http://wh1100717.github.io/PolySpider/images/flowchart/CheckAppDetailsPipeline.jpg"  alt="">
##4、UpdateCategoryPipeline（更新app::data中的category项）
*	如果item['DROP_APP']为True，丢弃该item
*	如果item['UPDATE_APP']为True，对category进行重新计算
*	通过category_reorder对该应用分类排序，按照命中分类次数由高到低排序
*	通过AppDao.update_app_category()更新分类

<img src="http://wh1100717.github.io/PolySpider/images/flowchart/UpdateCategoryPipeline.jpg"  alt="">
##5、StatusRecordPipeline（更新status记录）
*	通过StatusDao.status_incr对item['platform']下的crawled加1
*	如果item['NEW_APP']为True通过StatusDao.status_incr对item['platform']下的new加1
*	如果item['UPDATE_APP']为True通过StatusDao.status_incr对item['platform']下的update加1
<img src="http://wh1100717.github.io/PolySpider/images/flowchart/StatusRecordPipeline.jpg"  alt="">