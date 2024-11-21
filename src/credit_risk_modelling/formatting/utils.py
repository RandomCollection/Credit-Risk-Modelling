import pandas as pd

from typing import Union

from .. import cfg, validation


def format_cols_date(
		df: pd.DataFrame,
		cols: Union[str, list],
		date_format: str = cfg.DATE_FORMAT,
		date_format_upper: bool = False
) -> pd.DataFrame:
	if cols is None:
		cols = []
	if type(cols) is str:
		cols = [cols]
	for col in cols:
		last_col_entry = df.iloc[-1, df.columns.get_loc(col)]
		if (type(last_col_entry) is str) and (last_col_entry.isin([cfg.MEAN, cfg.SUM])):
			slicer = -1
		else:
			slicer = None
		try:
			df = df.assign(
				**{
					col: lambda _df:
					pd.to_datetime(_df.iloc[:slicer, _df.columns.get_loc(col)]).dt.strftime(date_format).str.upper()
					if date_format_upper
					else pd.to_datetime(_df.iloc[:slicer, _df.columns.get_loc(col)]).dt.strftime(date_format)
				}
			)
		except AttributeError:
			raise AttributeError(validation.MESSAGES[5].format(col=col))
		except ValueError:
			raise ValueError(validation.MESSAGES[6])
	return df


def format_cols_num(df: pd.DataFrame, cols: Union[str, list], digits: int = 0, kind: str = "f") -> pd.DataFrame:
	if cols is None:
		cols = []
	if type(cols) is str:
		cols = [cols]
	for col in cols:
		last_col_entry = df.iloc[-1, df.columns.get_loc(col)]
		if (type(last_col_entry) is str) and (last_col_entry.isin([cfg.MEAN, cfg.SUM])):
			slicer = -1
		else:
			slicer = None
		try:
			df = df.assign(
				**{
					col: lambda _df:
					_df.iloc[:slicer, _df.columns.get_loc(col)].apply(lambda x: f"{x:,.{digits}{kind}}")
				}
			)
		except ValueError:
			raise ValueError(validation.MESSAGES[7].format(col=col))
	return df
