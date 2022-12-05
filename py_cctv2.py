#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import json
import time
import base64

class Spider(Spider):  # 元类 默认的元类 type
	def getName(self):
		return "央视2"
	def init(self,extend=""):
		print("============{0}============".format(extend))
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		# https://meijuchong.cc/
		result = {}
		cateManual = {
"新闻1":"TOPC1451539822927345",#华人世界
"新闻2":"TOPC1451558926200436",#环球视线
"法治": "TOPC1451542672944335", #忏悔录
"经济": "TOPC1451531385787654", #天下财经
"科教1":"TOPC1451540268188575", #国宝档案
"科教2":"TOPC1451543426689237", #夜线
"农业1": "TOPC1568949310515140", #致富经
"农业2": "TOPC1563178829094125", #乡间纪事
"健康乡村纪实": "TOPC1451542933238628", #见证
"音乐1": "TOPC1451541994820527", #民歌·中国
"音乐2": "TOPC1451542222069826", #音乐传奇
"电影电视剧": "TOPC1451469943519994", #星推荐
"军事1": "TOPC1451527941788652", #军事报道
"军事2": "TOPC1575602995944674", #军事纪录
"动画":"TOPC1451542209144770", #动画城
"少儿": "TOPC1451559344361150", #大仓库
"生活": "TOPC1451541349400938", #远方的家
"综艺1": "TOPC1451541564922207", #中华情
"综艺2": "TOPC1451984301286720", #欢乐中国行
"体育1": "TOPC1451550970356385", #体坛快讯
"体育2": "TOPC1551324792732798", #ATP周刊
"戏曲": "TOPC1451558728003217" #影视剧场
		}
		classes = []
		for k in cateManual:
			classes.append({
				'type_name':k,
				'type_id':cateManual[k]
			})
		
		result['class'] = classes
		if(filter):
			result['filters'] = self.config['filter']
		return result
	def homeVideoContent(self):
		result = {
			'list':[]
		}
		return result
	def categoryContent(self,tid,pg,filter,extend):		

		result = {}
		# extend['id'] = tid
		extend['p'] = pg
		extend['sort']="desc"
		extend['mode']=0

		filterParams = ["id", "p", "d", "sort","mode"]
		params = ["", "", "", "",""]
		for idx in range(len(filterParams)):
			fp = filterParams[idx]
			if fp in extend.keys():
				params[idx] = '{0}={1}'.format(filterParams[idx],extend[fp])
		suffix = '&'.join(params)
		url = 'https://api.cntv.cn/NewVideo/getVideoListByColumn?{0}&n=20&sort=desc&mode=0&serviceId=tvcctv&t=json'.format(suffix)
		if not tid.startswith('TOPC'):
			url = 'https://api.cntv.cn/NewVideo/getVideoListByAlbumIdNew?{0}&n=20&sort=desc&mode=0&serviceId=tvcctv&t=json'.format(suffix)

		rsp = self.fetch(url,headers=self.header)
		jo = json.loads(rsp.text)
		vodList = jo['data']['list']
		videos = []
		for vod in vodList:
			guid = vod['guid']
			title = vod['title']
			img = vod['image']
			brief = vod['brief']
			videos.append({
				"vod_id":guid+"###"+img,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":''
			})
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = 9999
		result['limit'] = 90
		result['total'] = 999999
		return result

	def detailContent(self,array):
		aid = array[0].split('###')
		tid = aid[0]
		url = "https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid={0}".format(tid)

		rsp = self.fetch(url,headers=self.header)
		jo = json.loads(rsp.text)
		title = jo['title'].strip()
		link = jo['hls_url'].strip()
		vod = {
			"vod_id":tid,
			"vod_name":title,
			"vod_pic":aid[1],
			"type_name":'',
			"vod_year":"",
			"vod_area":"",
			"vod_remarks":"",
			"vod_actor":"",
			"vod_director":"",
			"vod_content":""
		}
		vod['vod_play_from'] = 'CCTV'
		vod['vod_play_url'] = title+"$"+link

		result = {
			'list':[
				vod
			]
		}
		return result
	def searchContent(self,key,quick):
		result = {
			'list':[]
		}
		return result
	def playerContent(self,flag,id,vipFlags):
		result = {}
		rsp = self.fetch(id,headers=self.header)
		content = rsp.text.strip()
		arr = content.split('\n')
		urlPrefix = self.regStr(id,'(http[s]?://[a-zA-z0-9.]+)/')
		url = urlPrefix + arr[-1]
		result["parse"] = 0
		result["playUrl"] = ''
		result["url"] = url
		result["header"] = ''
		return result

	config = {
		"player": {},
		# "filter": {"1": [{"key":"sub","name":"类别","value":[{"n":"海峡两岸","v":"TOPC1451540328102649"},{"n":"今日关注","v":"TOPC1451540389082713"}],{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2022", "v": "2022"}, {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}],"2": [{"key":"sub","name":"类别","value":[{"n":"天网","v":"TOPC1451543228296920"},{"n":"一线","v":"TOPC1451543462858283"}],{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2022", "v": "2022"}, {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}]}
		"filter": {"TOPC1451539822927345": [{"key":"id","name":"类别","value":[
{"n":"华人世界","v":"TOPC1451539822927345"},
{"n":"海峡两岸","v":"TOPC1451540328102649"},
{"n":"今日关注","v":"TOPC1451540389082713"},
{"n":"中国新闻","v":"TOPC1451539894330405"},
{"n":"今日亚洲","v":"TOPC1451540448405749"},
{"n":"朝闻天下","v":"TOPC1451558496100826"},
{"n":"新闻直播间","v":"TOPC1451559129520755"},
{"n":"新闻30分","v":"TOPC1451559097947700"},
{"n":"共同关注","v":"TOPC1451558858788377"},
{"n":"东方时空","v":"TOPC1451558532019883"},
{"n":"新闻1+1","v":"TOPC1451559066181661"},
{"n":"今日环球","v":"TOPC1571034705435323"},
{"n":"华人故事","v":"TOPC1571646754621556"}]},{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2022", "v": "2022"},  {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}],
		"TOPC1451558926200436": [{"key":"id","name":"类别","value":[{"n":"环球视线","v":"TOPC1451558926200436"},
{"n":"鲁健访谈","v":"TOPC1609904361007481"},
{"n":"深度国际","v":"TOPC1451540709098112"},
{"n":"国际时讯","v":"TOPC1451558887804404"},
{"n":"24小时","v":"TOPC1451558428005729"},
{"n":"午夜新闻","v":"TOPC1451558779639282"},
{"n":"新闻调查","v":"TOPC1451558819463311"},
{"n":"新闻周刊","v":"TOPC1451559180488841"},
{"n":"世界周刊","v":"TOPC1451558687534149"},
{"n":"面对面","v":"TOPC1451559038345600"},
{"n":"每周质量报告","v":"TOPC1451558650605123"},
{"n":"华人世界","v":"TOPC1451539822927345"}]},{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2022", "v": "2022"},  {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}],
	"TOPC1451542672944335": [{"key":"id","name":"类别","value":[{"n":"方圆剧阵","v":"TOPC1571217727564820"},
{"n":"天网","v":"TOPC1451543228296920"},
{"n":"生命线","v":"TOPC1571040589483598"},
{"n":"道德观察","v":"TOPC1451542784285432"},
{"n":"一线","v":"TOPC1451543462858283"},
{"n":"法治在线","v":"TOPC1451558590627940"},
{"n":"热线12","v":"TOPC1451543168050863"},
{"n":"从心开始","v":"TOPC1571217374070848"},
{"n":"现场","v":"TOPC1571301089686775"},
{"n":"小区大事","v":"TOPC1451543346581129"},
{"n":"法治深壹度","v":"TOPC1571535828826169"},
{"n":"忏悔录","v":"TOPC1451542672944335"}]},{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2022", "v": "2022"},  {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}],
	"TOPC1451531385787654": [{"key":"id","name":"类别","value":[{"n":"我有传家宝","v":"TOPC1451525396109388"},
{"n":"天下财经","v":"TOPC1451531385787654"},
{"n":"正点财经","v":"TOPC1453100395512779"},
{"n":"收藏传奇","v":"TOPC1451526640730841"},
{"n":"分秒必争","v":"TOPC1451379074008632"}]},{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2022", "v": "2022"},  {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}],
	"TOPC1451540268188575": [{"key":"id","name":"类别","value":[{"n":"天涯共此时","v":"TOPC1451540858793305"},
{"n":"国宝档案","v":"TOPC1451540268188575"},
{"n":"真相","v":"TOPC1503545711557359"},
{"n":"大家","v":"TOPC1451557371520714"},
{"n":"讲述","v":"TOPC1451557691081955"},
{"n":"人物","v":"TOPC1451557861628208"},
{"n":"动物世界","v":"TOPC1451378967257534"},
{"n":"人与自然","v":"TOPC1451525103989666"},
{"n":"中华民族","v":"TOPC1451525460925648"},
{"n":"国家记忆","v":"TOPC1473235107169415"},
{"n":"国宝·发现","v":"TOPC1571034869935436"},
{"n":"百家讲坛","v":"TOPC1451557052519584"},
{"n":"自然传奇","v":"TOPC1451558150787467"},
{"n":"探索·发现","v":"TOPC1451557893544236"},
{"n":"地理·中国","v":"TOPC1451557421544786"},
{"n":"外国人在中国","v":"TOPC1451541113743615"},
{"n":"文明之旅","v":"TOPC1451541205513705"},
{"n":"记住乡愁第六季","v":"TOPC1577672009520911"},
{"n":"跟着书本去旅行","v":"TOPC1575253587571324"},
{"n":"记住乡愁第七季","v":"TOPC1608533695279753"},
{"n":"时尚科技秀","v":"TOPC1570874587435537"},
{"n":"创新进行时","v":"TOPC1570875218228998"},
{"n":"解码科技史","v":"TOPC1570876640457386"},
{"n":"科学动物园","v":"TOPC1571021385508957"},
{"n":"考古公开课","v":"TOPC1571021251454875"},
{"n":"科幻地带","v":"TOPC1571021323137369"},
{"n":"实验现场","v":"TOPC1571021159595290"}]},{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2022", "v": "2022"},  {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}],
	"TOPC1451543426689237": [{"key":"id","name":"类别","value":[{"n":"人物·故事","v":"TOPC1570780618796536"},
{"n":"百家说故事","v":"TOPC1574995326079121"},
{"n":"透视新科技","v":"TOPC1576631973420833"},
{"n":"夕阳红","v":"TOPC1451543312252987"},
{"n":"心理访谈","v":"TOPC1451543382680164"},
{"n":"读书","v":"TOPC1451557523542854"},
{"n":"夜线","v":"TOPC1451543426689237"},
{"n":"我爱发明","v":"TOPC1569314345479107"},
{"n":"环球科技视野","v":"TOPC1451463780801881"},
{"n":"状元360","v":"TOPC1451528493821255"},
{"n":"1起聊聊","v":"TOPC1451374975347585"},
{"n":"秘境之眼","v":"TOPC1554187056533820"},
{"n":"文化视点","v":"TOPC1451536118642783"},
{"n":"文化正午","v":"TOPC1451538455169283"},
{"n":"文化大百科","v":"TOPC1451536035602751"},
{"n":"动物传奇","v":"TOPC1451984181884527"},
{"n":"文化讲坛","v":"TOPC1451984533334125"},
{"n":"流行无限","v":"TOPC1451540644606949"},
{"n":"天涯共此时","v":"TOPC1451540858793305"},
{"n":"中国影像方志","v":"TOPC1592552941644815"},
{"n":"创新无限","v":"TOPC1451557109280614"},
{"n":"科技人生","v":"TOPC1451557739596986"},
{"n":"绿色空间","v":"TOPC1451557825546179"},
{"n":"重访","v":"TOPC1451558118808439"},
{"n":"走近科学","v":"TOPC1451558190239536"},
{"n":"原来如此","v":"TOPC1451558088858410"},
{"n":"科技之光","v":"TOPC1451557776198149"},
{"n":"文明密码","v":"TOPC1451557930785264"},
{"n":"我爱发明（科普）","v":"TOPC1451557970755294"}]},{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2022", "v": "2022"},  {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}],
	"TOPC1568949310515140": [{"key":"id","name":"类别","value":[{"n":"致富经","v":"TOPC1568949310515140"},
{"n":"三农群英汇","v":"TOPC1600745974233265"},
{"n":"田间示范秀","v":"TOPC1563178908227191"},
{"n":"农业气象","v":"TOPC1568949200635957"},
{"n":"中国三农报道","v":"TOPC1600746045741952"},
{"n":"大地讲堂","v":"TOPC1568966472372643"},
{"n":"乡土中国","v":"TOPC1563178586782832"},
{"n":"振兴路上","v":"TOPC1632709936747979"},
{"n":"谁知盘中餐","v":"TOPC1568966325430648"},
{"n":"田野里的歌声","v":"TOPC1632628323813790"},
{"n":"乡理乡亲","v":"TOPC1568966155566515"}]},{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2022", "v": "2022"},  {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}],
	"TOPC1563178829094125": [{"key":"id","name":"类别","value":[{"n":"我的美丽乡村","v":"TOPC1570787364956444"},
{"n":"攻坚日记","v":"TOPC1568966013656550"},
{"n":"地球村日记","v":"TOPC1568966232265609"},
{"n":"乡约","v":"TOPC1568949394517190"},
{"n":"乡村剧场","v":"TOPC1563179005948252"},
{"n":"乡村振兴面对面","v":"TOPC1568966531726705"},
{"n":"乡间纪事","v":"TOPC1563178829094125"},
{"n":"超级新农人","v":"TOPC1597627647957699"},
{"n":"科技链","v":"TOPC1563178120425659"},
{"n":"乡村振兴资讯","v":"TOPC1568965444563295"},
{"n":"遍地英雄","v":"TOPC1568966086614400"}]},{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2022", "v": "2022"},  {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}],
	"TOPC1451542933238628": [{"key":"id","name":"类别","value":[{"n":"健康之路","v":"TOPC1451557646802924"},
{"n":"中华医药","v":"TOPC1451541666791291"},
{"n":"乡村大舞台","v":"TOPC1563179546003162"},
{"n":"记住乡愁第八季","v":"TOPC1640330887412898"},
{"n":"印象·乡村","v":"TOPC1563178734372977"},
{"n":"中国缘","v":"TOPC1571646819318596"},
{"n":"见证","v":"TOPC1451542933238628"}]},{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2022", "v": "2022"},  {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}],
	"TOPC1451541994820527": [{"key":"id","name":"类别","value":[{"n":"乐享汇","v":"TOPC1528430065133683"},
{"n":"国际艺苑","v":"TOPC1451379250581117"},
{"n":"中国音乐电视","v":"TOPC1451542397206110"},
{"n":"精彩音乐汇","v":"TOPC1451541414450906"},
{"n":"童声唱","v":"TOPC1570593464032566"},
{"n":"民歌·中国","v":"TOPC1451541994820527"},
{"n":"CCTV音乐厅","v":"TOPC1451534421925242"},
{"n":"影视留声机","v":"TOPC1451542346007956"},
{"n":"音乐人生","v":"TOPC1451542308412911"},
{"n":"一起音乐吧","v":"TOPC1451542132455743"},
{"n":"音乐公开课","v":"TOPC1462849800640766"},
{"n":"乐游天下","v":"TOPC1451541538046196"}]},{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2022", "v": "2022"},  {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}],
	"TOPC1451542222069826": [{"key":"id","name":"类别","value":[{"n":"中国节拍","v":"TOPC1570025984977611"},
{"n":"聆听时刻","v":"TOPC1570026397101703"},
{"n":"音乐周刊","v":"TOPC1570593186033488"},
{"n":"合唱先锋","v":"TOPC1570026172793162"},
{"n":"巅峰音乐汇","v":"TOPC1451984095463376"},
{"n":"曲苑杂坛","v":"TOPC1451984417763860"},
{"n":"星光舞台","v":"TOPC1451542099519708"},
{"n":"百年歌声","v":"TOPC1451534465694290"},
{"n":"音乐传奇","v":"TOPC1451542222069826"},
{"n":"音乐告诉你","v":"TOPC1451542273313866"},
{"n":"广场舞金曲","v":"TOPC1528685010104859"},
{"n":"快乐琴童","v":"TOPC1451541450128978"},
{"n":"歌声与微笑","v":"TOPC1451541189657627"},
{"n":"今乐坛","v":"TOPC1451541229451689"}]},{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2022", "v": "2022"},  {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}],
	"TOPC1451469943519994": [{"key":"id","name":"类别","value":[{"n":"中国电影报道","v":"TOPC1451354597100320"},
{"n":"星推荐","v":"TOPC1451469943519994"},
{"n":"剧说很好看","v":"TOPC1495184612807684"},
{"n":"今日影评","v":"TOPC1470713254980521"},
{"n":"世界电影之旅","v":"TOPC1451560112462173"},
{"n":"影视俱乐部","v":"TOPC1451469901250966"},
{"n":"影视同期声","v":"TOPC1451469804671799"},
{"n":"影视名堂","v":"TOPC1451558049329358"},
{"n":"第10放映室","v":"TOPC1451557487468814"}]},{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2022", "v": "2022"},  {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}],
	"TOPC1451527941788652": [{"key":"id","name":"类别","value":[{"n":"国防军事早报","v":"TOPC1564109128610932"},
{"n":"正午国防军事","v":"TOPC1564109254301161"},
{"n":"军事报道","v":"TOPC1451527941788652"},
{"n":"防务新观察","v":"TOPC1451526164984187"},
{"n":"军迷行天下","v":"TOPC1564131644145429"},
{"n":"老兵你好","v":"TOPC1564109722559395"},
{"n":"军武零距离","v":"TOPC1564109434999268"},
{"n":"军事制高点","v":"TOPC1564109356650207"},
{"n":"军事科技","v":"TOPC1451528087494889"},
{"n":"军事纪实","v":"TOPC1451527993718730"},
{"n":"谁是终极英雄","v":"TOPC1451530272783201"},
{"n":"军营的味道","v":"TOPC1564110136027687"}]},{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2022", "v": "2022"},  {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}],
	"TOPC1575602995944674": [{"key":"id","name":"类别","value":[{"n":"砺剑","v":"TOPC1649983616689859"},
{"n":"军事纪录","v":"TOPC1575602995944674"},
{"n":"国防故事","v":"TOPC1578551434601482"},
{"n":"兵器面面观","v":"TOPC1564110696628209"},
{"n":"第二战场","v":"TOPC1564110615253124"},
{"n":"世界战史","v":"TOPC1564110396694880"},
{"n":"五星剧场","v":"TOPC1564110834985329"},
{"n":"国防微视频-军歌嘹亮","v":"TOPC1564110222559767"},
{"n":"军情时间到","v":"TOPC1462504102545692"},
{"n":"国防科工","v":"TOPC1564109813378483"}]},{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2022", "v": "2022"},  {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}],
	"TOPC1451541349400938": [{"key":"id","name":"类别","value":[{"n":"走遍中国","v":"TOPC1451542134053698"},
{"n":"生活提示","v":"TOPC1451526037568184"},
{"n":"人口","v":"TOPC1451466072378425"},
{"n":"生活圈","v":"TOPC1451546588784893"},
{"n":"是真的吗","v":"TOPC1451534366388377"},
{"n":"生活家","v":"TOPC1593419181674791"},
{"n":"远方的家","v":"TOPC1451541349400938"},
{"n":"美食中国","v":"TOPC1571034804976375"},
{"n":"味道","v":"TOPC1482483166133803"},
{"n":"生活早参考","v":"TOPC1451525302140236"},
{"n":"走遍中国","v":"TOPC1451542134053698"}]},{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2022", "v": "2022"},  {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}],
	"TOPC1451542209144770": [{"key":"id","name":"类别","value":[{"n":"动画城","v":"TOPC1451542209144770"},
{"n":"动漫世界","v":"TOPC1451559448233349"},
{"n":"周末动画片","v":"TOPC1451559836238828"},
{"n":"快乐驿站","v":"TOPC1451542273075862"},
{"n":"动画城","v":"TOPC1451542209144770"},
{"n":"动漫星空","v":"TOPC1451559936284927"},
{"n":"动画剧场","v":"TOPC1451559414465320"}]},{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2022", "v": "2022"},  {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}],
	"TOPC1451559344361150": [{"key":"id","name":"类别","value":[{"n":"新闻袋袋裤","v":"TOPC1451559603261584"},
{"n":"英雄出少年","v":"TOPC1451559695702690"},
{"n":"七巧板","v":"TOPC1451559569040502"},
{"n":"快乐体验","v":"TOPC1451559479171411"},
{"n":"智力快车","v":"TOPC1451559756374759"},
{"n":"动感特区","v":"TOPC1451559378830189"},
{"n":"音乐快递","v":"TOPC1451559666055645"},
{"n":"SK极智少年强","v":"TOPC1476950587121943"},
{"n":"加油！少年派","v":"TOPC1451464548229761"},
{"n":"风车剧场","v":"TOPC1573528152700717"},
{"n":"希望-英语杂志","v":"TOPC1451558013229330"},
{"n":"成长在线","v":"TOPC1451559901017891"},
{"n":"童心回放","v":"TOPC1451559966897957"},
{"n":"文学宝库","v":"TOPC1451560002205989"},
{"n":"大仓库","v":"TOPC1451559344361150"},
{"n":"宝贝一家亲","v":"TOPC1451559867985861"},
{"n":"绿野寻踪","v":"TOPC1451559534065469"},
{"n":"芝麻开门","v":"TOPC1451559725520729"},
{"n":"异想天开","v":"TOPC1451559633994614"}]},{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2022", "v": "2022"},  {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}],
	"TOPC1451541564922207": [{"key":"id","name":"类别","value":[{"n":"中华情","v":"TOPC1451541564922207"},
{"n":"回声嘹亮","v":"TOPC1451535575561597"},
{"n":"你好生活第三季","v":"TOPC1627961377879898"},
{"n":"我的艺术清单","v":"TOPC1582272259917160"},
{"n":"黄金100秒","v":"TOPC1451468496522494"},
{"n":"非常6+1","v":"TOPC1451467940101208"},
{"n":"向幸福出发","v":"TOPC1451984638791216"},
{"n":"幸福账单","v":"TOPC1451984801613379"},
{"n":"中国文艺报道","v":"TOPC1601348042760302"},
{"n":"舞蹈世界","v":"TOPC1451547605511387"},
{"n":"艺览天下","v":"TOPC1451984851125433"},
{"n":"天天把歌唱","v":"TOPC1451535663610626"},
{"n":"金牌喜剧班","v":"TOPC1611826337610628"},
{"n":"环球综艺秀","v":"TOPC1571300682556971"},
{"n":"挑战不可能第五季","v":"TOPC1579169060379297"},
{"n":"我们有一套","v":"TOPC1451527089955940"},
{"n":"为了你","v":"TOPC1451527001597710"},
{"n":"朗读者第一季","v":"TOPC1487120479377477"},
{"n":"挑战不可能第二季","v":"TOPC1474277421637816"}]},{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2022", "v": "2022"},  {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}],
	"TOPC1451984301286720": [{"key":"id","name":"类别","value":[{"n":"精彩一刻","v":"TOPC1451464786232149"},
{"n":"挑战不可能之加油中国","v":"TOPC1547519813971570"},
{"n":"挑战不可能第一季","v":"TOPC1452063816677656"},
{"n":"机智过人第三季","v":"TOPC1564019920570762"},
{"n":"经典咏流传第二季","v":"TOPC1547521714115947"},
{"n":"挑战不可能第三季","v":"TOPC1509500865106312"},
{"n":"经典咏流传第一季","v":"TOPC1513676755770201"},
{"n":"欢乐中国人第二季","v":"TOPC1516784350726581"},
{"n":"故事里的中国第一季","v":"TOPC1569729252342702"},
{"n":"你好生活第二季","v":"TOPC1604397385056621"},
{"n":"喜上加喜","v":"TOPC1590026042145705"},
{"n":"走在回家的路上","v":"TOPC1577697653272281"},
{"n":"综艺盛典","v":"TOPC1451985071887935"},
{"n":"艺术人生","v":"TOPC1451984891490556"},
{"n":"全家好拍档","v":"TOPC1474275463547690"},
{"n":"大魔术师","v":"TOPC1451984047073332"},
{"n":"欢乐一家亲","v":"TOPC1451984214170587"},
{"n":"开心辞典","v":"TOPC1451984378754815"},
{"n":"综艺星天地","v":"TOPC1451985188986150"},
{"n":"激情广场","v":"TOPC1451984341218765"},
{"n":"笑星大联盟","v":"TOPC1451984731428297"},
{"n":"天天乐","v":"TOPC1451984447718918"},
{"n":"欢乐英雄","v":"TOPC1451984242834620"},
{"n":"欢乐中国行","v":"TOPC1451984301286720"},
{"n":"我爱满堂彩","v":"TOPC1451538709371329"},
{"n":"综艺头条","v":"TOPC1569226855085860"},
{"n":"魔法奇迹","v":"TOPC1451542029126607"}]},{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2022", "v": "2022"},  {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}],
	"TOPC1451550970356385": [{"key":"id","name":"类别","value":[{"n":"运动大不同","v":"TOPC1451552002869953"},
{"n":"天下足球","v":"TOPC1451551777876756"},
{"n":"篮球公园","v":"TOPC1451549958391444"},
{"n":"体育新闻","v":"TOPC1451551426170389"},
{"n":"足球之夜","v":"TOPC1451552481492403"},
{"n":"北京2022","v":"TOPC1462860742367700"},
{"n":"体坛快讯","v":"TOPC1451550970356385"},
{"n":"体育世界","v":"TOPC1451551371554333"},
{"n":"欧冠开场哨","v":"TOPC1451550484638864"},
{"n":"棋牌乐","v":"TOPC1451550531682936"},
{"n":"健身动起来","v":"TOPC1451549599140203"},
{"n":"体育晨报","v":"TOPC1451551258388672"},
{"n":"体谈","v":"TOPC1451551830518827"}]},{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2022", "v": "2022"},  {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}],
	"TOPC1551324792732798": [{"key":"id","name":"类别","value":[{"n":"ATP周刊","v":"TOPC1551324792732798"},
{"n":"冰球冰球","v":"TOPC1551323337921620"},
{"n":"冰天雪地","v":"TOPC1551323403033398"},
{"n":"约战果岭","v":"TOPC1551324843068553"},
{"n":"艺术里的奥林匹克","v":"TOPC1634807797280923"},
{"n":"逐冰追雪","v":"TOPC1634807873035403"},
{"n":"五环纪事","v":"TOPC1634807936107991"},
{"n":"奥秘无穷","v":"TOPC1634808174904190"},
{"n":"奥林匹克人","v":"TOPC1634808300961576"},
{"n":"体育在线","v":"TOPC1451540777295250"},
{"n":"运动大不同","v":"TOPC1451552002869953"},
{"n":"NBA最前线","v":"TOPC1451548615930237"},
{"n":"冠军欧洲","v":"TOPC1451549411228903"},
{"n":"巅峰时刻","v":"TOPC1451549547540149"},
{"n":"赛车时代","v":"TOPC1451550589995997"},
{"n":"体育人间","v":"TOPC1451551310742737"},
{"n":"武林大会","v":"TOPC1451551891055866"},
{"n":"谁是球王","v":"TOPC1451550868295303"}]},{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2022", "v": "2022"},  {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}],
	"TOPC1451558728003217": [{"key":"id","name":"类别","value":[{"n":"角儿来了","v":"TOPC1508747509633692"},
{"n":"梨园闯关我挂帅","v":"TOPC1451558484007800"},
{"n":"CCTV空中剧院","v":"TOPC1451558856402351"},
{"n":"过把瘾","v":"TOPC1451558291260577"},
{"n":"名段欣赏","v":"TOPC1451558515719854"},
{"n":"名家书场","v":"TOPC1579401761622774"},
{"n":"宝贝亮相吧","v":"TOPC1579401989187953"},
{"n":"中国京剧音配像精粹","v":"TOPC1451558769767256"},
{"n":"九州大戏台","v":"TOPC1451558399948678"},
{"n":"青春戏苑","v":"TOPC1451558552047910"},
{"n":"戏曲青年说","v":"TOPC1626161016006801"},
{"n":"了不起的戏曲","v":"TOPC1657505173323752"},
{"n":"梨园周刊","v":"TOPC1574909786070351"},
{"n":"中国京剧像音像集萃","v":"TOPC1626832834318986"},
{"n":"典藏","v":"TOPC1597825254395109"},
{"n":"快乐戏园","v":"TOPC1451558438767762"},
{"n":"锦绣梨园","v":"TOPC1451558328292617"},
{"n":"影视剧场","v":"TOPC1451558728003217"},
{"n":"戏苑百家","v":"TOPC1451558644535996"},
{"n":"跟我学","v":"TOPC1451558178940505"},
{"n":"戏曲采风","v":"TOPC1451558610462968"}]},{"key": "d", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2022", "v": "2022"},  {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"}, {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}]}]

	
	
	
	}

	}
	header = {
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"
	}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]