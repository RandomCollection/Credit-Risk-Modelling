>>> import credit_risk_modelling as crm  # markdown-exec: hide

>>> data = crm.load_data.load_data()  # markdown-exec: hide

>>> print("")  # markdown-exec: hide
>>> print(data.loc[lambda df: df["DATE"].dt.year.isin([2022, 2023])].crm.frequency(index="GRADE", column="DATE", cohort="ID").table(sort_by_list=crm.cfg.GRADES))  # markdown-exec: hide
>>> (
>>>     data
>>>     .loc[lambda df: df["DATE"].dt.year.isin([2022, 2023])]
>>>     .crm.frequency(index="GRADE", column="DATE", cohort="ID")
>>>     .table(sort_by_list=crm.cfg.GRADES)
>>> )