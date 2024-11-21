>>> import credit_risk_modelling as crm

>>> data = (
>>>		crm.load_data.load_data()
>>>     .crm.frequency(index="DATE", column="GRADE")
>>>     .table()
>>>     .iloc[:, 0:2]
>>>     .set_axis(["DATE", "COUNT"], axis=1)
>>> )

>>> print("")  # markdown-exec: hide
>>> print(data)  # markdown-exec: hide
>>> data