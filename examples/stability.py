>>> import credit_risk_modelling as crm  # markdown-exec: hide

>>> data = crm.load_data.load_data()  # markdown-exec: hide

>>> print("")  # markdown-exec: hide
>>> print(data.loc[lambda df: df["DATE"].dt.year.isin([2022, 2023])].crm.frequency(index="GRADE", column="DATE", cohort="ID").table().crm.stability(score_ref="2023-12-31_PCT", score="2022-12-31_PCT").table(sort_by_list=crm.cfg.GRADES))  # markdown-exec: hide
>>> (
>>>     data
>>>     .loc[lambda df: df["DATE"].dt.year.isin([2022, 2023])]
>>>     .crm.frequency(index="GRADE", column="DATE", cohort="ID")
>>>     .table()
>>>     .crm.stability(score_ref="2023-12-31_PCT", score="2022-12-31_PCT")
>>>     .table(sort_by_list=crm.cfg.GRADES)
>>> )