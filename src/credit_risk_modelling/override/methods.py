import pandas as pd

from io import BytesIO

from ..plotting import utils as plotting
from .. import cfg, utils, validation


class Override:
	def __init__(self, df: pd.DataFrame, grade_1: str, grade_2: str):
		self.df = self.__validate_df(df=df, grade_1=grade_1, grade_2=grade_2)
		self.grade_1 = grade_1
		self.grade_2 = grade_2
		self.df_override = self.__create_df_override()
		self.result_list = self.__get_result_list()

	def __repr__(self):
		return f"{self.__class__.__name__}: {self.result_list.__repr__()}"

	def __append_result_list(self, result_list: list, dict_to_append: dict) -> None:
		utils.help_append_result_list(
			result_list=result_list,
			dict_to_append=dict_to_append,
			cols=cfg.COLS_OVERRIDE,
			name=self.__class__.__name__
		)

	def __create_df_override(self) -> pd.DataFrame:
		return pd.DataFrame({self.grade_1: self.df[self.grade_1], self.grade_2: self.df[self.grade_2]})

	def __get_result_list(self) -> list:
		result_list = []
		dict_to_append = utils.help_calculate_statistics_movement(df=self.df_override, name=self.__class__.__name__)
		validation.validate_cohort(self.__class__.__name__, input_dict=dict_to_append)
		self.__append_result_list(result_list=result_list, dict_to_append=dict_to_append)
		return result_list

	def __validate_df(self, df: pd.DataFrame, grade_1: str, grade_2: str) -> pd.DataFrame:
		df = validation.validate_missing_value(name=self.__class__.__name__, df=df, col=grade_1)
		df = validation.validate_missing_value(name=self.__class__.__name__, df=df, col=grade_2)
		return df

	def plot(
			self,
			x_axis_label: str = "Grade After Override",
			y_axis_label: str = "Grade Before Override",
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
		df.crm.override(grade_1="GRADE_1", grade_2="GRADE_2").plot()
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
			Returns a "heatmap" override matrix.
		"""
		# Preparation
		df, value_counts = utils.help_preparation(
			df=self.df_override,
			values=1,
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
		df.crm.override(grade_1="GRADE_1", grade_2="GRADE_2").table()
		```

		Returns:
			Returns a table containing the number of observations, the rating grade upgrades, and the rating grade \
			downgrades.
		"""
		return pd.DataFrame(self.result_list)
