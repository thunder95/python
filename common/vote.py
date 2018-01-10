import urllib
import http.cookiejar
import re
import random
import time
from pytesser3 import *


def vote(fl, total):
 
	#cookieUrl = "http://sc.hrnewspaper.com/show.asp?id=115";
	#获取cookie

	CaptchaUrl = "http://sc.hrnewspaper.com/checkcode_add.asp"
	PostUrl = "http://sc.hrnewspaper.com/FeedbackSave.asp"
	# 验证码地址和post地址

	cookie = http.cookiejar.CookieJar()  # 声明一个CookieJar对象实例来保存cookie
	handler = urllib.request.HTTPCookieProcessor(cookie)  # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
	opener = urllib.request.build_opener(handler)  # 通过handler来构建opener
	picture = opener.open(CaptchaUrl).read()
	# 用openr访问验证码地址,保存cookie, 获取验证码并用ocr识别

	pic_1 = 'tmp.jpg'
	local = open(pic_1, 'wb')
	local.write(picture)
	local.close()
	#保存图片

	img = Image.open(pic_1)
	pic_2 = 'tmp.png'
	img.save(pic_2)
	#更换图片格式

	im = Image.open(pic_2)
	SecretCode = image_to_string(im)
	fl.writelines(['\r\n\r\n\r\ncode_1: ', SecretCode])
	SecretCode = SecretCode.replace('I','1')
	SecretCode = SecretCode.replace('!','1')
	SecretCode = re.sub("\D", "", SecretCode)
	if (len(SecretCode) != 5):
		SecretCode = image_file_to_string(pic_2, graceful_errors=True)
		fl.writelines(['\r\ncode_2: ', SecretCode])
		SecretCode = SecretCode.replace('I','1')
		SecretCode = SecretCode.replace('!','1')
		SecretCode = SecretCode = re.sub("\D", "", SecretCode)

	fl.writelines(['\r\nEndcode: ', SecretCode])
	if (len(SecretCode) != 5):
		return;

	tup = ('%C5%AE%C9%F1%BC%D3%D3%CD',
			'%BC%D3%D3%CD%BC%D3%D3%CD',
			'%D6%A7%B3%D6%D6%A7%B3%D6',
			'%B3%A4%B7%E7%C6%C6%C0%CB%BB%E1%D3%D0%CA%B1%D6%B1%B9%D2%D4%C6%B7%AB%BC%C3%B2%D7%BA%A3',
			'%D5%C5%C0%CF%CA%A6%BA%C3%C3%C0',
			'%C5%AE%C9%F1%BA%C3%C3%C0',
			'%D6%A7%B3%D6%D5%C5%C0%CF%CA%A6+%D4%BD%C0%B4%D4%BD%BA%C3',
			'%D6%A7%B3%D6%D5%C5%D7%DC',
			'%D5%C5%D7%DC%BC%D3%D3%CD',
			'%C5%AE%C9%F1%CD%B6%D2%BB%C6%B1',
			'%C7%E1%CB%C9%D2%E6%BC%D2%C7%E1%CB%C9%B4%F3%BC%D2',
			'%D5%C5%D7%DC%A3%AC%D6%A7%B3%D6%C4%E3%A3%A1',
			'%C5%AE%C9%F1%A3%AC%D5%C5%D7%DC%A3%A1')

	content = random.choice(tup)
	postdata =urllib.parse.urlencode({	
	'nc': '%B9%AB%D6%DA',
	'content': content,
	'rname': '115',
	'checkcode': SecretCode
	}).encode('utf-8')
	print (postdata)
	fl.writelines(['\r\npostConent: ', urllib.parse.unquote_plus(content, encoding="gbk")])
	# 根据抓包信息 构造表单数据 content需要EUC-CN编码

	header = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	"Accept-Encoding":"gzip, deflate",
	'Accept-Language': 'zh-CN,zh;q=0.8',
	'Connection': 'keep-alive',
	"Host":"sc.hrnewspaper.com",
	"Referer":"http://sc.hrnewspaper.com/show.asp?id=115",
	'Content-Type': 'application/x-www-form-urlencoded',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
	}
	req = urllib.request.Request(PostUrl,postdata,header)
	# 根据抓包信息 构造headers

	try:
		response = opener.open(req)
		result = response.read().decode('gb2312')
		# 由于该网页是gb2312的编码，所以需要解码

		
		if  result.find('留言需要审核请耐心等待', 1) > -1:
			fl.writelines(['\r\nOK: ', time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))])
			return
		else:
			fl.writelines(['\r\nERROR: ', result ])

	# 打印登录后的页面
	except urllib.error.URLError as e:
	    print(e.reason)
	    fl.writelines(['\r\nERROR: ', e.reason, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))])
	# 利用之前存有cookie的opener登录页面

fl = open('vote_log.txt', 'a+', encoding= 'utf8')
total = 0
for i in range(1, 1000):
   result = vote(fl, total);
   if result == 1:
       total = total+1
   time.sleep(3)
   # 延迟3秒再投


fl.writelines(['\r\n累计成功: ', str(total)])
fl.close()

print ('本次成功投票待审核:')
print (total)

