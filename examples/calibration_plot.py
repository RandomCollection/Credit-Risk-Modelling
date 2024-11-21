>>> import credit_risk_modelling as crm  # markdown-exec: hide

>>> data = crm.load_data.load_data()  # markdown-exec: hide

>>> (
>>>	    data
>>>	    .crm.calibration(default="DEFAULT", score="GRADE_PD", by="GRADE")
>>>	    .plot(show=True)
>>> )