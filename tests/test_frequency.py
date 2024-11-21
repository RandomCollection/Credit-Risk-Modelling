import pandas as pd
import unittest

import credit_risk_modelling as crm


class TestFrequency(unittest.TestCase):
	def setUp(self) -> None:
		self.df = crm.load_data.load_data()

	def test_1(self) -> None:
		pd.testing.assert_frame_equal(
			left=(
				self.df
				.crm.frequency(index="GRADE")
				.table(add_sum=True)
				.tail(2)
			),
			right=pd.DataFrame(
				data={
					"GRADE": ["D", "Sum"],
					"GRADE_ABS": [492.0, 4_150.0],
					"GRADE_PCT": [0.118554, 1.0],
				},
				index=[7, 8]
			)
		)

	def test_2(self) -> None:
		pd.testing.assert_frame_equal(
			left=(
				self.df
				.crm.frequency(index="GRADE", column="DATE")
				.table(add_sum=True)
				.tail(2)
				.iloc[:, :3]
			),
			right=pd.DataFrame(
				data={
					"GRADE": ["D", "Sum"],
					"2019-12-31_ABS": [74.0, 750.0],
					"2019-12-31_PCT": [0.098667, 1.0],
				},
				index=[7, 8]
			)
		)

	def test_3(self) -> None:
		pd.testing.assert_frame_equal(
			left=(
				self.df
				.crm.frequency(index="GRADE", column="DATE", cohort="ID")
				.table(add_sum=True)
				.tail(2)
				.iloc[:, :3]
			),
			right=pd.DataFrame(
				data={
					"GRADE": ["D", "Sum"],
					"2019-12-31_ABS": [27.0, 265.0],
					"2019-12-31_PCT": [0.101887, 1.0],
				},
				index=[7, 8]
			)
		)

	def test_4(self) -> None:
		pd.testing.assert_frame_equal(
			left=(
				self.df
				.crm.frequency(index="GRADE", column="DATE", cohort="ID")
				.table(index_range=crm.cfg.GRADES, sort_by_list=crm.cfg.GRADES, add_sum=True)
				.tail(2)
				.iloc[:, :3]
			),
			right=pd.DataFrame(
				data={
					"GRADE": ["D", "Sum"],
					"2019-12-31_ABS": [27.0, 265.0],
					"2019-12-31_PCT": [0.101887, 1.0],
				},
				index=[7, 8]
			)
		)

	def tearDown(self) -> None:
		del self.df


if __name__ == "__main__":
	unittest.main()
