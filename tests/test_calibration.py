import numpy as np
import pandas as pd
import unittest

import credit_risk_modelling as crm


class TestCalibration(unittest.TestCase):
	def setUp(self) -> None:
		self.df = pd.DataFrame(
			{
				"DEFAULT": [0, 0, 1, 1],
				"GRADE_PD": [0.0007, 0.0013, 0.0225, 1.0000]
			}
		)

	def test_Calibration(self) -> None:
		self.assertEqual(
			first=str(self.df.crm.calibration(default="DEFAULT", score="GRADE_PD")),
			second=(
				"Calibration: [{'BY': None, 'OBS': 4, 'DEFAULT_OBS': 2, 'DEFAULT_PRE': 1.0, 'PD_OBS': 0.5, "
				"'PD_PRE': 0.256125, 'GRADE_OBS': 'CCC', 'GRADE_PRE': 'CCC', 'GRADE_DIF': 0, "
				"'P_BINOM_UND': np.float64(0.27209574788437574), 'P_BINOM_OVE': np.float64(0.9457028701421882), "
				"'P_JEFFREYS': np.float64(0.133421055309482)}]"
			)
		)

	def test_table(self) -> None:
		pd.testing.assert_frame_equal(
			left=self.df.crm.calibration(default="DEFAULT", score="GRADE_PD").table(add_mean=True, add_sum=True),
			right=pd.DataFrame(
				data={
					"BY": [None, "Mean", "Sum"],
					"OBS": [4.0, 4.0, 4.0],
					"DEFAULT_OBS": [2.0, 2.0, 2.0],
					"DEFAULT_PRE": [1.0, 1.0, 1.0],
					"PD_OBS": [0.5, 0.5, 0.5],
					"PD_PRE": [0.256125, 0.256125, 0.256125],
					"GRADE_OBS": ["CCC", "CCC", "CCC"],
					"GRADE_PRE": ["CCC", "CCC", "CCC"],
					"GRADE_DIF": [0, 0, 0],
					"P_BINOM_UND": [0.27209574788437574, 0.27209574788437574, 0.27209574788437574],
					"P_BINOM_OVE": [0.9457028701421882, 0.9457028701421882, 0.9457028701421882],
					"P_JEFFREYS": [0.133421055309482, 0.133421055309482, 0.133421055309482],
					"CT_PD_OBS": [0.5, 0.5, 0.5],
					"CT_PD_PRE": [0.256125, 0.256125, 0.256125],
				},
				index=[0, 1, 2]
			)
		)

	def test_utils_calculate_statistics_calibration(self) -> None:
		self.assertEqual(
			first=crm.calibration.utils.calculate_statistics_calibration(
				default=self.df["DEFAULT"], score=self.df["GRADE_PD"]
			),
			second={
				"OBS": 4,
				"DEFAULT_OBS": 2,
				"PD_OBS": 0.5,
				"PD_PRE": 0.256125,
				"DEFAULT_PRE": 1.0,
				"GRADE_OBS": "CCC",
				"GRADE_PRE": "CCC",
				"GRADE_DIF": 0,
				"P_BINOM_UND": np.float64(0.27209574788437574),
				"P_BINOM_OVE": np.float64(0.9457028701421882),
				"P_JEFFREYS": np.float64(0.133421055309482)
			}
		)

	def tearDown(self) -> None:
		del self.df


if __name__ == "__main__":
	unittest.main()
