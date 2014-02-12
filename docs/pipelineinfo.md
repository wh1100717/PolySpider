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
*	通过SqliteUtil.checkTableExist()判断是否存在数据库，如果没有创建数据库
*	通过item['app_name']在ps_app表中利用App.get_app_by_app_name(app_name)方法查找app
	*	如果app为空，生成item['category']，并通过App.insert_app()向ps_app表中添加数据，并对item['NEW_APP']赋值为True
	*	如果app不为空，item['UPDATE_APP']赋值为True
*	判断如果从ps_app中获取到的author为空，而抓取到的item['author']不为空，则执行App.update_app_author()更新app_author

<img src="http://wh1100717.github.io/PolySpider/images/flowchart/CheckAppPipeline.jpg"  alt="">
##3、CheckAppDetailsPipeline（检查app详细内容）
*	通过AppDetail.get_app_detail_by_item()方法获取app的详细信息
	*	如果没有app详细信息，先执行apk_operation()方法,通过item['apk_url']对app下载，分析，获取item['package_name']，并且上传到云终端，然后AppDetail.insert_app_detail()方法添加app的详细信息
	*	如果有app的详细信息，item['DROP_APP']赋值为True

<img src="http://wh1100717.github.io/PolySpider/images/flowchart/CheckAppDetailsPipeline.jpg"  alt="">
##4、UpdateCategoryPipeline（更新ps_app中的category项）
*	如果item['DROP_APP']为True，丢弃该item
*	如果item['UPDATE_APP']为True，对category进行重新计算
*	通过category_reorder对该应用分类排序，按照命中分类次数由高到低排序
*	通过App.update_app_category()更新分类

<img src="http://wh1100717.github.io/PolySpider/images/flowchart/UpdateCategoryPipeline.jpg"  alt="">
##5、StatusRecordPipeline（更新ps_status记录）
*	通过Status.get_today_status()获取当日该平台应用抓取数量
	*	如果有记录返回记录status
	*	如果没有记录，向ps_status表中添加当日时间和平台的记录，并将status返回
*	如果item['NEW_APP']为True对记录中的new_app加1
*	如果item['UPDATE_APP']为True对记录中的update_app加1
*	通过Status.update_status()对ps_status进行更新

<img src="http://wh1100717.github.io/PolySpider/images/flowchart/StatusRecordPipeline.jpg"  alt="">