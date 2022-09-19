from selenium import webdriver
from selenium.webdriver.chrome.options import Options

username = 'mouyangchen@163.com'
key = ''

# 设置selenium使用chrome的无头模式
options = Options()
#options.add_argument('--headless')
options.add_argument("--window-size=1920,1080")
headers = {
      "User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
}
# 在启动浏览器时加入配置
browser = webdriver.Chrome(options=options)
# 打开百度
browser.get('https://www.zulutrade.com/login')
# 等待加载，最多等待20秒
browser.implicitly_wait(20)