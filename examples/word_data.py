>>> import os

>>> from docxtpl import InlineImage
>>> from docx.shared import Mm

>>> import credit_risk_modelling as crm

>>> data = crm.load_data.load_data().crm.frequency(index="GRADE", column="DATE").table(index_range=crm.cfg.GRADES, sort_by_list=crm.cfg.GRADES, add_sum=True).filter(items=["GRADE", "2022-12-31_ABS", "2022-12-31_PCT", "2023-12-31_ABS", "2023-12-31_PCT"])  # markdown-exec: hide
>>> print(data)  # markdown-exec: hide
>>> data