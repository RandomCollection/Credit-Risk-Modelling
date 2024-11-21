import unittest

import credit_risk_modelling as crm


class TestData(unittest.TestCase):
	def test_load_data(self) -> None:
		self.assertIsNotNone(obj=crm.load_data.load_data())


if __name__ == "__main__":
	unittest.main()
