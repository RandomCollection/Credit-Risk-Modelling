>>> import credit_risk_modelling as crm  # markdown-exec: hide

>>> data = crm.load_data.load_data()  # markdown-exec: hide

>>> print("")  # markdown-exec: hide
>>> print(data.crm.formatting().format_cols(float_cols="OVERRIDE_PD", float_digits=2, pct_cols="GRADE_PD", pct_digits=2, date_cols="DATE", date_format="%d %b %Y", date_format_upper=True, shift_index=True))  # markdown-exec: hide
>>> (
>>>     data
>>>     .crm.formatting()
>>>     .format_cols(
>>>         float_cols="OVERRIDE_PD", float_digits=2,
>>>         pct_cols="GRADE_PD", pct_digits=2,
>>>         date_cols="DATE", date_format="%d %b %Y", date_format_upper=True,
>>>         shift_index=True
>>>     )
>>> )