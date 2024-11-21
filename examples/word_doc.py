>>> import os  # markdown-exec: hide

>>> from docxtpl import InlineImage  # markdown-exec: hide
>>> from docx.shared import Mm  # markdown-exec: hide

>>> import credit_risk_modelling as crm  # markdown-exec: hide

>>> PATH_WORD = r"C:\Users\valer\Documents\Coding\Python\projects\credit-risk-modelling\architecture\word_docs_execution"  # markdown-exec: hide

>>> data = crm.load_data.load_data().crm.frequency(index="GRADE", column="DATE").table(index_range=crm.cfg.GRADES, sort_by_list=crm.cfg.GRADES, add_sum=True).filter(items=["GRADE", "2022-12-31_ABS", "2022-12-31_PCT", "2023-12-31_ABS", "2023-12-31_PCT"])  # markdown-exec: hide

>>> print("")  # markdown-exec: hide
>>> tbl = (
>>>     data
>>> 	.set_index("GRADE")
>>> 	.crm.formatting().format_cols(
>>> 		int_cols=["2022-12-31_ABS", "2023-12-31_ABS"],
>>> 		pct_cols=["2022-12-31_PCT", "2023-12-31_PCT"]
>>> 	)
>>> 	.set_axis(["# 2022-12-31", "% 2022-12-31", "# 2023-12-31", "% 2023-12-31"], axis=1)
>>> 	.crm.formatting().df_to_tbl(label="Grade")
>>> )
>>> fig = (
>>> 	data[data.iloc[:, 0] != "Sum"]
>>> 	.crm.plotting().plot_bar(
>>> 		x="GRADE",
>>> 		y=["2022-12-31_PCT", "2023-12-31_PCT"],
>>> 		x_axis_label="Grade",
>>> 		legend_label=["2022-12-31", "2023-12-31"],
>>> 	)
>>> )
>>> document = crm.docx.WordDocument(path_word_in=os.path.join(PATH_WORD, r"word_in.docx"))
>>> document.add(dict_item={"date_start": "31 December 2022"})
>>> document.add(dict_item={"date_end": "31 December 2023"})
>>> document.add(dict_item={"tbl": tbl})
>>> document.add(dict_item={"fig": InlineImage(document.doc, fig, width=Mm(150))})
>>> document.save(path_word_out=os.path.join(PATH_WORD, r"word_out.docx"))
