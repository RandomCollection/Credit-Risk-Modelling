import matplotlib.pyplot as plt
import pandas as pd

from io import BytesIO
from matplotlib.ticker import FuncFormatter, MultipleLocator
from sklearn.metrics import roc_curve
from typing import Union

from . import utils as discrimination
from ..plotting import utils as plotting
from .. import cfg, utils, validation


class Discrimination:
	def __init__(self, df: pd.DataFrame, default: str, score: str, alpha: float = None, by: str = None):
		validation.validate_binary(name=self.__class__.__name__, df=df, col=default)
		validation.validate_numeric(name=self.__class__.__name__, df=df, col=score)
		if alpha is not None:
			validation.validate_range_bt_0_1(name=self.__class__.__name__, x=alpha, x_name="alpha")

		self.df = self.__validate_df(df=df, default=default, score=score)
		self.default = default
		self.score = score
		self.alpha = alpha
		self.by = by
		self.result_list = self.__get_result_list()

	def __repr__(self):
		return f"{self.__class__.__name__}: {self.result_list.__repr__()}"

	def __append_result_list(self, result_list: list, dict_to_append: dict) -> None:
		utils.help_append_result_list(
			result_list=result_list,
			dict_to_append=dict_to_append,
			cols=cfg.COLS_DISCRIMINATION,
			name=self.__class__.__name__
		)

	def __get_result_list(self) -> list:
		if self.by is None:
			groups = [(None, self.df)]
		else:
			groups = self.df.groupby(by=self.by)
		result_list = []
		for i, group in groups:
			self.__append_result_list(
				result_list=result_list,
				dict_to_append={
					cfg.BY: i,
					**discrimination.calculate_statistics_discrimination(
						default=group[self.default], score=group[self.score], alpha=self.alpha
					)
				}
			)
		return result_list

	def __validate_df(self, df: pd.DataFrame, default: str, score: str) -> pd.DataFrame:
		df = validation.validate_missing_value(name=self.__class__.__name__, df=df, col=default)
		df = validation.validate_missing_value(name=self.__class__.__name__, df=df, col=score)
		return df

	def plot(
			self,
			x_axis_label: str = "1 - Specificity / Percentage of Ratings",
			y_axis_label: str = "Sensitivity / Percentage of Defaults",
			legend_label: Union[str, list] = None,
			score_2: str = None,
			legend_label_2: Union[str, list] = None,
			legend_loc: str = "lower right",
			fig_size: tuple = (7.5, 7.5),
			path: str = None,
			show: bool = False
	) -> BytesIO:
		"""
		Minimal working example:

		```py
		df.crm.discrimination(default="DEFAULT", score="SCORE").plot()
		```

		Args:
			x_axis_label: Defines the x-axis label.
			y_axis_label: Defines the y-axis label.
			legend_label: Defines the legend label.
			score_2: Defines a second score column.
			legend_label_2: Defines the legend label of the second score column.
			legend_loc: Defines the legend location.
			fig_size: Defines the figure size.
			path: Defines the saving path including the filename of the figure and should be entered as \
			r"C:\<path\>\<filename\>.<image_format\>".
			show: If True, plot is shown.

		Returns:
			Returns the ROC curve.
		"""
		# Change default colour cycle of matplotlib
		plt.rcParams["axes.prop_cycle"] = plt.cycler(color=cfg.COLOURS)
		# Initialise plot
		fig_bytes, (fig, ax) = plotting.plot_initialise(fig_size=fig_size)
		
		def help_plot(score: str, _legend_label: Union[str, list] = None) -> None:
			df_score = validation.validate_missing_value(name=self.__class__.__name__, df=self.df, col=self.default)
			df_score = validation.validate_missing_value(name=self.__class__.__name__, df=df_score, col=score)
			if self.by is None:
				fpr, tpr, thresholds = roc_curve(y_true=df_score[self.default], y_score=df_score[score])
				result = discrimination.calculate_statistics_discrimination(
					default=df_score[self.default], score=df_score[score]
				)
				if result[cfg.AR] is not None:
					if _legend_label is not None:
						plt.plot(fpr, tpr, label=f"{_legend_label}, AR: {result[cfg.AR]:.2f}")
					else:
						plt.plot(fpr, tpr, label=f"{score}, AR: {result[cfg.AR]:.2f}")
			if self.by is not None:
				groups = df_score.groupby(self.by)
				for i, group in enumerate(groups):
					fpr, tpr, thresholds = roc_curve(y_true=group[1][self.default], y_score=group[1][score])
					result = discrimination.calculate_statistics_discrimination(
						default=group[1][self.default], score=group[1][score]
					)
					if result[cfg.AR] is not None:
						if _legend_label is not None:
							assert len(_legend_label) == groups.ngroups, validation.MESSAGES[14].format(
								module=self.__class__.__name__, number_of_groups=groups.ngroups
							)
							plt.plot(fpr, tpr, label=f"{_legend_label[i]}, AR: {result[cfg.AR]:.2f}")
						elif type(group[0]) is not str:
							plt.plot(
								fpr,
								tpr,
								label=f"{group[0].strftime(cfg.DATE_FORMAT)}, AR: {result[cfg.AR]:.2f}"
							)
						else:
							plt.plot(fpr, tpr, label=f"{group[0]}, AR: {result[cfg.AR]:.2f}")

		# Plot
		# Score
		help_plot(score=self.score, _legend_label=legend_label)
		# Score 2
		if score_2 is not None:
			help_plot(score=score_2, _legend_label=legend_label_2)
		plt.plot([0, 1], [0, 1], "k--")
		# Legend
		ax.legend(edgecolor=cfg.COLOUR_BLACK, fancybox=False, loc=legend_loc)
		# Adjust plot
		ax.set_xlim(-0.05, 1.05)
		ax.set_ylim(-0.05, 1.05)
		ax.xaxis.set_major_locator(MultipleLocator(0.1))
		ax.yaxis.set_major_locator(MultipleLocator(0.1))
		ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.0%}"))
		ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.0%}"))
		plotting.plot_adjust(fig=fig, ax=ax, x_axis_label=x_axis_label, y_axis_label=y_axis_label)
		# Save plot
		plotting.plot_save(fig_bytes=fig_bytes, path=path)
		# Close plot
		plotting.plot_close(show=show)
		return fig_bytes

	def table(self) -> pd.DataFrame:
		"""
		Minimal working example:

		```py
		df.crm.discrimination(default="DEFAULT", score="SCORE").table()
		```

		Returns:
			Returns a table containing the AR, the left (lower) bound of the AR confidence interval, the right (upper) \
			bound of the AR confidence interval, the significance level, the number of observations, and the number of \
			observed defaults.
		"""
		return pd.DataFrame(self.result_list)
