import pandas as pd

from typing import Union

from . import utils as stability
from .. import utils, validation


class Stability:
	def __init__(self, df: pd.DataFrame, score_ref: str, score: Union[str, list]):
		validation.validate_numeric(name=self.__class__.__name__, df=df, col=score_ref)
		if type(score) is str:
			score = [score]
		for i in range(0, len(score)):
			validation.validate_numeric(name=self.__class__.__name__, df=df, col=score[i])

		self.df = df
		self.score_ref = score_ref
		self.score = score
		self.df_stability = self.__create_df_stability()

	def __repr__(self):
		return f"{self.__class__.__name__}: {self.df_stability.__repr__()}"

	def __create_df_stability(self) -> pd.DataFrame:
		return stability.calculate_statistics_stability(df=self.df, score_ref=self.score_ref, score=self.score)

	def table(
		self,
		sort_by_col: str = None,
		sort_by_list: list = None,
		sort_asc: bool = True,
		add_sum: bool = False
	) -> pd.DataFrame:
		"""
		Minimal working example:

		```py
		df.crm.stability(score_ref="SCORE_REFERENCE", score="SCORE").table()
		```

		```py
		(
			df
			.crm.frequency(index="GRADE", column="DATE", cohort="ID")
			.table()
			.crm.stability(score_ref="SCORE_REF", score="SCORE")
			.table()
		)
		```

		Args:
			sort_by_col: Defines the column to sort.
			sort_by_list: Defines the list to sort in case of categorical items which have no intrinsic sorting order.
			sort_asc: Sorts the previously defined column or list ascending.
			add_sum: Adds a sum row to the DataFrame.

		Returns:
			Returns the PSI.
		"""
		if sort_by_col is not None:
			self.df_stability.sort_values(by=sort_by_col, ascending=sort_asc, inplace=True)
		if sort_by_list is not None:
			self.df_stability = utils.help_sort_by_list(
				df=self.df_stability, col=self.df_stability.columns[0], sort_by_list=sort_by_list, sort_asc=sort_asc
			)
		if add_sum:
			self.df_stability = utils.help_add_sum(df=self.df_stability)
		return self.df_stability
