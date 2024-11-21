import pandas as pd
import unittest


class TestFormatting(unittest.TestCase):
	def setUp(self) -> None:
		self.df = pd.DataFrame(
			{
				"INT": [1, 2.0, 3.5],
				"FLOAT": [1.0, 2.3, 3.9999],
				"PCT": [0.1, 0.8, 3.5],
				"DATE": [pd.Timestamp(2024, 1, 1), pd.Timestamp(2024, 3, 1), pd.Timestamp(2024, 5, 23)],
			}
		)

	def test_format_cols(self) -> None:
		pd.testing.assert_frame_equal(
			left=(
				self.df
				.crm.formatting().format_cols(
					int_cols="INT",
					float_cols="FLOAT", float_digits=2,
					pct_cols="PCT", pct_digits=0,
					date_cols="DATE", date_format="%d %b %Y",
					shift_index=True
				)
			),
			right=pd.DataFrame(
				data={
					"INT": ["1", "2", "4"],
					"FLOAT": ["1.00", "2.30", "4.00"],
					"PCT": ["10%", "80%", "350%"],
					"DATE": ["01 Jan 2024", "01 Mar 2024", "23 May 2024"],
				},
				index=[1, 2, 3]
			)
		)

	def test_df_to_tbl(self) -> None:
		self.assertEqual(
			first=(
				self.df
				.crm.formatting().format_cols(
					int_cols="INT",
					float_cols="FLOAT", float_digits=2,
					pct_cols="PCT", pct_digits=0,
					date_cols="DATE", date_format="%d %b %Y",
					shift_index=True
				)
				.crm.formatting().df_to_tbl(label="Data")
			),
			second=[
				{"LABEL": "Data", "COLS": ["INT", "FLOAT", "PCT", "DATE"]},
				{"LABEL": 1, "COLS": ["1", "1.00", "10%", "01 Jan 2024"]},
				{"LABEL": 2, "COLS": ["2", "2.30", "80%", "01 Mar 2024"]},
				{"LABEL": 3, "COLS": ["4", "4.00", "350%", "23 May 2024"]}
			]
		)

	def tearDown(self) -> None:
		del self.df


if __name__ == "__main__":
	unittest.main()
