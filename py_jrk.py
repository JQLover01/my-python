#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import json

class Spider(Spider):
	def getName(self):
		return "体育直播"
	def init(self,extend=""):
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			"全部": "all"
		}
		classes = []
		for k in cateManual:
			classes.append({
				'type_name': k,
				'type_id': cateManual[k]
			})

		result['class'] = classes
		if (filter):
			result['filters'] = self.config['filter']
		return result
	def homeVideoContent(self):
		result = {}
		return result
	header = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
		"referer": "http://www.jrskan.com/"
	}

	def categoryContent(self,tid,pg,filter,extend):
		result = {}
		url = 'http://www.jrskan.com/'
		rsp = self.fetch(url,headers=self.header)
		root = self.html(rsp.text)
		aList = root.xpath("//div[contains(@class,'loc_match_list')]/div[contains(@class,'loc_match')]/div[@class='sub_list']/ul")
		videos = []
		for a in aList:
			area = a.xpath("./li[@class='lab_events']/span/text()")[0]
			time = a.xpath("./li[@class='lab_time']/text()")[0]
			home = a.xpath("./li[@class='lab_team_home']/strong/text()")[0]
			away = a.xpath("./li[@class='lab_team_away']/strong/text()")[0]
			img = a.xpath("./li[@class='lab_team_home']/span/img/@src")[0]
			aid = a.xpath("./li[@class='lab_channel']/a/@href")[0]
			title = home + 'vs' + away
			remark = area + '/' + time
			videos.append({
				"vod_id": aid,
				"vod_name": title,
				"vod_pic": img,
				"vod_remarks": remark
			})
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = 9999
		result['limit'] = 90
		result['total'] = 999999
		return result

	def detailContent(self,array):
		aid = array[0]
		url = aid
		rsp = self.fetch(url,headers=self.header)
		if rsp.status_code == 200:
			root = self.html(rsp.text)
			divContent = root.xpath("//div[@class='sub_head loc_match']/div[@class='sub_list']/ul")[0]
			area = divContent.xpath("./li[@class='lab_events']/span/text()")[0]
			time = divContent.xpath("./li[@class='lab_time']/text()")[0]
			home = divContent.xpath("./li[@class='lab_team_home']/strong/text()")[0]
			away = divContent.xpath("./li[@class='lab_team_away']/strong/text()")[0]
			img = divContent.xpath("./li[@class='lab_team_home']/span/img/@src")[0]
			title = home + 'vs' + away
			remark = area + '/' + time
			vod_play_url = '$$$'
			vod_play_from = '直播'
			playList = []
			vodItems = []
			pfList = root.xpath("//div[@class='sub_playlist']/div[@class='sub_channel']/a")
			for pf in pfList:
				pd = str(pf.xpath(".//@data-play")[0])
				if 'pao.php' in pd or 'i_up.html' in pd or 'i11.html' in pd or 'i22.html' in pd or '=&id2=' in pd:
					continue
				else:
					name = pf.xpath(".//strong/text()")[0]
					url = pd
				vodItems.append(name + "$" + url)
			joinStr = '#'
			joinStr = joinStr.join(vodItems)
			playList.append(joinStr)
			vod_play_url = vod_play_url.join(playList)
		else:
			return {}
		vod = {
			"vod_id": aid,
			"vod_name": title,
			"vod_pic": img,
			"type_name": area,
			"vod_year": "",
			"vod_area": area,
			"vod_remarks": remark,
			"vod_actor": '',
			"vod_director": '',
			'vod_play_from': vod_play_from,
			'vod_play_url': vod_play_url,
			"vod_content": ''
		}

		result = {
			'list': [
				vod
			]
		}
		return result
	def searchContent(self,key,quick):
		result = {}
		return result
	def playerContent(self,flag,id,vipFlags):
		result = {}
		ids = id.split('?')[1].split('&')
		nid1 = ids[0].split('=')[1]
		nid2 = ids[1].split('=')[1]
		if 'sm.html' in id:
			url = 'http://play.sportsteam365.com/play/{0}.html'.format(nid1)
			pat = 'iframe src=\\"(.*?)\\"'
		elif 'wlive.php' in id:
			url = 'http://play.sportsteam365.com{0}'.format(id)
			pat = "iframe width=\\'100%\\' height=\\'100%\\' src=\\'(.*?)\\'"
		elif 'i22.html' in id:
			url = 'http://play.sportsteam365.com/p/zkc_54_j.php?id={0}&id2={1}'.format(nid1,nid2)
			pat = "iframe width=\\'100%\\' height=\\'100%\\' src=\\'(.*?)\\'"
		elif 'i11.html' in id:
			url = 'http://play.sportsteam365.com/p/zkc_54_j.php?id={0}&id2={1}'.format(nid1,nid2)
			pat = "iframe width=\\'100%\\' height=\\'100%\\' src=\\'(.*?)\\'"
		rsp = self.fetch(url)
		if rsp.status_code == 200:
			html = self.cleanText(rsp.text)
			content = self.regStr(html, pat)
			purl = content.split('id=')[1]
		else:
			purl = ''
		result["parse"] = 0
		result["playUrl"] = ''
		result["url"] = purl
		result["header"] = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}

		return result

	config = {
		"player": {},
		"filter": {}
	}
	header = {}

	config = {
		"player": {},
		"filter": {}
	}
	header = {}
	def localProxy(self,param):
		action = {
			'url':'',
			'header':'',
			'param':'',
			'type':'string',
			'after':''
		}
		return [200, "video/MP2T", action, ""]