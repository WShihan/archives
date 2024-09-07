import unittest
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time

# 设置无头模式
opt = Options()
opt.add_argument("--headless")  # 启用无头模式
opt.add_argument("--no-sandbox")  # 解决DevToolsActivePort文件不存在的报错
opt.add_argument("--disable-dev-shm-usage")  # 解决资源不足的问题

driver = webdriver.Edge(options=None)
driver.maximize_window()

class UITest(unittest.TestCase):

    def tearDown(self) -> None:
        # 关闭浏览器
        driver.quit()
    
    def test_comment(self):
        print('执行评论测试！')
        id = 97670476
        driver.get(f'http://127.0.0.1:5000/blog/{id}')
        driver.implicitly_wait(10)

        # 填写表单
        nickname = driver.find_element(By.ID, 'nickname')
        nickname.send_keys('cmt_test')
        email = driver.find_element(By.ID, 'email')
        email.send_keys('3443327820@qq.com')
        site = driver.find_element(By.ID, 'site')
        site.send_keys('https://wsh233.cn')
        comment = driver.find_element(By.ID, 'comment')
        comment.send_keys('这是评论自动化测试！')

        time.sleep(3)
        # 点击提交
        submit=driver.find_element(By.XPATH,'//*[@id="cmt-submit"]')
        driver.execute_script("arguments[0].click();", submit)
        time.sleep(10)




if __name__ == '__main__':
    unittest.main()

