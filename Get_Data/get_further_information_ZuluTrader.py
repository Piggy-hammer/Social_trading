import sys
import time

from selenium.common import exceptions
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
original_csv = r'D:\Social_trading\Zulu\ZuluInvestors_original_0922.csv'
new_csv = r'D:\Social_trading\Zulu\ZuluInvestors_0922.csv'
trading_history_dir = 'D:\\Social_trading\\Zulu\\Trading_history'

def iselement(browser, xpaths):
    """
    基本实现判断元素是否存在
    :param browser: 浏览器对象
    :param xpaths: xpaths表达式
    :return: 是否存在
    """
    try:
        browser.find_element_by_xpath(xpaths)
        return True
    except exceptions.NoSuchElementException:
        return False



def login(browser):
    # 打开登录页面
    browser.get('https://www.zulutrade.com/login')
    # 等待加载，最多等待20秒
    browser.implicitly_wait(10)
    browser.maximize_window()
    time.sleep(1)

    # 关闭cookie提示
    close_cookie = browser.find_element_by_xpath('//*[@id="cookie-acceptance"]/span')
    ActionChains(browser).move_to_element(close_cookie).click(on_element=None).perform()

    browser.find_element_by_id("main_tbUsername").send_keys(username)
    browser.find_element_by_id("main_tbPassword").send_keys(key)
    browser.find_element_by_id("main_btnLogin").click()
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located(('id', 'welcome-modal-page-1')))
        print("登录成功宝贝！\n")
    except TimeoutException:
        browser.quit()
        sys.exit('open login page timeout')


def read_csv(oringal_csv):
    dataframe = pandas.read_csv(oringal_csv).set_index('name')
    dataframe.insert(loc=len(dataframe.columns), column='rank', value=None)
    dataframe.insert(loc=len(dataframe.columns), column='nation', value=None)
    dataframe.insert(loc=len(dataframe.columns), column='rating_star', value=None)
    dataframe.insert(loc=len(dataframe.columns), column='balance', value=None)
    dataframe.insert(loc=len(dataframe.columns), column='leverage', value=None)
    dataframe.insert(loc=len(dataframe.columns), column='amount_following', value=None)
    dataframe.insert(loc=len(dataframe.columns), column='ROI', value=None)
    dataframe.insert(loc=len(dataframe.columns), column='is_ROI_annual', value=None)
    dataframe.insert(loc=len(dataframe.columns), column='total_Profit', value=None)
    dataframe.insert(loc=len(dataframe.columns), column='open_positions', value=None)
    dataframe.insert(loc=len(dataframe.columns), column='weeks', value=None)
    dataframe.insert(loc=len(dataframe.columns), column='max_drawdown', value=None)
    dataframe.insert(loc=len(dataframe.columns), column='total_followers', value=None)
    dataframe.insert(loc=len(dataframe.columns), column='copied_by_real_investors', value=None)
    dataframe.insert(loc=len(dataframe.columns), column='viewed', value=None)
    dataframe.insert(loc=len(dataframe.columns), column='recommended_min_investment', value=None)
    dataframe.insert(loc=len(dataframe.columns), column='last_updated', value=None)
    dataframe.insert(loc=len(dataframe.columns), column='trading_times', value=None)
    dataframe.insert(loc=len(dataframe.columns), column='trading_history', value=None)

    print(dataframe.columns)
    print(dataframe)
    return dataframe


def get_data(browser, df):
    # 先测试前10个投资领袖
    df = df[0:10]

    for inx, data in df.iterrows():
        browser.get(data['website'])
        browser.implicitly_wait(5)

        # 将初始单位更改为美元
        browser.find_element_by_xpath('/html/body/app/zl-layout/zl-trader/div[3]/div/div/div[2]/div['
                                      '2]/trader-trading/div[2]/trader-trading-currency-toggle/div/span[1]').click()

        # 加载详细介绍
        more_info = iselement(browser, '/html/body/app/zl-layout/zl-trader/div[2]/div/div[2]/zl-trader-status/div['
                                       '2]/div[1]/a' )
        if more_info:
            browser.find_element_by_xpath(
                '/html/body/app/zl-layout/zl-trader/div[2]/div/div[2]/zl-trader-status/div[2]/div[1]/a').click()
            time.sleep(0.1)

        # 获取各项详细信息
        name = inx
        rank = browser.find_element_by_xpath('/html/body/app/zl-layout/zl-trader/div[2]/div/div['
                                             '1]/zl-trader-rank/div/span/strong').text[1:]
        rating_star = browser.find_element_by_xpath('/html/body/app/zl-layout/zl-trader/div[2]/div/div['
                                                    '1]/zl-trader-profile/div[2]/ngl-rating').get_attribute('title')
        nation = browser.find_element_by_xpath('/html/body/app/zl-layout/zl-trader/div[2]/div/div['
                                               '1]/zl-trader-profile/zl-user-logo/div/span[2]').get_attribute('nation')
        balance = browser.find_element_by_xpath('/html/body/app/zl-layout/zl-trader/div[2]/div/div['
                                                '2]/zl-trader-status/div[2]/div[1]/div[2]/div/span[2]').text
        leverage = browser.find_element_by_xpath('/html/body/app/zl-layout/zl-trader/div[2]/div/div['
                                                 '2]/zl-trader-status/div[2]/div[1]/div[2]/div/span[4]').text
        amount_following = browser.find_element_by_xpath('/html/body/app/zl-layout/zl-trader/div[3]/div/div/div['
                                                         '1]/zl-trader-overall-stats/div/div[2]/span').text
        ROI = browser.find_element_by_xpath('/html/body/app/zl-layout/zl-trader/div[3]/div/div/div['
                                            '1]/zl-trader-overall-stats/div/div[3]/span').text
        weeks = int(browser.find_element_by_xpath('/html/body/app/zl-layout/zl-trader/div[3]/div/div/div['
                                                  '1]/zl-trader-overall-stats/div/div[6]/span').text)
        is_ORI_annual = 1 if weeks > 52 else 0
        total_Profit = browser.find_element_by_xpath('/html/body/app/zl-layout/zl-trader/div[3]/div/div/div['
                                                     '1]/zl-trader-overall-stats/div/div[4]/div[2]').text
        open_positions = browser.find_element_by_xpath('/html/body/app/zl-layout/zl-trader/div[3]/div/div/div['
                                                       '1]/zl-trader-overall-stats/div/div[5]/div[2]').text
        max_drawdown = browser.find_element_by_xpath('/html/body/app/zl-layout/zl-trader/div[3]/div/div/div['
                                                     '1]/zl-trader-overall-stats/div/div[7]/span').text
        total_followers = browser.find_element_by_xpath('/html/body/app/zl-layout/zl-trader/div[3]/div/div/div['
                                                        '1]/zl-trader-overall-stats/div/div[8]/span').text
        copied_by_real_investors = browser.find_element_by_xpath('/html/body/app/zl-layout/zl-trader/div['
                                                                 '3]/div/div/div[1]/zl-trader-overall-stats/div/div['
                                                                 '9]/span').text
        viewed = browser.find_element_by_xpath('/html/body/app/zl-layout/zl-trader/div[3]/div/div/div['
                                               '1]/zl-trader-overall-stats/div/div[10]/span').text
        recommended_min_investment = browser.find_element_by_xpath('/html/body/app/zl-layout/zl-trader/div['
                                                                   '3]/div/div/div['
                                                                   '1]/zl-trader-overall-stats/div/div[11]/span').text
        last_updated = browser.find_element_by_xpath('/html/body/app/zl-layout/zl-trader/div[3]/div/div/div['
                                                     '1]/zl-trader-overall-stats/div/div[12]/span').text


        trading_times = int(browser.find_element_by_xpath('/html/body/app/zl-layout/zl-trader/div[3]/div/div/div[2]/div['
                                          '2]/trader-trading/div['
                                          '3]/ngl-tabs/div/zl-trading-history-table-container/div/zl'
                                          '-trading-history-table/section/div[1]/span').text.split()[4])

        # 下载csv
        browser.find_element_by_xpath('/html/body/app/zl-layout/zl-trader/div[3]/div/div/div[2]/div['
                                      '2]/trader-trading/div['
                                      '3]/ngl-tabs/div/zl-trading-history-table-container/zl-trading-history-excel'
                                      '-export/span/button').click()
        time.sleep(0.2)
        choose_csv = browser.find_element_by_xpath('/html/body/app/zl-layout/zl-trader/div[3]/div/div/div[2]/div['
                                                   '2]/trader-trading/div['
                                                   '3]/ngl-tabs/div/zl-trading-history-table-container/zl-trading'
                                                   '-history-excel-export/span/div/ul/li[3]/a')
        ActionChains(browser).move_to_element(choose_csv).click(on_element=None).perform()

        # 根据总交易量自定义下载等候时间
        sleep_time = 0.5 + round(trading_times / 1000, 1)
        time.sleep(sleep_time)

        trading_history = trading_history_dir + '\\' + 'TradingHistory_' + name + '_2022922.csv'

        print(name, rank, balance, leverage, open_positions, trading_times, sleep_time, trading_history)

        data['rank'] = rank
        data['rating_star'] = rating_star
        data['nation'] = nation
        data['balance'] = balance
        data['leverage'] = leverage
        data['amount_following'] = amount_following
        data['ROI'] = ROI
        data['is_ROI_annual'] = is_ORI_annual
        data['total_Profit'] = total_Profit
        data['open_positions'] = open_positions
        data['weeks'] = weeks
        data['max_drawdown'] = max_drawdown
        data['total_followers'] = total_followers
        data['copied_by_real_investors'] = copied_by_real_investors
        data['viewed'] = viewed
        data['recommended_min_investment'] = recommended_min_investment
        data['last_updated']= last_updated
        data['trading_times'] = trading_times
        data['trading_history'] = trading_history

    # 返回修改后的dataframe文件
    return df


if __name__ == '__main__':
    # 设置selenium使用chrome的无头模式
    options = Options()
    # options.add_argument('--headless')

    # 设置下载模式和路径
    prefs = {'profile.default_content_settings.popups': 0,
             # "profile.default_content_setting_values.automatic_downloads": 1,
             'download.default_directory': trading_history_dir}
    options.add_experimental_option('prefs', prefs)
    options.add_argument("--window-size=1920,1080")
    # 在启动浏览器时加入配置
    browser = webdriver.Chrome(options=options)

    df = read_csv(original_csv)

    login(browser)

    data = get_data(browser, df)

    print("输出csv格式")

    data.to_csv(new_csv, encoding='UTF-8')
