>>> import credit_risk_modelling as crm  # markdown-exec: hide

>>> data = crm.load_data.load_data()  # markdown-exec: hide

>>> (
>>>     data
>>>     .crm.discrimination(default="DEFAULT", score="GRADE_PD", alpha=0.1, by="DATE")
>>>     .plot(show=True)
>>> )