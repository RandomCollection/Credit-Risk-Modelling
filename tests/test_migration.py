import pandas as pd
import unittest

import credit_risk_modelling as crm


class TestMigration(unittest.TestCase):
	def setUp(self) -> None:
		self.df = crm.load_data.load_data().loc[lambda df: df["DATE"].dt.year.isin([2022, 2023])]

	def test_Migration(self) -> None:
		self.assertEqual(
			first=str(self.df.crm.migration(grade="GRADE", date="DATE", cohort="ID")),
			second=(
				"Migration: [{'OBS_1': np.int64(900), 'OUTFLOWS': 79, 'OBS_1_COHORT': np.int64(821), "
				"'OBS_2': np.int64(1000), 'INFLOWS': 179, 'OBS_2_COHORT': np.int64(821), 'UNCHANGED': np.int64(575), "
				"'UP_1': np.int64(66), 'UP_2': np.int64(40), 'UP_3': np.int64(10), 'UP_>3': np.int64(15), "
				"'UP_TOTAL': np.int64(131), 'DOWN_1': np.int64(64), 'DOWN_2': np.int64(27), 'DOWN_3': np.int64(19), "
				"'DOWN_>3': np.int64(5), 'DOWN_TOTAL': np.int64(115), 'MR': 0.14129110840438489, "
				"'DR': 0.4396551724137931}]"
			)
		)

	def test_table(self) -> None:
		pd.testing.assert_frame_equal(
			left=self.df.crm.migration(grade="GRADE", date="DATE", cohort="ID").table(),
			right=pd.DataFrame(
				data={
					"OBS_1": [900],
					"OUTFLOWS": [79],
					"OBS_1_COHORT": [821],
					"OBS_2": [1_000],
					"INFLOWS": [179],
					"OBS_2_COHORT": [821],
					"UNCHANGED": [575],
					"UP_1": [66],
					"UP_2": [40],
					"UP_3": [10],
					"UP_>3": [15],
					"UP_TOTAL": [131],
					"DOWN_1": [64],
					"DOWN_2": [27],
					"DOWN_3": [19],
					"DOWN_>3": [5],
					"DOWN_TOTAL": [115],
					"MR": [0.141291],
					"DR": [0.439655],
				},
				index=[0]
			)
		)

	def tearDown(self) -> None:
		del self.df


if __name__ == "__main__":
	unittest.main()
