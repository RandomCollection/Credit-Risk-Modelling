"""
The module defines a class "WordDocument" that can be used to initialise a Word template, add content, and save it. See
<a href="https://docxtpl.readthedocs.io/en/latest/" target="_blank">docxtpl.readthedocs</a> for more information.
"""

from docxtpl import DocxTemplate


class WordDocument:
	def __init__(self, path_word_in: str):
		self.doc = DocxTemplate(path_word_in)
		self.context = {}

	def add(self, dict_item: dict):
		self.context.update(dict_item)

	def save(self, path_word_out: str):
		self.doc.render(self.context, autoescape=True)
		self.doc.save(path_word_out)
