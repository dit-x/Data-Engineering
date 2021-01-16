#!usr/python3.8
import unittest
import pandas as pd

# from pandas.util.testing import assert_frame_equal 
from pandas.testing import assert_frame_equal

class DFTests(unittest.TestCase):
    
    """ class for running unittests """

    def setUp(self):
        """ Your setUp """
        TEST_INPUT_DIR = ''
        test_file_name =  'customers.csv'
        try:
            data = pd.read_csv(TEST_INPUT_DIR + test_file_name,
                sep = ',',
                header = 0)
        except IOError:
            print('cannot open file')
        self.fixture = data

    def test_dataFrame_constructedAsExpected(self):
        """ Test that the dataframe read in equals what you expect"""
        foo = pd.read_csv('cus.csv')
        assert_frame_equal(self.fixture, foo)

if __name__ == "__main__":
    unittest.main()