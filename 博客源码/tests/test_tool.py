from unittest import TestCase
import unittest
import Mylog.util.tool as Tool

ip_checker = Tool.IPChecker()

class ServiceTest(TestCase):
    def setUp(self) -> None:
        pass

    # 测试获取ip信息
    def test_get_all(self):
        ip = ip_checker.get_baidu('198.144.180.189')
        self.assertIsInstance(ip, Tool.IP)

    def test_extract_device(self):
        ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'
        device = Tool.extract_device(ua)
        self.assertIsInstance(device, str)



if __name__ == '__main__':
    unittest.main()
    
    