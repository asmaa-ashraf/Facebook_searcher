from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas
class FbSearcherBot:
    def __init__(self, x=1):
        if x != 1:
            self.browser = None
            self.l = True
            self.username = ''
            self.password = ''
        else:
            self.l = False
            self.browser = webdriver.Chrome()
            self.browser.get("http://www.facebook.com")
            self.username = ''
            self.password = ''

    def login(self, account, passw):

        if self.l:
            self.browser = webdriver.Chrome()
            self.browser.get("http://www.facebook.com")
            self.l = False
        try:
            username = self.browser.find_element_by_id("email")
            password = self.browser.find_element_by_id("pass")
            submit = self.browser.find_element_by_name("login")
            username.send_keys(account)
            password.send_keys(passw)
            submit.click()
        except:
            return 1
        self.username = account
        self.password = passw
        self.tsid=''
        try:
            username = self.browser.find_element_by_id("email")
            print(username)
        except:
            print("logged in")
            return 0
        else:
            return 2
        return 0
    def gettsid(self,item):
        wait = WebDriverWait(self.browser, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='search']"))).send_keys(item+Keys.ENTER)
        wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'search')]"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'search/pages')]")))
        element=self.browser.find_element_by_xpath("//a[contains(@href,'search/pages')]")
        s = element.get_attribute('href')
        #element.click()

        href=str(s)
        start = href.find('tsid__=')
        end = start + 7
        first = href[end:-1]
        last = first.find('&amp')
        tsid = first[0:last]
        #get the pag's url and get the tsid from it

        self.tsid=tsid
    def visitpage(self,url):
        url=url+'/about/?ref=page_internal'
        self.browser.get(url)
        
    def search(self, item):
        if self.tsid=='':
            self.gettsid(item)
        wait = WebDriverWait(self.browser, 10)
        url = 'https://web.facebook.com/search/pages/?q=' + item + '&amp%3B__tsid__='+self.tsid+'&amp%3B__epa__=SERP_TAB&amp%3B__eps__=SERP_TOP_TAB'
        self.browser.get(url)
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Search results']")))
        searchdiv = self.browser.find_element_by_xpath("//div[@aria-label='Search results']")

        results = searchdiv.find_elements(By.XPATH, './/a')
        pages=[]
        for result in results:
            page=result.get_attribute('href')
            pages.append(page)
        return pages
        # wait.until(EC.presence_of_element_located((By.XPATH,"//input[@type='search']"))).send_keys(item)
        # wait.until(EC.presence_of_element_located((By.XPATH,"//a[contains(@href,'search')]"))).click()
        # wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'search/pages')]"))).click()
        # self.browser.find_element_by_xpath("//a[contains(@href,'search')]").click()
        # c.send_keys(Keys.ENTER)
        # result = self.browser.find_element_by_xpath("//input[@type='search']")
        # result.send_keys(item)

    def readfile(self, filepath):
        # use pandas to read the keywords file and return a list of keywords
        print('opening file' + filepath)
        data=pandas.read_csv(filepath)

        return data

    def getinfo(self, f,r='outbut.csv'):
        keywords = self.readfile(f)
        #results = pandas.DataFrame(columns=['keyword','page'])
        o = pandas.DataFrame({'keyword': [], 'page': []})
        c = 0
        for keyword in keywords:
            o.loc[c] = [keyword] + [self.search(keyword)]
            c = c + 1

        # write results to output.csv

        o.to_csv(r)


    def close(self):
        self.browser.close()


bot = FbSearcherBot()
name=input("enter your email on facebook,please:")
password=input("enter your password on facebook,please:")
bot.login(name, password)
file=input('enter the file path of the keywords file:')
c = bot.getinfo(file)