>>> import credit_risk_modelling as crm  # markdown-exec: hide

>>> data = crm.load_data.load_data().crm.frequency(index="DATE", column="GRADE").table().iloc[:, 0:2].set_axis(["DATE", "COUNT"], axis=1)  # markdown-exec: hide

>>> print("")  # markdown-exec: hide
>>> (
>>>     data
>>>     .crm.plotting().plot_line(
>>>         x="DATE",
>>>         y="COUNT",
>>>         pct=False,
>>>         x_axis_label="Date",
>>>         x_tick_labels="%d %B %Y",
>>>         y_axis_label="Count",
>>>         legend_label="Count",
>>>         marker="o",
>>>         show=True
>>>     )
>>> )