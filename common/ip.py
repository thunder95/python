import urllib.request  
import os, re,sys,time,socket,threading,random
import urllib
import http.cookiejar
from pytesser3 import *

try:  
    from StringIO import StringIO  
except ImportError:  
    from io import StringIO  
  
  
loca = re.compile(r"""ion":"\D+", "ti""")  
#伪装成浏览器  
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}  
  
class Getip():  
    def __init__(self,diqu):  
        self.ur ={"xicidaili国内普通代理   --1线":"http://www.xicidaili.com/nt/",  
                                
             "ip84国内普通代理   --2线":'http://www.ip84.com/dlpn-http/',  
                                
             'xicidaili国内高匿名代理 --1线':'http://www.xicidaili.com/nn/',  
                              
             'ip84国内高匿名代理 --2线':'http://www.ip84.com/dlgn-http/',  
               
             'xicidaili国外高匿名代理 --1线':'http://www.xicidaili.com/wn/',  
               
             'ip84国外高匿名代理 --2线':'http://www.ip84.com/gwgn-http/',  
             'xicidaili国外普通代理   --1线':'http://www.xicidaili.com/wt/',  
             'haodailiip国内混合代理   --3线':'http://www.haodailiip.com/guonei/',  
             'haodailiip国外混合代理   --3线':'http://www.haodailiip.com/guoji/',  
                                }  
        self.diqu = diqu  
      
    def urlopen(self,url):  
        global header  
        try:  
            req = urllib.request.Request(url, None, header)  
            res=urllib.request.urlopen(req)  
          
            return res  
        except:  
            pass  
    def getip(self,ren):  
        '''''url = "http://proxy.ipcn.org/proxylist.html"#代理IP页面 
        ip_proxy_re = re.compile(r"""\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,}""")#  直接匹配  xxx.xxx.xxx.xxx:xxxx'''  
          
        url = self.ur[self.diqu]+str(ren)  
        print(url)
        ip_proxy_re = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*</td>\s*<td>\s*(\d{1,})\s*</td>\s*<[^\u4E00-\u9FA5]+>([\u4E00-\u9FA5]*\s*[\u4E00-\u9FA5]*\s*[\u4E00-\u9FA5]*)\s*<')  
  
        #################################通用正则匹配的      格式 是       (IP,端口,地区)  地区有可能包含换行和空格  
  
        try:  
            data = self.urlopen(url).read().decode('utf-8')  
        except:  
            return None  
  
          
          
        self.rel = []  
          
        ip = ip_proxy_re.findall(data)  
        ##########返回的IP 就是 正则匹配的结果(IP,端口,地区)  地区有可能包含换行和空格  
              
        return ip  

#验证的函数, 先不写入类
def valid(prox):
    socket.setdefaulttimeout(3)  #设置全局超时时间
    #url = "http://sc.hrnewspaper.com/show.asp?id=115"  #打算爬取的网址
    #url = 'http://www.whatismyip.com.tw/'
    try:
        #目标URL
        CaptchaUrl = "http://sc.hrnewspaper.com/checkcode_add.asp"
        PostUrl = "http://scwc.hrnewspaper.com/FeedbackSave.asp"

        #随机的userAgent
        agents = (
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
            )
        agent = random.choice(agents)

        #添加headers
        header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        "Accept-Encoding":"gzip, deflate",
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        "Host":"sc.hrnewspaper.com",
        "Referer":"http://sc.hrnewspaper.com/show.asp?id=115",
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': agent,
        }
        headers = []
        for key, value in header.items():
            elem = (key, value)
            headers.append(elem)
   
        cookie = http.cookiejar.CookieJar()  # 声明一个CookieJar对象实例来保存cookie
        cookie_support = urllib.request.HTTPCookieProcessor(cookie) 
        proxy_support = urllib.request.ProxyHandler(prox)
        opener = urllib.request.build_opener(proxy_support, cookie_support)
        opener.addheaders = headers
        urllib.request.install_opener(opener)
        
        #取验证码
        picture = opener.open(CaptchaUrl).read()

        #lock.acquire()     #线程上锁

        #处理验证码
        pic_1 = 'tmp.jpg'
        local = open(pic_1, 'wb')
        local.write(picture)
        local.close() #保存图片

        img = Image.open(pic_1)
        pic_2 = 'tmp.png'
        img.save(pic_2) #更换图片格式

        im = Image.open(pic_2)
        SecretCode = image_to_string(im)
        print ('code_1: ', SecretCode)
        SecretCode = SecretCode.replace('I','1')
        SecretCode = SecretCode.replace('!','1')
        SecretCode = re.sub("\D", "", SecretCode)
        if (len(SecretCode) != 5):
            SecretCode = image_file_to_string(pic_2, graceful_errors=True)
            print ('code_2: ', SecretCode)
            SecretCode = SecretCode.replace('I','1')
            SecretCode = SecretCode.replace('!','1')
            SecretCode = SecretCode = re.sub("\D", "", SecretCode)

        print ('code_3: ', SecretCode)
        if (len(SecretCode) != 5):
            return;


        #开始灌水

        #随机的留言内容
        tup = ('%C5%AE%C9%F1%BC%D3%D3%CD%7E',
            '%BC%D3%D3%CD%BC%D3%D3%CD%7E',
            '%D6%A7%B3%D6%D6%A7%B3%D6%7E',
            '%B3%A4%B7%E7%C6%C6%C0%CB%BB%E1%D3%D0%CA%B1%D6%B1%B9%D2%D4%C6%B7%AB%BC%C3%B2%D7%BA%A3%7E',
            '%D5%C5%C0%CF%CA%A6%BA%C3%C3%C0%7E',
            '%C5%AE%C9%F1%BA%C3%C3%C0%7E',
            '%D6%A7%B3%D6%D5%C5%C0%CF%CA%A6+%D4%BD%C0%B4%D4%BD%BA%C3%7E',
            '%D6%A7%B3%D6%D5%C5%D7%DC%7E',
            '%D5%C5%D7%DC%BC%D3%D3%CD%7E',
            '%C5%AE%C9%F1%CD%B6%D2%BB%C6%B1%7E',
            '%C7%E1%CB%C9%D2%E6%BC%D2%C7%E1%CB%C9%B4%F3%BC%D2%7E',
            '%D5%C5%D7%DC%A3%AC%D6%A7%B3%D6%C4%E3%A3%A1%7E',
            '%C5%AE%C9%F1%A3%AC%D5%C5%D7%DC%A3%A1%7E',
            '%B5%E3%D4%DE%B5%E3%D4%DE%7E',
            '%B8%F8%C4%E3%B5%E3%D4%DE%7E',
            '%D5%C5%D7%DC%BA%C3%B0%F4%7E',)

   
        content = random.choice(tup)
        postdata =urllib.parse.urlencode({  
        'nc': '%B9%AB%D6%DA',
        'content': content,
        'rname': '115',
        'checkcode': SecretCode
        }).encode('utf-8')
        request = urllib.request.Request(PostUrl)
        response = urllib.request.urlopen(request, postdata)

        #try:
        result = response.read().decode('gb2312')

        
        if  result.find('留言需要审核请耐心等待', 1) > -1:
            print ('ok')
            #time.sleep(2)
            # 延迟10秒再投
            return 1
        else:
            print (result)
        #vote(prox)
        #print(prox,'is OK')        
        #proxy_ip.write('%s\n' %str(prox))  #写入该代理IP
        #lock.release()     #释放锁
    except Exception as e:
        #lock.acquire()
        print(prox,e)
        #lock.release()

#执行函数
def run(name):
    g = Getip(name)
    for x in range(4):  
        ips = g.getip(1)
        print (ips)
        if ips is None:
            continue
        num = len(ips)  

        for i in range (num):
            proxy_host = ips[i][0]+':'+ips[i][1]
            fo.writelines([str(proxy_host), '\n'])
        time.sleep(3)
  
if __name__ == '__main__':  
    import pprint  

    if 0:
        fo = open('ips_log.txt', 'w', encoding= 'utf8')
        run("xicidaili国内普通代理   --1线")
        fo.close()

    fr = open('ips_log.txt', 'r', encoding= 'utf8')
    for x in range(10):
        print ('运行第: ', x, '次')
        for line in fr.readlines():                              #依次读取每行 
            line = line.strip()                                    #去掉每行头尾空白 
            if not len(line) or line.startswith('#'):       #判断是否是空行或注释行 
                continue                                            #是的话，跳过不处理 
            print (line) 
            valid({'http':line})
    fr.close()
        #print('获取到ip地址一共:',len(ips))
        #print(ips[0][0])  
        #pprint.pprint(ips)  

    #proxy_ip=open('proxy_ip.txt','w')  #新建一个储存有效IP的文档
    #lock=threading.Lock()  #建立一个锁

    #threads=[]
    #for i in range(len(proxys)):
        #thread=threading.Thread(target=valid,args=[proxys[i]])
        #threads.append(thread)
        #thread.start()
    #阻塞主进程，等待所有子线程结束
    #for thread in threads:
        #thread.join()
        
    #proxy_ip.close()  #关闭文件
