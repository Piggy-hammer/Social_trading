import sys
import time
from selenium.webdriver.support import expected_conditions as EC

import pandas
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

# 登录用的账户名和密码
username = 'mouyangchen@163.com'
key = 'X9aj:7.tCCGWG7u'


def login(browser):
    # 打开登录页面
    browser.get('https://www.zulutrade.com/login')
    # 等待加载，最多等待20秒
    browser.implicitly_wait(10)
    browser.find_element_by_id("main_tbUsername").send_keys(username)
    browser.find_element_by_id("main_tbPassword").send_keys(key)
    browser.find_element_by_id("main_btnLogin").click()
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located(('id', 'welcome-modal-page-1')))
        print("登录成功宝贝！\n")
    except TimeoutException:
        browser.quit()
        sys.exit('open login page timeout')

if __name__ == '__main__':
    # 设置selenium使用chrome的无头模式
    options = Options()
    prefs = {'profile.default_content_settings.popups': 0, 'dowload.default_directory': 'D:\新建文件夹\Zulu\Trading_history'}
    options.add_experimental_option('prefs', prefs)
    # options.add_argument('--headless')
    options.add_argument("--window-size=1920,1080")
    # 在启动浏览器时加入配置
    browser = webdriver.Chrome(options=options)

    login(browser)

    # 测试用的四个网址
    list = ('https://www.zulutrade.com/trader/386204?t=10000', 'https://www.zulutrade.com/trader/421590?t=10000',
            'https://www.zulutrade.com/trader/391899?t=10000', 'https://www.zulutrade.com/trader/416576?t=10000')
    for e in list:
        browser.get(e)
        browser.implicitly_wait(5)
        browser.find_element_by_xpath(
            '/html/body/app/zl-layout/zl-trader/div[2]/div/div[2]/zl-trader-status/div[2]/div[1]/a').click()
        time.sleep(0.1)
        name = browser.find_element_by_xpath('/html/body/app/zl-layout/zl-trader/div[2]/div/div[1]/zl-trader-profile/div[1]/div/h1').text
        rank = browser.find_element_by_xpath('/html/body/app/zl-layout/zl-trader/div[2]/div/div[1]/zl-trader-rank/div/span/strong').text
        balance = browser.find_element_by_xpath('/html/body/app/zl-layout/zl-trader/div[2]/div/div[2]/zl-trader-status/div[2]/div[1]/div[2]/div/span[2]').text
        leverage = browser.find_element_by_xpath(
            '/html/body/app/zl-layout/zl-trader/div[2]/div/div[2]/zl-trader-status/div[2]/div[1]/div[2]/div/span[4]').text
        open_positions = browser.find_element_by_xpath('//*[@id="overallStats"]/div[5]/div[2]').text

        print(name, rank, balance, leverage, open_positions)
