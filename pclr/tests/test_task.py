import unittest
from pclr.main import get_ten


class FlowTests(unittest.TestCase):
    def test_flow_get_ten(self):
        self.assertEqual(10, get_ten.run())
