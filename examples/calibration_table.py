>>> import credit_risk_modelling as crm  # markdown-exec: hide

>>> crm.general.set_pandas_options()  # markdown-exec: hide

>>> data = crm.load_data.load_data()  # markdown-exec: hide

>>> print("")  # markdown-exec: hide
>>> print(data.crm.calibration(default="DEFAULT", score="GRADE_PD", by="DATE").table())  # markdown-exec: hide
>>> (
>>>     data
>>>     .crm.calibration(default="DEFAULT", score="GRADE_PD", by="DATE")
>>>     .table()
>>> )