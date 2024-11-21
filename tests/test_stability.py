import pandas as pd
import unittest

import credit_risk_modelling as crm


class TestStability(unittest.TestCase):
	def setUp(self) -> None:
		self.df = (
			crm.load_data.load_data()
			.loc[lambda df: df["DATE"].dt.year.isin([2022, 2023])]
			.crm.frequency(index="GRADE", column="DATE", cohort="ID")
			.table()
		)

	def test_table(self) -> None:
		pd.testing.assert_frame_equal(
			left=self.df.crm.stability(score_ref="2022-12-31_PCT", score="2023-12-31_PCT").table(add_sum=True).tail(2),
			right=pd.DataFrame(
				data={
					"GRADE": ["D", "Sum"],
					"2022-12-31_ABS": [108.0, 821.0],
					"2022-12-31_PCT": [0.131547, 1.0],
					"2023-12-31_ABS": [106.0, 821.0],
					"2023-12-31_PCT": [0.129111, 1.0],
					"PSI_2022-12-31_PCT-2023-12-31_PCT": [0.000045535037788435043, 0.009026197907522338],
				},
				index=[7, 8]
			)
		)

	def tearDown(self) -> None:
		del self.df


if __name__ == "__main__":
	unittest.main()
