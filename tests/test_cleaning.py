import numpy as np
import pandas as pd
import unittest

import credit_risk_modelling as crm


class TestCleaning(unittest.TestCase):
	def setUp(self) -> None:
		self.df = pd.DataFrame(
			data={
				"NAME": ["alice", "alice", " bob", "carol _", " dave"],
				" age": [29, 29, 55, 18, 9],
				"Sex ": ["", "", "None", "female   ", "   "],
				"_ hEiGhT": [167, 167, 178, 174, None],
			},
			index=[0, 4, 6, 18, 89]
		)

	def test_change_column_names(self) -> None:
		self.assertSequenceEqual(
			seq1=crm.cleaning.change_column_names(df=self.df, style="upper").columns.tolist(),
			seq2=["NAME", " AGE", "SEX ", "_ HEIGHT"]
		)
		self.assertSequenceEqual(
			seq1=crm.cleaning.change_column_names(df=self.df, style="lower").columns.tolist(),
			seq2=["name", " age", "sex ", "_ height"]
		)
		self.assertSequenceEqual(
			seq1=crm.cleaning.change_column_names(df=self.df, style="unchanged").columns.tolist(),
			seq2=["NAME", " age", "Sex ", "_ hEiGhT"]
		)
		with self.assertRaises(expected_exception=ValueError):
			crm.cleaning.change_column_names(df=self.df, style="fail")

	def test_clean(self) -> None:
		pd.testing.assert_frame_equal(
			left=crm.cleaning.clean(df=self.df),
			right=pd.DataFrame(
				data={
					"NAME": ["alice", "bob", "carol _", "dave"],
					"AGE": [29, 55, 18, 9],
					"SEX": [np.nan, np.nan, "female", np.nan],
					"_ HEIGHT": [167, 178, 174, np.nan],
				},
				index=[0, 1, 2, 3]
			)
		)

	def drop_duplicates(self) -> None:
		self.assertEqual(
			first=len(crm.cleaning.drop_duplicates(df=self.df, drop=True)),
			second=4
		)
		self.assertEqual(
			first=len(crm.cleaning.drop_duplicates(df=self.df, drop=False)),
			second=5
		)
		with self.assertRaises(expected_exception=ValueError):
			crm.cleaning.drop_duplicates(df=self.df, drop="fail")

	def test_reset_index(self) -> None:
		self.assertSequenceEqual(
			seq1=crm.cleaning.reset_index(df=self.df).index.tolist(),
			seq2=[0, 1, 2, 3, 4]
		)

	def test_strip_strings(self) -> None:
		self.assertSequenceEqual(
			seq1=crm.cleaning.strip_strings(df=self.df).columns.tolist(),
			seq2=["NAME", "age", "Sex", "_ hEiGhT"]
		)
		self.assertSequenceEqual(
			seq1=crm.cleaning.strip_strings(df=self.df)["NAME"].tolist(),
			seq2=["alice", "alice", "bob", "carol _", "dave"]
		)
		self.assertSequenceEqual(
			seq1=crm.cleaning.strip_strings(df=self.df)["Sex"].tolist(),
			seq2=["", "", "None", "female", ""]
		)

	def test_transform_missing_strings_to_nan(self) -> None:
		self.assertSequenceEqual(
			seq1=crm.cleaning.transform_missing_strings_to_nan(df=self.df)["NAME"].tolist(),
			seq2=["alice", "alice", " bob", "carol _", " dave"]
		)
		self.assertSequenceEqual(
			seq1=crm.cleaning.transform_missing_strings_to_nan(df=self.df)["Sex "].tolist(),
			seq2=[np.nan, np.nan, np.nan, "female   ", "   "]
		)

	def tearDown(self) -> None:
		del self.df


if __name__ == "__main__":
	unittest.main()
