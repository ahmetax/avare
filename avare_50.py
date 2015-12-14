# -*- coding: utf-8 -*-
#Author: Ahmet Aksoy
#Purpose: Simulate human behaviour while visiting selected web pages
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import sys
import datetime
import time
import random
from sys import stdout
import os
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#read proxy list
dosya = open('./proxy.txt','r')
liste = dosya.readlines()
dosya.close()
proxies =[]
for px in liste:
    if ':' in px:
        px = px.split(' ')[0]
    else:
        px = px.strip()
    proxies.append(px)

#read address list
dosya = open('./visits.txt','r')
liste = dosya.readlines()
visits = []
for z in liste:
    z = z.strip()
    visits.append(z)
dosya.close()

sout=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
sout = "./logs/alog-"+sout+".txt"
print(sout)
outfile = open(sout, "a")

outfile.write("avare_50")

#In order to set socket timeout remove # from the following line
#RemoteConnection.set_timeout(180)

def getRandomAddress():
    nmax = len(visits)
    random.seed(time.time())
    n = random.randint(0,nmax-1)
    return visits[n]

def getRandomProxy():
    nmax = len(proxies)
    random.seed(time.time())
    n = random.randint(0,nmax-1)
    return proxies[n]

def printLog(s):
    t = time.strftime("%H:%M:%S:%MS", time.localtime())
    print(t,s)
    outfile.write(t+s+"\n")
    outfile.flush()

def getRootAddress(adres):
    addressParts = adres.replace("http://","").split("/")
    return "http://"+addressParts[0]

def connectToPage(sproxy, nproxy, noproxy):

    profile = webdriver.FirefoxProfile()

    if profile == None:
        printLog("profile=None problem ")
        return
    profile.native_events_enabled = True
    if noproxy == False:
        profile.set_preference("network.proxy.type",1)
        profile.set_preference("network.proxy.http",sproxy)
        profile.set_preference("network.proxy.http_port",nproxy)

    printLog("Browser open "+sproxy+":"+str(nproxy))

    try:
        driver = webdriver.Firefox(firefox_profile=profile)
    except:
        printLog("profile problem ")
        try:
            driver.quit()
        except:
            e = sys.exc_info()[0]
            printLog( "Error: %s" % e )
            pass
        driver = None
    printLog("NEW DRIVER ESTABLISHED")
    return driver

def loadPage(driver,adres):

    if driver is None:
        return

    bekle = random.randint(15,25)

    driver.get(adres)

    printLog("Preferred waiting time: "+format("%f" % bekle))
    printLog("Now waiting for page to load...")
    try:
        max_time=30
        t0=time.time()
        printLog("Waiting for html tag...")
        wait = WebDriverWait(driver,30)
        wait.until(lambda driver: driver.execute_script("return document.readyState"))
        #wait.until(lambda driver: driver.find_element_by_tag_name('html'))
        t1=(time.time()-t0)
        printLog("After WebDriverWait waiting period="+format("%f" % t1))
        printLog("Page Title: "+driver.title)

        #If there are problems in page loading then try another page
        hatalar = ["Sayfa yükleme sorunu", "404 Not Found", "500 Internal Privoxy Error","503 Forwarding failure"]
        if (driver.title=='') or (driver.title in hatalar):
            printLog("Error in page loading:  "+driver.title)
            driver.quit()
            return
        # Start page show timer
        bkl=random.uniform(7.1,13.8)
        time.sleep(bkl)
        printLog("General wait="+format("%f" % bkl))

    except TimeoutException as e:
        printLog("TimeOut Exception ")
        pass
    except WebDriverException as e:
        printLog("WebDriverException ")
        pass
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        printLog( "Except Error: %s" % e )
        pass
    finally:
        printLog("Finally ")
        try:
            driver.quit()
        except:
            e = sys.exc_info()[0]
            printLog( "Finally Error: %s" % e )
        return

def loadRandomPage():

    adres = getRandomAddress()
    print(adres)
    proxy = getRandomProxy()
    noproxy = False
    if str(proxy)[0] =='#':
        noproxy = True
    proxy = proxy.split(" ")[0]
    ss = proxy.split(':')
    sproxy = ss[0]
    if len(ss)>1:
        nproxy = int(ss[1])
    else:
        nproxy = 0
        noproxy = True

    driver = connectToPage(sproxy, nproxy, noproxy)
    if driver is not None:
        loadPage(driver, adres)

stop = False
say = 0
#infinite loop

while True:
    outfile.close()
    outfile = open(sout, "a")
    if stop == True:
        break
    loadRandomPage()
    bkl = random.uniform(3.3,7.9)   #random wait
    time.sleep(bkl)
