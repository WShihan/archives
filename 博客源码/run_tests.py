import unittest

# 执行测试，包括浏览器环境测试及单元测试
# Discover and run all tests in the tests package
if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    runner = unittest.TextTestRunner()
    runner.run(suite)

