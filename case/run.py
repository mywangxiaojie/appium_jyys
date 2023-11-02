
import sys 
sys.path.append("..") 
from start_session import driver

from test_password_set_alert import TestPasswordSetAlert
from test_order_reserve import TestOrderReserve
from test_login import TestLogin

import unittest

def run():
    suite = unittest.TestSuite()
    suite.addTest(TestLogin("test_login"))
    suite.addTest(TestPasswordSetAlert("test_0_title_and_message"))
    suite.addTest(TestPasswordSetAlert("test_1_cancel_btn"))
    suite.addTest(TestPasswordSetAlert("test_3_notice"))
    suite.addTest(TestOrderReserve("test_2_order_search"))
    unittest.TextTestRunner(verbosity=3).run(suite)


if __name__ == "__main__":
    run()
