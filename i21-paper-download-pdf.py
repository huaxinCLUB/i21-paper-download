#!/usr/bin/python3.8
import requests
from lxml import etree
import time
from datetime import datetime


#获取最新报纸期数
def get_newest_num(url):

	headers ={"User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1",
			"Host": "paper.i21st.cn",
			"Referer": "https://paper.i21st.cn/index_21je2.html"
		}
	#调用get_url_text()获取URL的文本
	try:
		response = requests.get(url,headers=headers)
		response.raise_for_status()
		response.encoding = response.apparent_encoding
		print('正在获取响应码-------')
		print(response.status_code)#显示响应码
	#print(text)
		text = response.text
		html = etree.HTML(text)
		date = html.xpath("//div[@class='listPicDiv listPicDivM0']/text()")
	#print(date[0].strip())
		return "目前报纸最新为："+date[0].strip()
	except:
		return "产生异常"

#或去PDF content 并返回

def get_pdf(url,cookie,grade,num):
	#image_url = "https://paper.i21st.cn/download/21je1_725.pdf"
	headers ={"User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1",
				"Host": "paper.i21st.cn",
				"Referer": "https://paper.i21st.cn/index_21je2.html",
				"cookie":cookie}
	r = requests.get(url,headers = headers,stream=True) 
	#获取pdf文件大小
	file_size_str = r.headers['Content-Length']
	#将文件大小转化成MB单位
	file_size = int(file_size_str)/1024/1024
	filename = "21je{}_{}.pdf".format(grade,num)
	with open(filename,'wb') as f:
		print("当前正在下载{}".format(filename))
		count =1
		for chunk in r.iter_content(chunk_size=2048):
			if chunk:
				f.write(chunk)
				#获取当前下载进度的百分比
				percent = count/512/file_size
				print("\r","{:.2%}{}".format(percent,"#"*int(percent*72)),end = "",flush = True)#100.0%加上72个#正好占满一行
				#print("当前正在下载{}，已下载{}MB /{}MB ".format(filename,count/512,file_size))
				count = count+1
		print("**************{}已下载完毕*****************".format(filename))


def get_cookie():
	with open("cookie.txt","r") as f:
		return f.read()

if __name__ == '__main__':
	#获取用户所需哪个年级的报纸,保存在grade变量中
	while 1:
		grade = input("请输入要下载的年级，输入“q”退出：")
		if grade == 'q':
			break#无法退出
		if grade in ["1","2","3"]:
			break
		else:
			continue
	
	#获取该年级最新一期报纸，
	new_url = "https://paper.i21st.cn/index_21je{}.html".format(grade)
	print(get_newest_num(new_url))
	

	#获取用户所需哪几期报纸，保存在nums列表里
	while 1:
	#使用num保存用户所需下载的报纸期数
		num =input('输入需要下载报纸的期数，若批量下载以减号隔开；')
		try:
			if '-' in num:
				numlist = num.split('-')
				nums = list(range(int(numlist[0]),int(numlist[1])+1))
				break
			else:
				nums=[int(num)]
				break
		except:
			print("input error")
			continue

	#将用户所需下载的报纸期数储存在nums列表里
	
	cookie = get_cookie()
	#cookie = input("input cookie:")
	print(cookie)
	for i in nums:
		pdf_url = "https://paper.i21st.cn/download/21je{}_{}.pdf".format(grade,i)
		print("正在解析{}年级第{}期网页内容，请稍等*************".format(int(grade)+6,i))
		get_pdf(pdf_url, cookie,grade,i)
	#url = 'https://img.i21st.cn/paper/21je1/2021/725/9b6eece0de5f6d43b35ced51c7de6ad3.jpg'
	
	#src = get_pdf(cookie,1,750)
	#save_pdf(src,1,750)

	