import unittest
import assignment3

SAMPLE_RATIO = 1e6

# START_DATE = '2020-04-01'
START_DATE = '2021-04-01'
END_DATE = '2022-04-30'

class A3Test(unittest.TestCase):
    def runTest(self):
        assignment3.run(countries_csv_name='a3-countries.csv', countries=['Afghanistan','Sweden','Japan'], sample_ratio= SAMPLE_RATIO, start_date= START_DATE, end_date= END_DATE)

unittest.main()
