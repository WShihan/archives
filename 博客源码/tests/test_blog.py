from unittest import TestCase
import unittest
from Mylog.store.blog import BlogService


_blogService = BlogService()


class ServiceTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_get_all(self):
        # all = _blogService.get_all()
        # self.assertIsInstance(all, list)
        pass


if __name__ == '__main__':
    unittest.main()
