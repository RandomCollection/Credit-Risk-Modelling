import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from io import BytesIO
from matplotlib.ticker import FuncFormatter
from scipy import stats

from . import utils as calibration
from ..plotting import utils as plotting
from .. import cfg, general, utils, validation


class Calibration:
	def __init__(self, df: pd.DataFrame, default: str, score: str, by: str = None):
		validation.validate_binary(name=self.__class__.__name__, df=df, col=default)
		validation.validate_numeric(name=self.__class__.__name__, df=df, col=score)

		self.df = self.__validate_df(df=df, default=default, score=score)
		self.default = default
		self.score = score
		self.by = by
		self.result_list = self.__get_result_list()

	def __repr__(self):
		return f"{self.__class__.__name__}: {self.result_list.__repr__()}"

	def __append_result_list(self, result_list: list, dict_to_append: dict) -> None:
		utils.help_append_result_list(
			result_list=result_list,
			dict_to_append=dict_to_append,
			cols=cfg.COLS_CALIBRATION,
			name=self.__class__.__name__
		)

	def __get_result_list(self) -> list:
		if self.by is None:
			groups = [(None, self.df)]
		elif set(self.df[self.by]).issubset(cfg.GRADES):
			self.df.sort_values(by=self.by, key=lambda x: x.map(cfg.GRADES_ORDER), inplace=True)
			groups = self.df.groupby(by=self.by, sort=False)
		else:
			groups = self.df.groupby(by=self.by)
		result_list = []
		for i, group in groups:
			self.__append_result_list(
				result_list=result_list,
				dict_to_append={
					cfg.BY: i,
					**calibration.calculate_statistics_calibration(default=group[self.default], score=group[self.score])
				}
			)
		return result_list

	def __validate_df(self, df: pd.DataFrame, default: str, score: str) -> pd.DataFrame:
		df = validation.validate_missing_value(name=self.__class__.__name__, df=df, col=default)
		df = validation.validate_missing_value(name=self.__class__.__name__, df=df, col=score)
		return df

	def plot(
			self,
			x_axis_label: str = "Predicted Probability of Default",
			y_axis_label: str = "Observed Probability of Default",
			annotation: bool = True,
			annot_xy: tuple = None,
			legend_loc: str = "upper left",
			fig_size: tuple = (7.5, 7.5),
			path: str = None,
			show: bool = False
	) -> BytesIO:
		"""
		Minimal working example:

		```py
		df.crm.calibration(default="DEFAULT", score="SCORE", by="GRADE").plot()
		```

		Args:
			x_axis_label: Defines the x-axis label.
			y_axis_label: Defines the y-axis label.
			annotation: Adds a "Progressive" and "Conservative" box to the plot.
			annot_xy: Adds annotations to data points provided as relative x- and y-positions, i.e. to be entered as \
			(float, float).
			legend_loc: Defines the legend location.
			fig_size: Defines the figure size.
			path: Defines the saving path including the filename of the figure and should be entered as \
			r"C:\<path\>\<filename\>.<image_format\>".
			show: If True, plot is shown.

		Returns:
			Returns a "calibration" plot.
		"""
		# Initialise plot
		fig_bytes, (fig, ax) = plotting.plot_initialise(fig_size=fig_size)
		# Plot
		df = self.table()
		df[cfg.PD_OBS] = df[cfg.PD_OBS].replace(0, np.nan)
		plotting.plot_plot_wrapper(
			df=df[[cfg.PD_OBS, cfg.PD_PRE]],
			kind="line",
			ax=ax,
			markeredgewidth=0.75,
			markeredgecolor=cfg.COLOUR_BLACK
		)
		df[cfg.PD_OBS] = df[cfg.PD_OBS].replace(np.nan, 0.0001)
		plotting.plot_plot_wrapper(
			df=df.loc[df[cfg.PD_OBS] == 0.0001, [cfg.PD_OBS, cfg.PD_PRE]],
			kind="scatter",
			ax=ax,
			s=50,
			linewidth=0.75,
			edgecolor=cfg.COLOUR_BLACK,
			label="_nolegend_"
		)
		plt.plot([0, 1], [0, 1], "k--")
		# Legend
		plotting.plot_legend(ax=ax, legend_label=["Observed Calibration", "Perfect Calibration"], legend_loc=legend_loc)
		# Adjust plot
		ax.set_xlim(0.0001, 1)
		ax.set_ylim(0.0001, 1)
		ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.1%}" if x == 0.001 else f"{x:.0%}"))
		ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.1%}" if x == 0.001 else f"{x:.0%}"))
		if annotation:
			plotting.plot_add_text(ax=ax, x=0.001, y=0.1, s="Progressive")
			plotting.plot_add_text(ax=ax, x=0.1, y=0.001, s="Conservative")
		if annot_xy is not None:
			if np.issubdtype(df[cfg.BY].dtype, np.datetime64):
				df[cfg.BY] = df[cfg.BY].apply(lambda x: x.strftime(cfg.DATE_FORMAT))
			for i, txt in enumerate(df[cfg.BY]):
				ax.annotate(
					txt,
					xy=(df[cfg.PD_PRE][i], df[cfg.PD_OBS][i]),
					xytext=annot_xy,
					textcoords="offset points"
				)
		plotting.plot_adjust(fig=fig, ax=ax, x_axis_label=x_axis_label, y_axis_label=y_axis_label)
		# Save plot
		plotting.plot_save(fig_bytes=fig_bytes, path=path)
		# Close plot
		plotting.plot_close(show=show)
		return fig_bytes

	def table(self, add_mean: bool = False, add_sum: bool = False) -> pd.DataFrame:
		"""
		Minimal working example:

		```py
		df.crm.calibration(default="DEFAULT", score="SCORE").table()
		```

		Args:
			add_mean: Adds a mean row to the table. The mean is calculated for the number of observations (rounded \
			down to nearest integer), the number of observed defaults (rounded down to nearest integer), the number of \
			predicted defaults, the observed PD, and the predicted PD. The remaining statistics are based on these \
			mean values.
			add_sum: Adds a sum row to the table. The sum is calculated for the number of observations, the number of \
			observed defaults, the number of predicted defaults, the observed PD, and the predicted PD. The remaining \
			statistics are based on these sum values.

		Returns:
			Returns a table containing the number of observations, the number of observed defaults, the number of \
			predicted defaults, the observed PD, the predicted PD, the observed grade, the predicted grade, the \
			absolute grade difference as integer, the binomial p-value for underestimation, the binomial p-value for \
			overestimation, the Jeffreys p-value, the observed PD CT, and the predicted PD CT.
		"""
		df = pd.DataFrame(data=self.result_list)

		df[cfg.CT_PD_OBS] = df[cfg.PD_OBS].expanding().mean()
		df[cfg.CT_PD_PRE] = df[cfg.PD_PRE].expanding().mean()

		def help_table(by_agg: str, df_agg: pd.Series, pd_obs_agg: float, pd_pre_agg: float) -> dict:
			obs_agg = df_agg[cfg.OBS]
			default_obs_agg = df_agg[cfg.DEFAULT_OBS]
			default_pre_agg = df_agg[cfg.DEFAULT_PRE]
			grade_obs_agg = general.pd_to_grade(pd=pd_obs_agg)
			grade_pre_agg = general.pd_to_grade(pd=pd_pre_agg)
			grade_dif_agg = abs(general.grade_difference(grade_1=grade_obs_agg, grade_2=grade_pre_agg))
			k = int(df_agg[cfg.DEFAULT_OBS])
			n = int(df_agg[cfg.OBS])
			p_binom_und = stats.binomtest(k=k, n=n, p=pd_pre_agg, alternative="greater").pvalue
			p_binom_ove = stats.binomtest(k=k, n=n, p=pd_pre_agg, alternative="less").pvalue
			p_jeffreys = stats.beta.cdf(
				x=pd_pre_agg,
				a=df_agg[cfg.DEFAULT_OBS] + 1 / 2,
				b=df_agg[cfg.OBS] - df_agg[cfg.DEFAULT_OBS] + 1 / 2
			)
			return {
				cfg.BY: by_agg,
				cfg.OBS: obs_agg,
				cfg.DEFAULT_OBS: default_obs_agg,
				cfg.DEFAULT_PRE: default_pre_agg,
				cfg.PD_OBS: pd_obs_agg,
				cfg.PD_PRE: pd_pre_agg,
				cfg.GRADE_OBS: grade_obs_agg,
				cfg.GRADE_PRE: grade_pre_agg,
				cfg.GRADE_DIF: grade_dif_agg,
				cfg.P_BINOM_UND: p_binom_und,
				cfg.P_BINOM_OVE: p_binom_ove,
				cfg.P_JEFFREYS: p_jeffreys,
				cfg.CT_PD_OBS: pd_obs_agg,
				cfg.CT_PD_PRE: pd_pre_agg
			}

		if add_mean:
			df_temp = df.loc[lambda _df: ~_df[cfg.BY].isin([cfg.MEAN, cfg.SUM])]
			df_mean = df_temp.mean(numeric_only=True)
			pd_obs_mean = df_mean[cfg.PD_OBS]
			pd_pre_mean = df_mean[cfg.PD_PRE]
			df = pd.concat(
				[
					df,
					pd.DataFrame(
						[help_table(by_agg=cfg.MEAN, df_agg=df_mean, pd_obs_agg=pd_obs_mean, pd_pre_agg=pd_pre_mean)]
					)
				],
				ignore_index=True
			)
		if add_sum:
			df_temp = df.loc[lambda _df: ~_df[cfg.BY].isin([cfg.MEAN, cfg.SUM])]
			df_sum = df_temp.sum(numeric_only=True)
			pd_obs_sum = df_sum[cfg.DEFAULT_OBS] / df_sum[cfg.OBS]
			pd_pre_sum = sum(df_temp[cfg.OBS] * df_temp[cfg.PD_PRE]) / df_sum[cfg.OBS]
			df = pd.concat(
				[
					df,
					pd.DataFrame(
						[help_table(by_agg=cfg.SUM, df_agg=df_sum, pd_obs_agg=pd_obs_sum, pd_pre_agg=pd_pre_sum)]
					)
				],
				ignore_index=True
			)
		return df
