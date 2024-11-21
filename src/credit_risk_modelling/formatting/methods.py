import pandas as pd

from typing import Union

from . import utils as formatting
from .. import cfg


class Formatting:
	def __init__(self, df: pd.DataFrame):
		self.df = df

	def df_to_tbl(self, label: str = "") -> list:
		"""
		Minimal working example:

		```py
		df.crm.formatting().df_to_tbl()
		```

		Args:
			label: Defines the top left entry of the resulting table.

		Returns:
			Returns the DataFrame as a list to be used by the Python package "docxtpl" to create a table in a Word \
			document.
		"""
		df = self.df.copy()
		cols = [label] + list(df.columns)
		tbl_list = [{"LABEL": cols[0], "COLS": cols[1:]}]
		for label in df.index:
			cols = df.loc[label, :].tolist()
			tbl_list.append({"LABEL": label, "COLS": cols})
		return tbl_list

	def format_cols(
			self,
			int_cols: Union[str, list] = None,
			float_cols: Union[str, list] = None,
			float_digits: int = 1,
			pct_cols: Union[str, list] = None,
			pct_digits: int = 1,
			date_cols: Union[str, list] = None,
			date_format: str = cfg.DATE_FORMAT,
			date_format_upper: bool = False,
			shift_index: bool = False
	) -> pd.DataFrame:
		"""
		Minimal working example:

		```py
		df.crm.formatting().format_cols()
		```

		Args:
			int_cols: Defines the columns to be formatted as integers, i.e. ",.0f".
			float_cols: Defines the columns to be formatted as floats, i.e. ",.<float_digits\>f".
			float_digits: Defines the number of float digits.
			pct_cols: Defines the columns to be formatted as percentage, i.e. ",.<percentage_digits\>%".
			pct_digits: Defines the number of percentage digits.
			date_cols: Defines the columns to be formatted as date, i.e., for example, "<%d.%m.%Y>".
			date_format: Defines the date format.
			date_format_upper: Transforms the date to uppercase.
			shift_index: Shifts the index by one.

		Returns:
			Returns the formatted DataFrame.
		"""
		df = (
			self.df.copy()
			.pipe(formatting.format_cols_num, cols=int_cols)
			.pipe(formatting.format_cols_num, cols=float_cols, digits=float_digits)
			.pipe(formatting.format_cols_num, cols=pct_cols, digits=pct_digits, kind="%")
			.pipe(
				formatting.format_cols_date,
				cols=date_cols,
				date_format=date_format,
				date_format_upper=date_format_upper
			)
		)
		if shift_index:
			df.index = df.index + 1
		return df
