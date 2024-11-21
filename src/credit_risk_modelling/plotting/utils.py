import datetime
import math
import matplotlib.axes
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from io import BytesIO
from matplotlib.ticker import FuncFormatter, MultipleLocator
from typing import Any, Tuple, Union

from .. import cfg, utils


def plot_add_text(ax: plt.axes, x: float, y: float, s: str, facecolor: str = cfg.COLOURS[1], **kwargs) -> None:
	ax.text(
		x=x,
		y=y,
		s=s,
		horizontalalignment="center",
		verticalalignment="center",
		bbox={"edgecolor": cfg.COLOUR_BLACK, "facecolor": facecolor, "pad": 10},
		**kwargs
	)


def plot_adjust(
		fig: plt.Figure,
		ax: plt.axes,
		x_axis_label: Union[str, None] = "Category",
		x_axis_label_color: str = cfg.COLOUR_BLACK,
		y_axis_label: Union[str, None] = "Per Cent",
		y_axis_label_color: str = cfg.COLOUR_BLACK,
		title: str = None
):
	ax.set_xlabel(x_axis_label, labelpad=10, color=x_axis_label_color)
	ax.set_ylabel(y_axis_label, labelpad=10, color=y_axis_label_color)
	ax.set_title(label=title)
	ax.margins(0)
	ax.set_axisbelow(True)
	ax.xaxis.grid(color=cfg.COLOUR_GREY, linestyle="-")
	ax.yaxis.grid(color=cfg.COLOUR_GREY, linestyle="-")
	fig.tight_layout()


def plot_adjust_axis_x(
		df: pd.DataFrame,
		cols: Union[str, list],
		ax: plt.axes,
		cols_is_date: bool = False,
		pct: bool = True,
		barh: bool = False,
		lim_adjustments: bool = True,
		lim_min: Union[float, pd.Timestamp, datetime.date] = None,
		lim_max: Union[float, pd.Timestamp, datetime.date] = None,
		lim_rounded: bool = True,
		tick_spacing: float = None,
		tick_digits: int = 0,
		tick_rot: int = 0,
		tick_color: str = cfg.COLOUR_BLACK
) -> (float, float):
	if (cols_is_date and not barh) or not lim_adjustments:
		if tick_spacing is None:
			tick_spacing = 1
		ax.set_xticks(range(0, len(df), tick_spacing))
		ax.set_xticklabels(df.loc[:, cols][::tick_spacing])
		ax.tick_params(axis="x", colors=tick_color, labelrotation=tick_rot)
	else:
		ax.tick_params(axis="x", colors=tick_color, labelrotation=tick_rot)
		lim_min_default, lim_max_default = ax.get_xlim()
		lim_min, lim_max = plot_adjust_lim(
			df=df,
			cols=cols,
			lim_min_default=lim_min_default,
			lim_max_default=lim_max_default,
			lim_min=lim_min,
			lim_max=lim_max,
			lim_rounded=lim_rounded
		)
		ax.set_xlim([lim_min, lim_max])
		if tick_spacing is not None:
			ax.xaxis.set_major_locator(MultipleLocator(tick_spacing))
		if pct and barh:
			ax.xaxis.set_major_formatter(FuncFormatter(lambda tick, _: f"{tick:.{tick_digits}%}"))
		else:
			ax.xaxis.set_major_formatter(FuncFormatter(lambda tick, _: f"{tick:,.{tick_digits}f}"))
		if not barh:
			ax.set_xticklabels(df.loc[:, cols])
		return lim_min, lim_max


def plot_adjust_axis_y(
		df: pd.DataFrame,
		cols: Union[str, list],
		ax: plt.axes,
		cols_is_date: bool = False,
		pct: bool = True,
		barh: bool = False,
		lim_adjustments: bool = True,
		lim_min: Union[float, pd.Timestamp, datetime.date] = None,
		lim_max: Union[float, pd.Timestamp, datetime.date] = None,
		lim_rounded: bool = True,
		tick_spacing: float = None,
		tick_digits: int = 0,
		tick_rot: int = 0,
		tick_color: str = cfg.COLOUR_BLACK
) -> (float, float):
	if (cols_is_date and not barh) or not lim_adjustments:
		if tick_spacing is None:
			tick_spacing = 1
		ax.set_yticks(range(0, len(df), tick_spacing))
		ax.set_yticklabels(df.loc[:, cols][::tick_spacing])
		ax.tick_params(axis="y", colors=tick_color, labelrotation=tick_rot)
	else:
		ax.tick_params(axis="y", colors=tick_color, labelrotation=tick_rot)
		lim_min_default, lim_max_default = ax.get_ylim()
		lim_min, lim_max = plot_adjust_lim(
			df=df,
			cols=cols,
			lim_min_default=lim_min_default,
			lim_max_default=lim_max_default,
			lim_min=lim_min,
			lim_max=lim_max,
			lim_rounded=lim_rounded
		)
		ax.set_ylim([lim_min, lim_max])
		if tick_spacing is not None:
			ax.yaxis.set_major_locator(MultipleLocator(tick_spacing))
		if pct and not barh:
			ax.yaxis.set_major_formatter(FuncFormatter(lambda tick, _: f"{tick:.{tick_digits}%}"))
		else:
			ax.yaxis.set_major_formatter(FuncFormatter(lambda tick, _: f"{tick:,.{tick_digits}f}"))
		if barh:
			ax.set_yticklabels(df.loc[:, cols])
		return lim_min, lim_max


def plot_adjust_lim(
	df: pd.DataFrame,
	cols: Union[str, list],
	lim_min_default: float,
	lim_max_default: float,
	lim_min: Union[float, pd.Timestamp, datetime.date] = None,
	lim_max: Union[float, pd.Timestamp, datetime.date] = None,
	lim_rounded: bool = True
) -> (float, float):
	lim_min_actual, lim_max_actual = plot_get_cols_range(df=df, cols=cols)
	if type(lim_min_actual) in [pd.Timestamp, datetime.date, datetime.datetime]:
		return lim_min_actual, lim_max_actual
	order_of_magnitude = max(plot_get_order_of_magnitude(lim_min_actual), plot_get_order_of_magnitude(lim_max_actual))
	lim_min_round = plot_round_number(number=lim_min_actual, order_of_magnitude=order_of_magnitude, direction="down")
	lim_max_round = plot_round_number(number=lim_max_actual, order_of_magnitude=order_of_magnitude, direction="up")
	if lim_min_actual < 0 and lim_max_actual < 0:
		lim_max_round = 0
	elif lim_min_actual > 0 and lim_max_actual > 0:
		lim_min_round = 0
	if lim_min is None and lim_rounded is True:
		lim_min = lim_min_round
	elif lim_min is None and lim_rounded is False:
		lim_min = lim_min_default
	if lim_max is None and lim_rounded is True:
		lim_max = lim_max_round
	elif lim_max is None and lim_rounded is False:
		lim_max = lim_max_default
	return lim_min, lim_max


def plot_adjust_x_tick_labels(df: pd.DataFrame, x: str, x_tick_labels: Union[str, list] = None) -> bool:
	x_is_date = False
	if df.loc[:, [x]].dtypes.iloc[0] in [
		np.dtype("datetime64[ns]"),
		np.dtype("<M8[us]"),
		np.dtype(">M8[us]"),
		np.dtype("<M8[ns]"),
		np.dtype(">M8[ns]")
	]:
		x_is_date = True
	if x_tick_labels is not None and type(x_tick_labels) is str:
		df[x] = df[x].dt.strftime(x_tick_labels)
	elif x_tick_labels is not None and type(x_tick_labels) is not str:
		df[x] = x_tick_labels
	return x_is_date


def plot_close(show: bool = False):
	if not show:
		plt.close()


def plot_get_cols_range(df: pd.DataFrame, cols: Union[str, list]) -> (float, float):
	df_tmp = df.loc[:, cols]
	try:
		cols_min = float(df_tmp.min().min())
	except AttributeError:
		cols_min = float(df_tmp.index.min())
	except TypeError:
		cols_min = df_tmp.min()
	try:
		cols_max = float(df_tmp.max().max())
	except AttributeError:
		cols_max = float(df_tmp.index.max())
	except TypeError:
		cols_max = df_tmp.max()
	return cols_min, cols_max


def plot_get_order_of_magnitude(number: float) -> int:
	try:
		return math.floor(math.log(abs(number), 10))
	except ValueError:
		return 0


def plot_heatmap_1(
		df: pd.DataFrame,
		colour: list,
		font_size: int,
		mask: np.array,
		ax: matplotlib.axes.Axes
) -> None:
	sns.heatmap(
		data=df,
		vmin=0,
		vmax=df.max().max(),
		cmap=sns.color_palette(colour),
		annot=True,
		fmt=".0%",
		annot_kws={"color": cfg.COLOUR_BLACK, "size": font_size},
		linewidths=1,
		linecolor=cfg.COLOUR_GREY,
		cbar=False,
		square=True,
		mask=mask,
		ax=ax
	)


def plot_heatmap_2(
		df: pd.DataFrame,
		vmax: int,
		font_size: int,
		ax: matplotlib.axes.Axes
) -> None:
	sns.heatmap(
		data=df,
		vmin=0,
		vmax=vmax,
		cmap=sns.color_palette(cfg.COLOURS_AMBER),
		annot=True,
		fmt=",.0f",
		annot_kws={"color": cfg.COLOUR_BLACK, "size": font_size},
		linewidths=0.5,
		cbar=False,
		xticklabels=False,
		yticklabels=False,
		ax=ax
	)


def plot_heatmap_3(
		df: pd.DataFrame,
		font_size: int,
		ax: matplotlib.axes.Axes
) -> None:
	sns.heatmap(
		data=df,
		cmap=sns.color_palette([cfg.COLOUR_WHITE]),
		annot=True,
		fmt=",.0f",
		annot_kws={"color": cfg.COLOUR_BLACK, "size": font_size},
		linewidths=0.5,
		cbar=False,
		xticklabels=False,
		yticklabels=False,
		ax=ax
	)


def plot_heatmap_wrapper_wrapper(
		df: pd.DataFrame,
		value_counts: pd.DataFrame,
		x_axis_label: str,
		y_axis_label: str,
		font_size: int,
		annotation: bool = True
) -> None:
	# Initialise plot
	ax_1 = plt.subplot2grid((20, 20), (0, 0), colspan=19, rowspan=19)
	ax_2 = plt.subplot2grid((20, 20), (19, 0), colspan=19, rowspan=1)
	ax_3 = plt.subplot2grid((20, 20), (0, 19), colspan=1, rowspan=19)
	ax_4 = plt.subplot2grid((20, 20), (19, 19), colspan=1, rowspan=1)
	mask_1 = np.zeros_like(df)
	mask_1[np.triu_indices_from(mask_1)] = True
	mask_2 = np.ones_like(df)
	mask_2[np.diag_indices_from(mask_2)] = False
	mask_3 = np.zeros_like(df)
	mask_3[np.tril_indices_from(mask_3)] = True
	box = plt.gca().get_position()
	plt.gca().set_position(
		[
			box.x0 + 0.05 * box.width, box.y0 + 0.05 * box.height, box.width * 0.95, box.height * 0.95
		]
	)
	# Plot
	plot_heatmap_1(df=df, colour=cfg.COLOURS_GREEN, font_size=font_size, mask=mask_1, ax=ax_1)
	plot_heatmap_1(df=df, colour=cfg.COLOURS_GREY, font_size=font_size, mask=mask_2, ax=ax_1)
	plot_heatmap_1(df=df, colour=cfg.COLOURS_RED, font_size=font_size, mask=mask_3, ax=ax_1)
	plot_heatmap_2(
		df=pd.DataFrame(value_counts.iloc[:, 1].fillna(0.0001)).transpose(),
		vmax=value_counts.max().max(),
		font_size=font_size,
		ax=ax_2
	)
	plot_heatmap_2(
		df=pd.DataFrame(value_counts.iloc[:, 0].fillna(0.0001)),
		vmax=value_counts.max().max(),
		font_size=font_size,
		ax=ax_3
	)
	plot_heatmap_3(df=pd.DataFrame({"": [value_counts.iloc[:, 0].fillna(0.0001).sum()]}), font_size=font_size, ax=ax_4)
	# Add annotation
	if annotation:
		plot_add_text(
			x=0.875,
			y=0.875,
			s="Downgrade",
			facecolor=cfg.COLOURS_RED[25],
			ax=ax_1,
			transform=ax_1.transAxes
		)
		plot_add_text(
			x=0.125,
			y=0.125,
			s="Upgrade",
			facecolor=cfg.COLOURS_GREEN[25],
			ax=ax_1,
			transform=ax_1.transAxes
		)
	# Adjust plot
	ax_1.set_xticklabels(ax_1.get_xticklabels(), rotation=0)
	ax_1.set_yticklabels(ax_1.get_yticklabels(), rotation=0)
	ax_1.set_xlabel(x_axis_label, labelpad=10)
	ax_1.set_ylabel(y_axis_label, labelpad=10)
	ax_1.xaxis.set_label_position("top")
	ax_1.xaxis.set_ticks_position("top")
	ax_1.tick_params(left=False, top=False)
	ax_1.set_axisbelow(True)


def plot_initialise(fig_size: tuple = (7.5, 7.5)) -> Union[BytesIO, Tuple[Any, Any]]:
	return BytesIO(), plt.subplots(figsize=fig_size)


def plot_legend(
		ax: plt.axes,
		df: pd.DataFrame = None,
		y: Union[str, list] = None,
		y_2: Union[str, list] = None,
		barh: bool = False,
		switch_order: bool = False,
		legend: bool = True,
		legend_label: Union[str, list] = None,
		legend_loc: str = "upper right"
):
	def define_legend(labels: list, reverse: bool = False, **kwargs) -> None:
		(
			ax
			.legend(
				labels=labels, edgecolor=cfg.COLOUR_BLACK, fancybox=False, loc=legend_loc, reverse=reverse, **kwargs
			)
			.set_visible(legend)
		)

	if barh:
		if switch_order:
			if legend_label is None:
				if y_2 is None:
					legend_label = df.loc[:, y].columns.tolist()
					define_legend(labels=legend_label, reverse=True)
				else:
					handles, labels = ax.get_legend_handles_labels()
					handles = handles[:len(y)][::-1] + handles[len(y):][::-1]
					labels = labels[:len(y)][::-1] + labels[len(y):][::-1]
					define_legend(labels=labels, reverse=False, handles=handles)
			else:
				if y_2 is None:
					define_legend(labels=legend_label[::-1], reverse=True)
				else:
					handles, _ = ax.get_legend_handles_labels()
					handles = handles[:len(y)][::-1] + handles[len(y):][::-1]
					labels = legend_label[:len(y)] + legend_label[len(y):]
					define_legend(labels=labels, reverse=False, handles=handles)
		else:
			if legend_label is None:
				if y_2 is None:
					legend_label = df.loc[:, y].columns.tolist()
					define_legend(labels=legend_label, reverse=True)
				else:
					legend_label = df.loc[:, np.r_[y, y_2]].columns.tolist()
					define_legend(labels=legend_label, reverse=True)
			else:
				if y_2 is None:
					define_legend(labels=legend_label, reverse=True)
				else:
					legend_label = legend_label[:len(y)] + legend_label[len(y):]
					define_legend(labels=legend_label, reverse=True)
	else:
		if switch_order:
			if legend_label is None:
				if y_2 is None:
					legend_label = df.loc[:, y].columns.tolist()
					define_legend(labels=legend_label, reverse=False)
				else:
					legend_label = df.loc[:, np.r_[y, y_2]].columns.tolist()
					define_legend(labels=legend_label, reverse=False)
			else:
				if y_2 is None:
					define_legend(labels=legend_label[::-1], reverse=False)
				else:
					legend_label = legend_label[len(y):] + legend_label[:len(y)]
					define_legend(labels=legend_label[::-1], reverse=False)
		else:
			if legend_label is None:
				if y_2 is None:
					legend_label = df.loc[:, y].columns.tolist()
					define_legend(labels=legend_label, reverse=False)
				else:
					legend_label = df.loc[:, np.r_[y, y_2]].columns.tolist()
					define_legend(labels=legend_label, reverse=False)
			else:
				if y_2 is None:
					define_legend(labels=legend_label, reverse=False)
				else:
					legend_label = legend_label[:len(y)] + legend_label[len(y):]
					define_legend(labels=legend_label, reverse=False)


def plot_plot_wrapper(df: pd.DataFrame, kind: str, ax: plt.axes, **kwargs) -> None:
	df.plot(
		kind=kind,
		x=1,
		y=0,
		color=cfg.COLOURS[0],
		marker="D",
		loglog=True,
		zorder=10,
		ax=ax,
		**kwargs
	)


def plot_preparation(
		y: Union[str, list],
		y_2: Union[str, list] = None,
		legend_label: Union[str, list] = None
) -> (list, list, list):
	if type(y) is str:
		y = [y]
	if type(y_2) is str:
		y_2 = [y_2]
	if type(legend_label) is str:
		legend_label = [legend_label]
	return y, y_2, legend_label


def plot_round_number(number: float, order_of_magnitude: int, direction: str) -> float:
	scale_factor = 10 ** order_of_magnitude
	number_tmp = None
	if direction == "down":
		number_tmp = math.floor((number - 10 ** (order_of_magnitude - 1)) / scale_factor)
	if direction == "up":
		number_tmp = math.ceil((number + 10 ** (order_of_magnitude - 1)) / scale_factor)
	return round(number=number_tmp * scale_factor, ndigits=abs(order_of_magnitude))


def plot_save(fig_bytes: BytesIO, path: str) -> None:
	plt.savefig(fig_bytes)
	if path is not None:
		plt.savefig(path)


def plot_sort(
		df: pd.DataFrame,
		x: str,
		sort_by_col: str = None,
		sort_by_list: list = None,
		sort_asc: bool = True
) -> pd.DataFrame:
	if sort_by_col is not None:
		df.sort_values(by=sort_by_col, ascending=sort_asc, inplace=True, ignore_index=True)
	if sort_by_list is not None:
		df = utils.help_sort_by_list(df=df, col=x, sort_by_list=sort_by_list, sort_asc=sort_asc)
	return df
