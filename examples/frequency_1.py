>>> import credit_risk_modelling as crm  # markdown-exec: hide

>>> data = crm.load_data.load_data()  # markdown-exec: hide

>>> print("")  # markdown-exec: hide
>>> print(data.crm.frequency(index="GRADE").table(add_sum=True))  # markdown-exec: hide
>>> (
>>>     data
>>>     .crm.frequency(index="GRADE")
>>>     .table(add_sum=True)
>>> )