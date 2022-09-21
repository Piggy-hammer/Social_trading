import sys

import pandas
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

# 登录用的账户名和密码
username = 'mouyangchen@163.com'
key = 'X9aj:7.tCCGWG7u'


# 此方法用于登录
def login(browser):
    # 打开登录页面
    browser.get('https://www.zulutrade.com/login')
    # 等待加载，最多等待20秒
    browser.implicitly_wait(10)
    browser.find_element_by_id("main_tbUsername").send_keys(username)
    browser.find_element_by_id("main_tbPassword").send_keys(key)
    browser.find_element_by_id("main_btnLogin").click()
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located(("id", "welcome-modal-page-1")))
        print("登录成功宝贝！\n")
    except TimeoutException:
        browser.quit()
        sys.exit('open login page timeout')


# 此方法用于获取所有投资领袖的个人主页链接
def getTradeList(browser):
    browser.get('https://www.zulutrade.com/traders/winning/30')
    browser.implicitly_wait(10)
    browser.find_element_by_xpath(
        '/html/body/app/zl-layout/zl-performance/div/zl-performance-forex/div['
        '2]/div/zl-performance-forex-view/div/button/zl-icon/ngl-icon').click()
    # xoffset 和 yoffset 分别为节点坐标的 x 和 y
    above = browser.find_element_by_xpath('/html/body/app/zl-layout/zl-performance/div/zl-performance-forex/div['
                                          '2]/div/zl-performance-forex-view/div/div/ul/li[2]/a')
    ActionChains(browser).move_to_element(above).perform()
    # ActionChains(browser).move_by_offset(xoffset=1394, yoffset=400).perform()
    sleep(2)
    ActionChains(browser).click(on_element=None).perform()
    # 执行这一步释放鼠标，（可选
    ActionChains(browser).release()


def getTheFullList(browser, df):
    # ‘加载下一页’按钮的位置
    locatorOfAdd = '/html/body/app/zl-layout/zl-performance/div/zl-performance-forex/ngl-tabs/div/ngl-tabs/div/zl' \
                   '-performance-forex-all/zl-load-more/button '
    # 投资领袖的位置
    locatorOfInvestorList = '/html/body/app/zl-layout/zl-performance/div/zl-performance-forex/ngl-tabs/div/ngl-tabs' \
                            '/div/zl-performance-forex-all/zl-performance-forex-list/div/table/* '

    # 关闭cookie提示窗口
    close_cookie = browser.find_element_by_xpath('/html/body/app/zl-layout/zl-cookies-policy/div/div/button')
    ActionChains(browser).move_to_element(close_cookie).click(on_element=None).perform()

    # 计算需要点击添加按钮的次数
    amount_need = 500
    press = int((amount_need - 50) / 50)

    # 点击press次添加按钮,每按一次增加50个
    for i in range(press):
        add = browser.find_element_by_xpath(locatorOfAdd)
        ActionChains(browser).move_to_element(add).click(on_element=None).perform()
        WebDriverWait(browser, 20, 0.1).until(EC.presence_of_element_located((By.XPATH, locatorOfAdd)))

    # 获取最终名单
    investorList = browser.find_elements_by_xpath(locatorOfInvestorList)
    print(len(investorList) / 2)
    for e in investorList:
        if e.tag_name == 'div':
            continue
        print(e.tag_name)
        web_link = e.find_element_by_xpath('./tr[1]/td[2]/zl-username/a')
        name = web_link.get_attribute("title")
        href = web_link.get_attribute('href')
        df.loc[name] = [name,href]
    print(df)
    df.to_csv('D:/Social_trading/Zulu/ZuluInvestors_original.csv', encoding='UTF-8')


if __name__ == '__main__':
    df = pandas.DataFrame(columns=['name', 'website']).set_index('name',drop=None)
    print(df.columns)

    # 设置selenium使用chrome的无头模式
    options = Options()

    # options.add_argument('--headless')
    options.add_argument("--window-size=1920,1080")
    # 在启动浏览器时加入配置
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()

    login(browser)

    getTradeList(browser)

    getTheFullList(browser, df)
