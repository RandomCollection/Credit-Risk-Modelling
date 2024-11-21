>>> import credit_risk_modelling as crm  # markdown-exec: hide

>>> data = crm.load_data.load_data()  # markdown-exec: hide

>>> (
>>>     data
>>>     .loc[lambda df: df["DATE"].dt.year.isin([2022, 2023])]
>>>     .crm.migration(grade="GRADE", date="DATE", cohort="ID")
>>>     .plot(show=True)
>>> )