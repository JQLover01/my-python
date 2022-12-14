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
		return "哔哩"
	def init(self,extend=""):
		print("============{0}============".format(extend))
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
   "综合": "综合",
   "热门": "热门",
   "游戏赛事": "游戏赛事",
   "英雄联盟": "英雄联盟",
   "番剧": "番剧",
   "国创": "国创",
   "放映厅": "放映厅",
   "电影": "电影",
   "电视剧": "电视剧",
   "综艺": "综艺",
   "影视": "影视",
   "动画": "动画",
   "吾爱测评": "吾爱测评",
   "小剧场": "小剧场",
   "音乐": "音乐",
   "新歌热榜": "新歌热榜",
   "粤语": "粤语",
   "2022年热榜": "2022年热榜",
   "经典老歌": "经典老歌",
   "娱乐": "娱乐",
   "鬼畜": "鬼畜",
   "课堂": "课堂",
   "校园学习": "校园学习",
   "体育": "体育",
   "科技": "科技",
   "数码": "数码",
   "计算机技术": "计算机技术",
   "MT管理器": "MT管理器",
   "网盘挂载": "网盘挂载",
   "alist+WebDav": "alist+WebDav",
   "python": "python",
   "c++": "c++",
   "java": "java",
   "极客DIY": "极客DIY",
"Zard": "Zard",
"美女": "美女",
"宇宙": "宇宙",
"天文": "天文",
"飞碟探索": "飞碟探索",
"BBC记录": "BBC记录",
"Discovery": "Discovery",
"地理": "地理",
"历史": "历史",
"纪实": "纪实",
"人文": "人文",
"考古": "考古",
"自然": "自然",
"航拍": "航拍",
"昆虫": "昆虫",
"动物世界": "动物世界",
"荒野求生": "荒野求生",
"大灾难": "大灾难",
"纪录片": "纪录片",
"皮划艇": "皮划艇",
"冲浪": "冲浪",
"赶海": "赶海",
"钓鱼": "钓鱼",
"户外": "户外",
"斗牛": "斗牛",
"摔角": "摔角",
"武林风": "武林风",
"太极": "太极",
"美食": "美食",
"旅游": "旅游",
"相声小品": "相声小品",
"赵本山": "赵本山",
"宋小宝": "宋小宝",
"文松": "文松",
"戏曲": "戏曲",
"搞笑": "搞笑",
"快板": "快板",
"评书": "评书",
"广场舞": "广场舞",
"mtv": "mtv",
"健身": "健身",
"DJ热播": "DJ热播",
"演唱会": "演唱会",
"张帝": "张帝",
"张行": "张行",
"刘文正": "刘文正",
"张蔷": "张蔷",
"吴涤清": "吴涤清",
"刀郎": "刀郎",
"陈淑桦": "陈淑桦",
"足球": "足球",
"篮球": "篮球",
"排球": "排球",
"乒乓球": "乒乓球",
"曲棍球": "曲棍球",
"橄榄球": "橄榄球",
"高尔夫": "高尔夫",
"台球": "台球",
"斯诺克": "斯诺克",
"畜牧": "畜牧",
"养殖": "养殖",
"水产": "水产",
			"假窗-白噪音": "窗+白噪音"
			
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
	cookies = ''
	def getCookie(self):
		rsp = self.fetch("https://www.bilibili.com/")
		self.cookies = rsp.cookies
		return rsp.cookies
	def categoryContent(self,tid,pg,filter,extend):		
		result = {}
		url = 'https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={0}&duration=4&page={1}'.format(tid,pg)
		if len(self.cookies) <= 0:
			self.getCookie()
		rsp = self.fetch(url,cookies=self.cookies)
		content = rsp.text
		jo = json.loads(content)
		if jo['code'] != 0:			
			rspRetry = self.fetch(url,cookies=self.getCookie())
			content = rspRetry.text		
		jo = json.loads(content)
		videos = []
		vodList = jo['data']['result']
		for vod in vodList:
			aid = str(vod['aid']).strip()
			title = vod['title'].strip().replace("<em class=\"keyword\">","").replace("</em>","")
			img = 'https:' + vod['pic'].strip()
			remark = str(vod['duration']).strip()
			videos.append({
				"vod_id":aid,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":remark
			})
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = 9999
		result['limit'] = 90
		result['total'] = 999999
		return result
	def cleanSpace(self,str):
		return str.replace('\n','').replace('\t','').replace('\r','').replace(' ','')
	def detailContent(self,array):
		aid = array[0]
		url = "https://api.bilibili.com/x/web-interface/view?aid={0}".format(aid)

		rsp = self.fetch(url,headers=self.header)
		jRoot = json.loads(rsp.text)
		jo = jRoot['data']
		title = jo['title'].replace("<em class=\"keyword\">","").replace("</em>","")
		pic = jo['pic']
		desc = jo['desc']
		typeName = jo['tname']
		vod = {
			"vod_id":aid,
			"vod_name":title,
			"vod_pic":pic,
			"type_name":typeName,
			"vod_year":"",
			"vod_area":"",
			"vod_remarks":"",
			"vod_actor":"",
			"vod_director":"",
			"vod_content":desc
		}
		ja = jo['pages']
		playUrl = ''
		for tmpJo in ja:
			cid = tmpJo['cid']
			part = tmpJo['part']
			playUrl = playUrl + '{0}${1}_{2}#'.format(part,aid,cid)

		vod['vod_play_from'] = 'B站'
		vod['vod_play_url'] = playUrl

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

		ids = id.split("_")
		url = 'https://api.bilibili.com:443/x/player/playurl?avid={0}&cid=%20%20{1}&qn=112'.format(ids[0],ids[1])
		rsp = self.fetch(url)
		jRoot = json.loads(rsp.text)
		jo = jRoot['data']
		ja = jo['durl']
		
		maxSize = -1
		position = -1
		for i in range(len(ja)):
			tmpJo = ja[i]
			if maxSize < int(tmpJo['size']):
				maxSize = int(tmpJo['size'])
				position = i

		url = ''
		if len(ja) > 0:
			if position == -1:
				position = 0
			url = ja[position]['url']

		result["parse"] = 0
		result["playUrl"] = ''
		result["url"] = url
		result["header"] = {
			"Referer":"https://www.bilibili.com",
			"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
		}
		result["contentType"] = 'video/x-flv'
		return result

	config = {
		"player": {},
		"filter": {}
	}
	header = {}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]
