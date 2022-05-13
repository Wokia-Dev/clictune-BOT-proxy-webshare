import os.path
import time
import random
import requests

from art import text2art
from rich.console import Console
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent

proxy_list = []
urls = []

# rich console
console = Console()

console.print(text2art('CTB by Wokia', font='sub-zero'), style='bold green')
console.print('v 0.1 \n\n', style='green')

# check if links file is empty
if os.path.getsize('links.txt') == 0:
    console.print('no links in links file exit in 3sec', style='bold red')
    time.sleep(3)
    exit()
else:
    linksFile = open('links.txt', 'r')
    for line in range(0, sum(1 for line in open('links.txt'))):
        urls.append(linksFile.readline())

# api request proxy
rep = requests.get('https://proxy.webshare.io/api/proxy/list/',
                   headers={'Authorization': '377b5b8641531b52c3404c4bff405b8a89dca67b'})
rep = rep.json()

# read old proxy list file
oldProxyListFile = open('proxy.txt', 'r')
oldProxyList = oldProxyListFile.read()
oldProxyListFile.close()

# new proxy list
currentProxyList = ''
for proxy in rep['results']:
    currentProxyList += ('https://' + proxy['proxy_address'] + ':' + str(proxy['ports']['http']) + '\n')
    proxy_list.append((proxy['proxy_address'] + ':' + str(proxy['ports']['http']) + '\n'))

# check if old proxy list is the same that new
console.print('Check if proxy is not the same..', style='bold yellow')
if currentProxyList == oldProxyList:
    console.print('the old proxy are the same exit in 3 sec..', style='bold red')
    time.sleep(3)
    exit()
else:
    # write new proxy at file
    proxyList = open('proxy.txt', 'w')
    for proxy in rep['results']:
        proxyList.write('https://' + proxy['proxy_address'] + ':' + str(proxy['ports']['http']) + '\n')

    proxyList.close()
    console.print('new proxy found \n\n', style='bold green')


# get random link
def randomLink():
    ur_len = len(urls)
    nb_url = random.randint(int(ur_len / 1.5), ur_len)
    return random.sample(urls, k=nb_url)


finalNbLinks = 0

# user all proxy on links
for prox in proxy_list:

    links = randomLink()
    finalNbLinks += len(links)

    console.print('*' * 112, style='bold green')
    console.print('load proxy ' + str(prox) + str(len(links)) + ' links to click', style='bold yellow')

    ua = UserAgent()
    user_agent = ua.random

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--proxy-server=%s' % prox)

    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)

    i = 0
    for link in links:
        i += 1
        console.print('num: ' + str(i) + 'get: ' + link, style='bold yellow')
        driver.get(link)

        # time out
        timeout = 5
        try:
            element_present = EC.presence_of_element_located((By.ID, 'compteur'))
            WebDriverWait(driver, timeout).until(element_present)

        except:
            console.print('timed out with proxy: ' + prox + ' at link ' + link, style='bold red')

        finally:
            while 'Veuillez' in driver.find_element(By.ID, 'compteur').text:
                time.sleep(0.2)
            time.sleep(0.2)
            driver.find_element(By.ID, 'compteur').click()
            time.sleep(0.5)
            console.print('success click', style='bold green')

    driver.quit()
console.print('FINISH ' + str(finalNbLinks) + ' links clicked', style='bold green')
input()
