import pandas as pd

from io import BytesIO

from ..plotting import utils as plotting
from .. import cfg, utils, validation


class Migration:
	def __init__(self, df: pd.DataFrame, grade: str, date: str, cohort: str):
		validation.validate_dimension_2(name=self.__class__.__name__, df=df, col=date)

		self.df = self.__validate_df(df=df, grade=grade)
		self.grade = grade
		self.date = date
		self.cohort = cohort
		self.df_migration = self.__create_df_migration()
		self.result_list = self.__get_result_list()

	def __repr__(self):
		return f"{self.__class__.__name__}: {self.result_list.__repr__()}"

	def __append_result_list(self, result_list: list, dict_to_append: dict) -> None:
		utils.help_append_result_list(
			result_list=result_list,
			dict_to_append=dict_to_append,
			cols=cfg.COLS_MIGRATION,
			name=self.__class__.__name__
		)

	def __create_df_migration(self) -> pd.DataFrame:
		return pd.crosstab(
			index=self.df[self.cohort], columns=self.df[self.date], values=self.df[self.grade], aggfunc="max"
		)

	def __get_result_list(self) -> list:
		result_list = []
		dict_to_append = utils.help_calculate_statistics_movement(df=self.df_migration, name=self.__class__.__name__)
		validation.validate_cohort(self.__class__.__name__, input_dict=dict_to_append)
		self.__append_result_list(result_list=result_list, dict_to_append=dict_to_append)
		return result_list

	def __validate_df(self, df: pd.DataFrame, grade: str) -> pd.DataFrame:
		df = validation.validate_missing_value(name=self.__class__.__name__, df=df, col=grade)
		return df

	def plot(
			self,
			x_axis_label: str = "Second Reporting Date",
			y_axis_label: str = "First Reporting Date",
			grade_range: list = None,
			annotation: bool = True,
			font_size: int = 7,
			fig_size: tuple = (7.5, 7.5),
			path: str = None,
			show: bool = False
	) -> BytesIO:
		"""
		Minimal working example:

		```py
		df.crm.migration(grade="GRADE", date="DATE", cohort="cohort").plot()
		```

		Args:
			x_axis_label: Defines the x-axis label.
			y_axis_label: Defines the y-axis label.
			grade_range: Extends the grade range to the specified range. Use "cfg.GRADES" for the complete range.
			annotation: Adds a "Downgrade" and "Upgrade" box to the plot.
			font_size: Defines the font size of the plot.
			fig_size: Defines the figure size.
			path: Defines the saving path including the filename of the figure and should be entered as \
			r"C:\<path\>\<filename\>.<image_format\>".
			show: If True, plot is shown.

		Returns:
			Returns a "heatmap" migration matrix.
		"""
		# Preparation
		df, value_counts = utils.help_preparation(
			df=self.df_migration,
			values=self.df_migration.index,
			grade_range=grade_range
		)
		# Initialise plot
		fig_bytes, (fig, ax) = plotting.plot_initialise(fig_size=fig_size)
		ax.axis("off")
		# Plot
		plotting.plot_heatmap_wrapper_wrapper(
			df=df,
			value_counts=value_counts,
			x_axis_label=x_axis_label,
			y_axis_label=y_axis_label,
			font_size=font_size,
			annotation=annotation
		)
		# Save plot
		plotting.plot_save(fig_bytes=fig_bytes, path=path)
		# Close plot
		plotting.plot_close(show=show)
		return fig_bytes

	def table(self) -> pd.DataFrame:
		"""
		Minimal working example:

		```py
		df.crm.migration(grade="GRADE", date="DATE", cohort="COHORT").table()
		```

		Returns:
			Returns a table containing the number of observations two dates, the cohort outflows, the cohort inflows, \
			the rating grade upgrades, the rating grade downgrades, the multi grade migration rate, and the downgrade \
			migration rate.
		"""
		return pd.DataFrame(self.result_list)
