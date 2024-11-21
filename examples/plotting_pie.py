>>> import credit_risk_modelling as crm  # markdown-exec: hide

>>> data = crm.load_data.load_data().crm.frequency(index="DATE", column="GRADE").table().iloc[:, 0:2].set_axis(["DATE", "COUNT"], axis=1)  # markdown-exec: hide

>>> print("")  # markdown-exec: hide
>>> (
>>>     data
>>>     .crm.plotting().plot_pie(
>>>         x="DATE",
>>>         y="COUNT",
>>>         x_tick_labels="%d %B %Y",
>>>         explode=(0.05,) * 5,
>>>         autocolor="black",
>>>         show=True
>>>     )
>>> )