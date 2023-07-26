import unittest

import pandas as pd
from main import fetch_housing_data, income_cat_proportions, load_housing_data


class TestHousingData(unittest.TestCase):
    def test_fetch_housing_data(self):
        # Test if data can be fetched and loaded correctly
        fetch_housing_data()
        self.assertTrue(os.path.exists("datasets/housing/housing.tgz"))

    def test_load_housing_data(self):
        # Test if data can be loaded correctly
        housing = load_housing_data()
        self.assertIsInstance(housing, pd.DataFrame)
        self.assertEqual(len(housing), 20640)
        self.assertEqual(len(housing.columns), 10)

    def test_income_cat_proportions(self):
        # Test the income category proportions function
        data = pd.DataFrame({"income_cat": [1, 2, 3, 3, 4, 4, 5]})
        proportions = income_cat_proportions(data)
        expected_proportions = pd.Series(
            {1: 1 / 7, 2: 1 / 7, 3: 2 / 7, 4: 2 / 7, 5: 1 / 7}
        )
        pd.testing.assert_series_equal(proportions, expected_proportions)


if __name__ == "__main__":
    unittest.main()
