>>> import credit_risk_modelling as crm  # markdown-exec: hide

>>> crm.general.set_pandas_options()  # markdown-exec: hide

>>> data = crm.load_data.load_data()  # markdown-exec: hide

>>> print("")  # markdown-exec: hide
>>> print(data.loc[lambda df: df["DATE"].dt.year == 2023].crm.override(grade_1="GRADE", grade_2="OVERRIDE").table())  # markdown-exec: hide
>>> (
>>>     data
>>>     .loc[lambda df: df["DATE"].dt.year == 2023]
>>>     .crm.override(grade_1="GRADE", grade_2="OVERRIDE")
>>>     .table()
>>> )