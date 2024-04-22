#!usr/bin/python3.12.2
# -*-  coding: utf-8 -*-
#
# @Time    : 2024/4/21 下午11:29
# @Author  : KeFang
# @Email   : 19130728969@163.com
# @File    : text.py
# Software : PyCharm
import throw
import unittest


class Text(unittest.TestCase):
    def test_text(self):
        waning = throw.warning()
        info = throw.info()
        error = throw.error()
        self.assertEqual(waning, "warning为空")
        self.assertEqual(info, "info为空")
        self.assertEqual(error, "error为空")
        error = throw.error("ValueError")
        self.assertEqual(error, "error为空")
        waning = throw.warning("*arge")
        info = throw.info("arge not find")
        self.assertEqual(waning, None)
        self.assertEqual(info, None)


if __name__ == '__main__':
    unittest.main()
