import pandas as pd
import unittest

import credit_risk_modelling as crm


class TestOverride(unittest.TestCase):
	def setUp(self) -> None:
		self.df = crm.load_data.load_data().loc[lambda df: df["DATE"].dt.year == 2023]

	def test_Override(self) -> None:
		self.assertEqual(
			first=str(self.df.crm.override(grade_1="GRADE", grade_2="OVERRIDE")),
			second=(
				"Override: [{'OBS_1': np.int64(1000), 'OUTFLOWS': 0, 'OBS_1_COHORT': np.int64(1000), "
				"'OBS_2': np.int64(1000), 'INFLOWS': 0, 'OBS_2_COHORT': np.int64(1000), 'UNCHANGED': np.int64(929), "
				"'UP_1': np.int64(9), 'UP_2': np.int64(7), 'UP_3': np.int64(3), 'UP_>3': np.int64(12), "
				"'UP_TOTAL': np.int64(31), 'DOWN_1': np.int64(13), 'DOWN_2': np.int64(8), 'DOWN_3': np.int64(4), "
				"'DOWN_>3': np.int64(15), 'DOWN_TOTAL': np.int64(40), 'MR': 0.049, 'DR': 0.5510204081632653}]"
			)
		)
		
	def test_table(self) -> None:
		pd.testing.assert_frame_equal(
			left=self.df.crm.override(grade_1="GRADE", grade_2="OVERRIDE").table(),
			right=pd.DataFrame(
				data={
					"OBS_1": [1_000],
					"OUTFLOWS": [0],
					"OBS_1_COHORT": [1_000],
					"OBS_2": [1_000],
					"INFLOWS": [0],
					"OBS_2_COHORT": [1_000],
					"UNCHANGED": [929],
					"UP_1": [9],
					"UP_2": [7],
					"UP_3": [3],
					"UP_>3": [12],
					"UP_TOTAL": [31],
					"DOWN_1": [13],
					"DOWN_2": [8],
					"DOWN_3": [4],
					"DOWN_>3": [15],
					"DOWN_TOTAL": [40],
					"MR": [0.049],
					"DR": [0.55102],
				},
				index=[0]
			)
		)

	def tearDown(self) -> None:
		del self.df


if __name__ == "__main__":
	unittest.main()
