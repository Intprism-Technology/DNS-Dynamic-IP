import time
import re
import importorinstall
import configuration
from DnsDriver import cloudflare

importorinstall.package('selenium')
importorinstall.package('webdriver_manager')
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

config = configuration
if(config.browserDriver == 'chrome'):
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    if(configuration.headlessMode == True):
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options = options.add_argument("--headless")
    else:
        options = ''
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
elif(config.browserDriver == 'firefox'):
    from selenium.webdriver.firefox.service import Service
    from webdriver_manager.firefox import GeckoDriverManager
    if(configuration.headlessMode == True):
        from selenium.webdriver.firefox.options import Options
        options = Options()
        options.headless = True
    else:
        options = ''
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
elif(config.browserDriver == 'msedge'):
    from selenium.webdriver.edge.service import Service
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    if(configuration.headlessMode == True):
        from selenium.webdriver.edge.options import Options
        options = Options()
        options.add_argument("headless")
    else:
        options = ''
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
username = config.username
password = config.password

def ChangeDNS(ip):
    if(configuration.dnsDriver == 'cloudflare'):
        cloudflare.dns_update(ip)

if(config.routerType == 'G-240W-L'):
    def Timeout():
        print("Timeout happened no page load...")
        driver.close()
    def Loading(id):
        try:    
            w = WebDriverWait(driver, 10)
            w.until(EC.presence_of_element_located((By.ID, id)))
        except:
            Timeout()
    def Login():
        driver.get("http://"+config.routerIP)
        Loading("loginform")
        driver.find_element(By.NAME, "name").send_keys(username)
        driver.find_element(By.NAME, "pswd").send_keys(password)
        driver.find_element(By.NAME, "loginBT").send_keys(Keys.ENTER)
        Loading("wrap")

    def CheckIPv4():
        Login()
        driver.get("http://"+config.routerIP+"/show_wan_status.cgi?ipv4")
        Loading("wan_conlist_div")
        time.sleep(1)
        public_ip = driver.find_element(By.ID, "ExternalIPAddress")
        rfc1918 = re.compile('^(10(\.(25[0-5]|2[0-4][0-9]|1[0-9]{1,2}|[0-9]{1,2})){3}|((172\.(1[6-9]|2[0-9]|3[01]))|192\.168)(\.(25[0-5]|2[0-4][0-9]|1[0-9]{1,2}|[0-9]{1,2})){2})$')
        if rfc1918.match(public_ip.text):
            driver.get("http://"+config.routerIP+"/wan_config_glb.cgi")
            Loading("cfg_wan")
            ipv = driver.find_element(By.XPATH, "//select[@name='ipv']")
            print(ipv.get_attribute("value"))
            if(ipv.get_attribute("value") == '1'):
                driver.find_element(By.XPATH, "//select[@name='ipv']/option[text()='IPv4&IPv6']").click()
            else:
                driver.find_element(By.XPATH, "//select[@name='ipv']/option[text()='IPv4']").click()
            driver.find_element(By.ID, "do_edit").send_keys(Keys.ENTER)
            Loading("cfg_wan")
            driver.get("http://"+config.routerIP+"/login.cgi?out")
            Loading("loginform")
            return 'reconnect_ok'
        else:
            print('IP : '+public_ip.text)
            print('Change DNS...')
            ChangeDNS(public_ip.text)
            driver.close()
            print('Success...')
else:
    driver.close()
    print("Router not Supported !")