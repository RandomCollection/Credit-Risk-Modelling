import numpy as np
import pandas as pd
import unittest

import credit_risk_modelling as crm


class TestDiscrimination(unittest.TestCase):
	def setUp(self) -> None:
		self.df = pd.DataFrame(
			{
				"DEFAULT": [0, 0, 1, 1],
				"GRADE_PD": [0.0007, 0.0013, 0.0225, 1.0000]
			}
		)

	def test_Discrimination(self) -> None:
		self.assertEqual(
			first=str(self.df.crm.discrimination(default="DEFAULT", score="GRADE_PD")),
			second=(
				"Discrimination: [{'BY': None, 'OBS': 4, 'DEFAULT_OBS': 2, 'AR': np.float64(1.0), "
				"'AR_BOUND_LOWER': None, 'AR_BOUND_UPPER': None, 'ALPHA': None}]"
			)
		)

	def test_table(self) -> None:
		pd.testing.assert_frame_equal(
			left=self.df.crm.discrimination(default="DEFAULT", score="GRADE_PD", alpha=0.1).table(),
			right=pd.DataFrame(
				data={
					"BY": None,
					"OBS": 4,
					"DEFAULT_OBS": 2,
					"AR": np.float64(1.0),
					"AR_BOUND_LOWER": np.float64(1.0),
					"AR_BOUND_UPPER": np.float64(1.0),
					"ALPHA": 0.1
				},
				index=[0]
			)
		)

	def test_utils_calculate_statistics_discrimination(self) -> None:
		self.assertEqual(
			first=crm.discrimination.utils.calculate_statistics_discrimination(
				default=self.df["DEFAULT"], score=self.df["GRADE_PD"], alpha=0.1
			),
			second={
				"OBS": 4,
				"DEFAULT_OBS": 2,
				"AR": np.float64(1.0),
				"AR_BOUND_LOWER": np.float64(1.0),
				"AR_BOUND_UPPER": np.float64(1.0),
				"ALPHA": 0.1
			}
		)

	def tearDown(self) -> None:
		del self.df


if __name__ == "__main__":
	unittest.main()
