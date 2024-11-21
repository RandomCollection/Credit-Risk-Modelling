import numpy as np
import pandas as pd

from . import utils as frequency
from .. import cfg, utils


class Frequency:
	def __init__(self, df: pd.DataFrame, index: str, column: str = None, value: str = None, cohort: str = None):
		self.df = df
		self.index = index
		self.column = column
		self.value = value
		self.cohort = cohort
		self.df_frequency = self.__create_df_frequency()

	def __repr__(self):
		return f"{self.__class__.__name__}: {self.df_frequency.__repr__()}"

	def __create_df_frequency(self) -> pd.DataFrame:
		return frequency.calculate_statistics_frequency(
			df=self.df, index=self.index, column=self.column, value=self.value, cohort=self.cohort
		)

	def table(
		self,
		index_range: list = None,
		df_ext: pd.DataFrame = None,
		sort_by_col: str = None,
		sort_by_list: list = None,
		sort_asc: bool = True,
		add_sum: bool = False
	) -> pd.DataFrame:
		"""
		Minimal working example:

		```py
		df.crm.frequency(index="GRADE").table()
		```

		Args:
			index_range: Extends the index range. In case of grades, for example, the index can be extended for \
			missing grades via, for example, "constants.GRADES" to get the complete range.
			df_ext: Adds data (columns) to the resulting DataFrame. Hence, dimensions of df_ext need to be defined \
			accordingly. Optimally, data in df_ext is already given in percentages.
			sort_by_col: Defines the column to sort.
			sort_by_list: Defines the list to sort in case of categorical items which have no intrinsic sorting order.
			sort_asc: Sorts the previously defined column or list ascending.
			add_sum: Adds a sum row to the DataFrame.

		Returns:
			Returns a frequency table. Generally, returns index per columns in absolute and percentage values.
		"""
		df_int = self.df_frequency.copy()
		if index_range is not None:
			df_int = self.df_frequency.reindex(pd.Index(index_range))
		df = pd.DataFrame()
		for i in range(0, len(df_int.columns)):
			try:
				df_app = pd.DataFrame(
					{
						df_int.columns[i].strftime(cfg.DATE_FORMAT) + "_ABS":
							df_int.iloc[:, i],
						df_int.columns[i].strftime(cfg.DATE_FORMAT) + "_PCT":
							df_int.iloc[:, i] / df_int.iloc[:, i].sum(),
					}
				)
			except AttributeError:
				df_app = pd.DataFrame(
					{
						str(df_int.columns[i]) + "_ABS":
							df_int.iloc[:, i],
						str(df_int.columns[i]) + "_PCT":
							df_int.iloc[:, i] / df_int.iloc[:, i].sum(),
					}
				)
			df = pd.concat([df, df_app], axis=1, sort=True)
		if df_ext is not None:
			df = pd.concat([df, df_ext], axis=1, sort=True)
		df.replace(np.nan, 0, inplace=True)
		df = df.rename_axis(self.index).reset_index()
		if sort_by_col is not None:
			df.sort_values(by=sort_by_col, ascending=sort_asc, inplace=True)
		if sort_by_list is not None:
			df = utils.help_sort_by_list(df=df, col=self.index, sort_by_list=sort_by_list, sort_asc=sort_asc)
		if add_sum:
			df = utils.help_add_sum(df=df)
		return df
