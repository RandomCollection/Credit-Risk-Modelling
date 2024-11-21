import datetime
import matplotlib.pyplot as plt
import pandas as pd

from io import BytesIO
from typing import Union

from . import utils as plotting
from .. import cfg, utils


class Plotting:
	def __init__(self, df: pd.DataFrame):
		self.df = df

	def plot_bar(
		self,
		x: str,
		y: Union[str, list],
		y_2: Union[str, list] = None,
		pct: bool = True,
		barh: bool = False,
		stacked: bool = False,
		switch_order: bool = False,
		sort_by_col: str = None,
		sort_by_list: list = None,
		sort_asc: bool = True,
		title: str = None,
		x_axis_label: str = "Category",
		x_tick_labels: Union[str, list] = None,
		x_tick_rot: int = 0,
		x_color: str = cfg.COLOUR_BLACK,
		y_axis_label: str = "Per Cent",
		y_lim_min: Union[float, pd.Timestamp, datetime.date] = None,
		y_lim_max: Union[float, pd.Timestamp, datetime.date] = None,
		y_lim_rounded: bool = True,
		y_tick_spacing: float = None,
		y_tick_digits: int = 0,
		y_tick_rot: int = 0,
		y_color: str = cfg.COLOUR_BLACK,
		color: Union[str, list] = None,
		legend: bool = True,
		legend_label: Union[str, list] = None,
		legend_loc: str = "upper right",
		fig_size: tuple = (10, 6.18),
		path: str = None,
		show: bool = False
	) -> BytesIO:
		"""
		Minimal working example:

		```py
		df.crm.plotting().plot_bar(x="DATE", y="SCORE")
		```

		Args:
			x: Defines the values to plot on the x-axis. Use ".reset_index()" to access the index of the DataFrame \
			since the index itself is not directly accessible.
			y: Defines the values to plot on the y-axis.
			y_2: Defines additional values to be plotted on the y-axis (with transparency).
			pct: Defines whether the y-axis is in percentage or absolute scale.
			barh: Defines whether the bar plot is horizontal or not.
			stacked: Defines whether the bar plot is stacked or not.
			switch_order: Defines whether to switch the order of the bars within one tick.
			sort_by_col: Defines the column to sort.
			sort_by_list: Defines the list to sort in case of categorical items which have no intrinsic sorting order.
			sort_asc: Sorts the previously defined column or list ascending.
			title: Defines the title.
			x_axis_label: Defines the x-axis label.
			x_tick_labels: Defines the x-tick labels. It can be an explicit list of labels or, in case of a date axis, \
			a format code based on the 1989 C standard such as "%b %Y".
			x_tick_rot: Defines the x-tick labels rotation.
			x_color: Defines the color of the x-ticks, the x-tick labels, and the x-axis label.
			y_axis_label: Defines the y-axis label.
			y_lim_min: Defines the y-axis minimum limit.
			y_lim_max: Defines the y-axis maximum limit.
			y_lim_rounded: Defines whether the y-axis limits should be rounded. This only works for limits which are \
			not explicitly defined via "y_lim_min" or "y_lim_max". The values are rounded to the next order of \
			magnitude or zero if appropriate.
			y_tick_spacing: Defines the y-tick spacing in absolute values.
			y_tick_digits: Defines the y-tick digits.
			y_tick_rot: Defines the x-tick labels rotation.
			y_color: Defines the color of the y-ticks, the y-tick labels, and the y-axis label.
			color: Defines the colour of the bars. Defaults to standard colour palette.
			legend: Defines whether a legend is plotted or not.
			legend_label: Defines the legend label.
			legend_loc: Defines the legend location.
			fig_size: Defines the figure size.
			path: Defines the saving path including the filename of the figure and should be entered as \
			r"C:\<path\>\<filename\>.<image_format\>".
			show: If True, plot is shown.

		Returns:
			Returns a bar plot.
		"""
		# Initialise
		df = self.df.copy()
		y, y_2, legend_label = plotting.plot_preparation(y=y, y_2=y_2, legend_label=legend_label)
		y_all = y + y_2 if y_2 is not None else y
		fig_bytes, (fig, ax) = plotting.plot_initialise(fig_size=fig_size)
		# Colour
		if color is None:
			color = cfg.COLOURS[0: len(y)]
		else:
			color = color
		if y_2 is not None:
			color_2 = utils.help_colour_wrapper(colours=color)[0:len(y_2)]
		else:
			color_2 = None
		# Switch
		if switch_order:
			y = y[::-1]
			color = color[::-1]
			if y_2 is not None:
				y_2 = y_2[::-1]
				color_2 = color_2[::-1]
		# Sort plot
		if barh:
			sort_asc = not sort_asc
		df = plotting.plot_sort(df=df, x=x, sort_by_col=sort_by_col, sort_by_list=sort_by_list, sort_asc=sort_asc)
		# x-tick labels
		x_is_date = plotting.plot_adjust_x_tick_labels(df=df, x=x, x_tick_labels=x_tick_labels)
		# Plot
		if not barh:
			if not stacked:
				df.loc[:, y].plot(kind="bar", color=color, zorder=2, ax=ax)
				if y_2 is not None:
					df.loc[:, y_2].plot(kind="bar", color=color_2, zorder=1, ax=ax)
			elif stacked:
				df.loc[:, y_all].plot(
					kind="bar",
					color=color + color_2 if color_2 is not None else color,
					stacked=stacked,
					zorder=2,
					ax=ax
				)
				df = df.assign(SUM=lambda _df: _df.loc[:, y_all].sum(axis=1))
				y_all = "SUM"
			_ = plotting.plot_adjust_axis_x(
				df=df,
				cols=x,
				ax=ax,
				cols_is_date=x_is_date,
				pct=pct,
				barh=barh,
				lim_rounded=False,
				tick_rot=x_tick_rot,
				tick_color=x_color
			)
			_ = plotting.plot_adjust_axis_y(
				df=df,
				cols=y_all,
				ax=ax,
				pct=pct,
				barh=barh,
				lim_min=y_lim_min,
				lim_max=y_lim_max,
				lim_rounded=y_lim_rounded,
				tick_spacing=y_tick_spacing,
				tick_digits=y_tick_digits,
				tick_rot=y_tick_rot,
				tick_color=y_color
			)
		elif barh:
			if not stacked:
				df.loc[:, y].plot(kind="barh", color=color, zorder=2, ax=ax)
				if y_2 is not None:
					df.loc[:, y_2].plot(kind="barh", color=color_2, zorder=1, ax=ax)
			elif stacked:
				df.loc[:, y_all].plot(
					kind="barh",
					color=color + color_2 if color_2 is not None else color,
					stacked=stacked,
					zorder=2,
					ax=ax
				)
				df = df.assign(SUM=lambda _df: _df.loc[:, y_all].sum(axis=1))
				y_all = "SUM"
			_ = plotting.plot_adjust_axis_x(
				df=df,
				cols=y_all,
				ax=ax,
				pct=pct,
				barh=barh,
				lim_min=y_lim_min,
				lim_max=y_lim_max,
				lim_rounded=y_lim_rounded,
				tick_spacing=y_tick_spacing,
				tick_digits=y_tick_digits,
				tick_rot=y_tick_rot,
				tick_color=y_color
			)
			_ = plotting.plot_adjust_axis_y(
				df=df,
				cols=x,
				ax=ax,
				cols_is_date=x_is_date,
				pct=pct,
				barh=barh,
				lim_rounded=False,
				tick_rot=x_tick_rot,
				tick_color=x_color
			)
			x_axis_label, y_axis_label = y_axis_label, x_axis_label
			x_color, y_color = y_color, x_color
		# Legend
		plotting.plot_legend(
			ax=ax,
			df=df,
			y=y,
			y_2=y_2,
			barh=barh,
			legend=legend,
			legend_label=legend_label,
			legend_loc=legend_loc,
			switch_order=switch_order
		)
		# Adjust plot
		plotting.plot_adjust(
			fig=fig,
			ax=ax,
			x_axis_label=x_axis_label,
			x_axis_label_color=x_color,
			y_axis_label=y_axis_label,
			y_axis_label_color=y_color,
			title=title
		)
		# Save plot
		plotting.plot_save(fig_bytes=fig_bytes, path=path)
		# Close plot
		plotting.plot_close(show=show)
		return fig_bytes

	def plot_line(
		self,
		x: str,
		y: Union[str, list],
		y_2: Union[str, list] = None,
		pct: bool = True,
		sort_by_col: str = None,
		sort_by_list: list = None,
		sort_asc: bool = True,
		title: str = None,
		x_axis_label: str = "Category",
		x_tick_labels: Union[str, list] = None,
		x_tick_rot: int = 0,
		x_color: str = cfg.COLOUR_BLACK,
		y_axis_label: str = "Per Cent",
		y_lim_min: Union[float, pd.Timestamp, datetime.date] = None,
		y_lim_max: Union[float, pd.Timestamp, datetime.date] = None,
		y_lim_rounded: bool = True,
		y_tick_spacing: float = None,
		y_tick_digits: int = 0,
		y_tick_rot: int = 0,
		y_color: str = cfg.COLOUR_BLACK,
		color: Union[str, list] = None,
		linewidth: float = None,
		linestyle: str = None,
		marker: str = None,
		markersize: float = None,
		markeredgewidth: float = None,
		markeredgecolor: str = None,
		markerfacecolor: str = None,
		vline: Union[int, float] = None,
		legend: bool = True,
		legend_label: Union[str, list] = None,
		legend_loc: str = "upper right",
		fig_size: tuple = (10, 6.18),
		path: str = None,
		show: bool = False
	) -> BytesIO:
		"""
		Minimal working example:

		```py
		df.crm.plotting().plot_line(x="DATE", y="SCORE")
		```

		Args:
			x: Defines the values to plot on the x-axis. Use ".reset_index()" to access the index of the DataFrame \
			since the index itself is not directly accessible.
			y: Defines the values to plot on the y-axis.
			y_2: Defines additional values to be plotted on the y-axis (with transparency).
			pct: Defines whether the y-axis is in percentage or absolute scale.
			sort_by_col: Defines the column to sort.
			sort_by_list: Defines the list to sort in case of categorical items which have no intrinsic sorting order.
			sort_asc: Sorts the previously defined column or list ascending.
			title: Defines the title.
			x_axis_label: Defines the x-axis label.
			x_tick_labels: Defines the x-tick labels. It can be an explicit list of labels or, in case of a date axis, \
			a format code based on the 1989 C standard such as "%b %Y".
			x_tick_rot: Defines the x-tick labels rotation.
			x_color: Defines the color of the x-ticks, the x-tick labels, and the x-axis label.
			y_axis_label: Defines the y-axis label.
			y_lim_min: Defines the y-axis minimum limit.
			y_lim_max: Defines the y-axis maximum limit.
			y_lim_rounded: Defines whether the y-axis limits should be rounded. This only works for limits which are \
			not explicitly defined via "y_lim_min" or "y_lim_max". The values are rounded to the next order of \
			magnitude or zero if appropriate.
			y_tick_spacing: Defines the y-tick spacing in absolute values.
			y_tick_digits: Defines the y-tick digits.
			y_tick_rot: Defines the x-tick labels rotation.
			y_color: Defines the color of the y-ticks, the y-tick labels, and the y-axis label.
			color: Defines the colour of the lines. Defaults to standard colour palette.
			linewidth: Defines the line width.
			linestyle: Defines the line style.
			marker: Defines the marker.
			markersize: Defines the marker size.
			markeredgewidth: Defines the marker edge width.
			markeredgecolor: Defines the marker edge color.
			markerfacecolor: Defines the marker face color.
			vline: Adds a dashed vertical line at position x = vline.
			legend: Defines whether a legend is plotted or not.
			legend_label: Defines the legend label.
			legend_loc: Defines the legend location.
			fig_size: Defines the figure size.
			path: Defines the saving path including the filename of the figure and should be entered as \
			r"C:\<path\>\<filename\>.<image_format\>".
			show: If True, plot is shown.

		Returns:
			Returns a line plot.
		"""
		# Initialise
		df = self.df.copy()
		y, y_2, legend_label = plotting.plot_preparation(y=y, y_2=y_2, legend_label=legend_label)
		fig_bytes, (fig, ax) = plotting.plot_initialise(fig_size=fig_size)
		# Colour
		if color is None:
			color = cfg.COLOURS[0: len(y)]
		else:
			color = color
		# Sort plot
		df = plotting.plot_sort(df=df, x=x, sort_by_col=sort_by_col, sort_by_list=sort_by_list, sort_asc=sort_asc)
		# x-tick labels
		_ = plotting.plot_adjust_x_tick_labels(df=df, x=x, x_tick_labels=x_tick_labels)
		# Plot
		if y_2 is not None:
			df.loc[:, y_2].plot(
				kind="line",
				linewidth=linewidth,
				linestyle=linestyle,
				color=utils.help_colour_wrapper(colours=color)[0:len(y_2)],
				marker=marker,
				markersize=markersize,
				markeredgewidth=markeredgewidth,
				markeredgecolor=markeredgecolor,
				markerfacecolor=markerfacecolor,
				ax=ax
			)
		df.loc[:, y].plot(
			kind="line",
			linewidth=linewidth,
			linestyle=linestyle,
			color=color,
			marker=marker,
			markersize=markersize,
			markeredgewidth=markeredgewidth,
			markeredgecolor=markeredgecolor,
			markerfacecolor=markerfacecolor,
			ax=ax
		)
		_ = plotting.plot_adjust_axis_x(
			df=df,
			cols=x,
			ax=ax,
			lim_adjustments=False,
			tick_rot=x_tick_rot,
			tick_color=x_color
		)
		_, y_lim_max = plotting.plot_adjust_axis_y(
			df=df,
			cols=y + y_2 if y_2 is not None else y,
			ax=ax,
			pct=pct,
			lim_min=y_lim_min,
			lim_max=y_lim_max,
			lim_rounded=y_lim_rounded,
			tick_spacing=y_tick_spacing,
			tick_digits=y_tick_digits,
			tick_rot=y_tick_rot,
			tick_color=y_color
		)
		# Vertical line
		if vline is not None:
			ax.vlines(
				x=vline,
				ymin=0,
				ymax=y_lim_max,
				color=cfg.COLOUR_BLACK,
				linestyles="dashed"
			)
		# Legend
		plotting.plot_legend(
			ax=ax,
			df=df,
			y=y,
			y_2=y_2,
			legend=legend,
			legend_label=legend_label,
			legend_loc=legend_loc
		)
		# Adjust plot
		plotting.plot_adjust(
			fig=fig,
			ax=ax,
			x_axis_label=x_axis_label,
			x_axis_label_color=x_color,
			y_axis_label=y_axis_label,
			y_axis_label_color=y_color,
			title=title
		)
		# Save plot
		plotting.plot_save(fig_bytes=fig_bytes, path=path)
		# Close plot
		plotting.plot_close(show=show)
		return fig_bytes

	def plot_pie(
		self,
		x: str,
		y: Union[str, list],
		sort_by_col: str = None,
		sort_by_list: list = None,
		sort_asc: bool = True,
		title: str = None,
		x_tick_labels: Union[str, list] = None,
		explode: tuple = None,
		color: Union[str, list] = None,
		autopct: str = "%1.1f%%",
		autocolor: str = cfg.COLOUR_WHITE,
		startangle: int = 90,
		radius: float = 1,
		fig_size: tuple = (10, 6.18),
		path: str = None,
		show: bool = False
	) -> BytesIO:
		"""
		Minimal working example:

		```py
		df.crm.plotting().plot_pie(x="DATE", y="SCORE")
		```

		Args:
			x: Defines the values to plot on the x-axis. Use ".reset_index()" to access the index of the DataFrame \
			since the index itself is not directly accessible.
			y: Defines the values to plot on the y-axis.
			sort_by_col: Defines the column to sort.
			sort_by_list: Defines the list to sort in case of categorical items which have no intrinsic sorting order.
			sort_asc: Sorts the previously defined column or list ascending.
			title: Defines the title.
			x_tick_labels: Defines the x-tick labels. It can be an explicit list of labels or, in case of a date axis, \
			a format code based on the 1989 C standard such as "%b %Y".
			explode: Defines the fraction of the radius with which to offset each wedge.
			color: Defines the colour of the lines. Defaults to standard colour palette.
			autopct: Defines the format of the labels inside the wedges.
			autocolor: Defines the colour of the wedges. Defaults to the standard colour palette.
			startangle: Defines the angle by which the start of the pie is rotated, counterclockwise from the x-axis.
			radius: Defines the radius of the pie.
			fig_size: Defines the figure size.
			path: Defines the saving path including the filename of the figure and should be entered as \
			r"C:\<path\>\<filename\>.<image_format\>".
			show: If True, plot is shown.

		Returns:
			Returns a pie plot.
		"""
		# Initialise
		df = self.df.copy()
		fig_bytes, (fig, ax) = plotting.plot_initialise(fig_size=fig_size)
		# Sort plot
		df = plotting.plot_sort(df=df, x=x, sort_by_col=sort_by_col, sort_by_list=sort_by_list, sort_asc=sort_asc)
		# x-tick labels
		_ = plotting.plot_adjust_x_tick_labels(df=df, x=x, x_tick_labels=x_tick_labels)
		# Colour
		if color is None:
			color = cfg.COLOURS[0: len(df[y])][::-1]
		# Plot
		_, texts, autotexts = ax.pie(
			df.loc[:, y],
			explode=explode,
			labels=df.loc[:, x].tolist(),
			colors=color,
			autopct=autopct,
			startangle=startangle,
			radius=radius
		)
		plt.setp(texts, color=cfg.COLOUR_BLACK)
		plt.setp(autotexts, color=autocolor)
		# Adjust plot
		plotting.plot_adjust(fig=fig, ax=ax, x_axis_label=None, y_axis_label=None, title=title)
		# Save plot
		plotting.plot_save(fig_bytes=fig_bytes, path=path)
		# Close plot
		plotting.plot_close(show=show)
		return fig_bytes
