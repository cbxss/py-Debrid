import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
API = ''   #api
user = ""  #username
passw = "" #pass
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-proxy-server')
headers = {
    'Authorization': 'Bearer '+ API,
    }
mad = input("Enter a Magnet Link: ")
postdata = {'host': 'real-debrid.com', 'split': '2', 'magnet': mad}
r= requests.post('https://api.real-debrid.com/rest/1.0/torrents/addMagnet',data = postdata, headers= headers)
r2 = requests.get('https://api.real-debrid.com/rest/1.0/torrents/info/' + r.json()['id'],
                  headers=headers)
jsonfiles = r2.json()['files']
if len(jsonfiles) == 0:
    print('Needs time to convert to torrent.')
    quit()
else:
    for idx, item in enumerate(jsonfiles):
        print(f'{idx + 1} ' + item['path'])
    print('Okay, now we\'ll need a comma seperated list of indexes for files you want.')
    selectedfiles = input('List of IDs or ALL: ')
    postdata = {'files': selectedfiles}
    r3 = requests.post('https://api.real-debrid.com/rest/1.0/torrents/selectFiles/' + r.json()['id'], data=postdata,
                       headers=headers)
    if r3.status_code == 204:
        print('Yay, torrent has been added and will now be downloaded')
    else:
        print(f'Oops! Error')
driver = webdriver.Chrome('/users/cbass/downloads/chromedriver', options=options)  #CHANGE PATH TO CHROMEDRIVER
driver.get('https://real-debrid.com')
print("real-debrid.com  Opened")
element = driver.find_element_by_xpath("""//*[@id="allpage-login-top"]/span""")
driver.execute_script("arguments[0].click();", element)
time.sleep(1)
driver.find_element_by_xpath("""//*[@id="loginform"]/fieldset[1]/input""").click()
driver.find_element_by_xpath("""//*[@id="loginform"]/fieldset[1]/input""").send_keys(user)
driver.find_element_by_xpath("""//*[@id="loginform"]/fieldset[2]/input""").send_keys(passw)
driver.find_element_by_xpath("""//*[@id="submit"]""").click()
print("Logged In!")
time.sleep(2)
driver.get('https://real-debrid.com/torrents')
time.sleep(1)
while True:
    try:
        print("Starting Download")
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior',
                  'params': {'behavior': 'allow', 'downloadPath': r'C:\Users\cbass\Downloads'}}                     #CHANGE PATH
        command_result = driver.execute("send_command", params)
        element = driver.find_element_by_xpath("""//*[@id="wrapper_global"]/div/div/table/tbody/tr[3]/td/form/input""")
        driver.execute_script("arguments[0].click();", element)
        break
    except:
        print("Probably isn't downloaded on Real-Debrid sorry!")
        break;
time.sleep(3)
dl = driver.find_element_by_xpath("""//*[@id="l1"]/a[1]""")
driver.execute_script("arguments[0].click();", dl)
print("Downloading")
time.sleep(0.5)
def downloads_done():
    for i in os.listdir(r"C:\Users\cbass\Downloads"):
        if ".crdownload"  in i:
            time.sleep(0.5)
            downloads_done()
downloads_done()
print("Done! Closing browser and exiting.")
driver.close()