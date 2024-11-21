>>> import credit_risk_modelling as crm  # markdown-exec: hide

>>> data = crm.load_data.load_data()  # markdown-exec: hide

>>> print("")  # markdown-exec: hide
>>> discrimination = data.crm.discrimination(default="DEFAULT", score="GRADE_PD", alpha=0.1, by="DATE")  # markdown-exec: hide
>>> print(discrimination.table())  # markdown-exec: hide
>>> discrimination.table()