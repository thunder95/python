from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random
import time
import sys

url = 'http://192.168.110.132:9080/#/login'
username = '18583995430'
pwd = '123456'

#禁止谷歌弹出保存密码之类的
options = webdriver.ChromeOptions()
prefs = {"":""}
prefs["credentials_enable_service"] = False
prefs["profile.password_manager_enabled"] = False
options.add_experimental_option("prefs", prefs)

browser = webdriver.Chrome(chrome_options=options) # Get local session of Chrome
browser.get(url) # Load page
time.sleep(0.2)

try:
	#输入用户名
    elem = browser.find_element_by_xpath('//*[@id="app"]/div/form/div[1]/div/div[1]/input')
    elem.send_keys(username)
    #输入密码
    elem = browser.find_element_by_xpath('//*[@id="app"]/div/form/div[2]/div/div[1]/input')
    elem.send_keys(pwd)
    #点击登录
    elem = browser.find_element_by_xpath('//*[@id="app"]/div/form/div[3]/div/button')
    elem.click()
    
    #隐式等待
    browser.implicitly_wait(10)
    browser.switch_to_window(browser.window_handles[-1])

    #展开所有的li
    #time.sleep(0.5)
    #js = 'document.querySelectorAll(".el-menu-item").style.display="block";'
    #browser.execute_script(js)

    #获取主菜单
    lenMain = browser.find_elements_by_xpath("//li[@class='el-submenu']")
    lastMain = -1
    lastSub = -1

except NoSuchElementException:
    assert 0, "can't find seleniumhq"
   
num = 1
errorList = [];
while True: # 该条件永远为true，循环将无限执行下去
	
	sys.stdout.flush()
	time.sleep(0.1)
	num += 1

	print ("try:"+str(num))
	try:
		#点击主菜单
		mainId = str(random.randint(1, len(lenMain))) #从1开始
		if mainId == '8' or mainId == '9' :
			continue

		main = browser.find_element_by_xpath("//li[@class='el-submenu']["+mainId+"]")
		print(len(lenMain), mainId)

		#点击子菜单
		sub = browser.find_elements_by_xpath("//li[@class='el-submenu']["+mainId+"]/ul/a/li")
		subId = random.randint(0, len(sub)-1)
		if mainId == lastMain and subId == lastSub :
			continue
		if (mainId, subId) in errorList :
			continue

		ActionChains(browser).click(main).click(sub[subId]).perform()
		print(len(sub), subId)

	except NoSuchElementException:
		if (mainId, subId) not in errorList:
			errorList.append((mainId, subId))

		print('error:'+ str(errorList))
		continue


time.sleep(2)
#browser.close()