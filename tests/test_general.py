import math
import numpy as np
import unittest

from itertools import product

import credit_risk_modelling as crm


class TestGeneral(unittest.TestCase):
	def test_grade_diff(self) -> None:
		self.assertSequenceEqual(
			seq1=[
				crm.general.grade_difference(grade_1=grade[0], grade_2=grade[1])
				for grade in product(crm.cfg.GRADES, repeat=2)
			],
			seq2=[
				crm.cfg.GRADES.index(grade[0]) - crm.cfg.GRADES.index(grade[1])
				for grade in product(crm.cfg.GRADES, repeat=2)
			]
		)

	def test_grade_to_index(self) -> None:
		self.assertSequenceEqual(
			seq1=[crm.general.grade_to_index(grade=grade) for grade in crm.cfg.GRADES],
			seq2=[crm.cfg.GRADES.index(grade) for grade in crm.cfg.GRADES]
		)
	
	def test_grade_to_pd(self) -> None:
		self.assertSequenceEqual(
			seq1=[crm.general.grade_to_pd(grade=grade) for grade in crm.cfg.GRADES],
			seq2=crm.cfg.PDS_MID
		)

	def test_index_to_grade(self) -> None:
		self.assertSequenceEqual(
			seq1=[crm.general.index_to_grade(index=index) for index in range(0, len(crm.cfg.GRADES))],
			seq2=crm.cfg.GRADES
		)
	
	def test_logitpd_to_pd(self) -> None:
		self.assertSequenceEqual(
			seq1=[
				crm.general.logit_pd_to_pd(logit_pd=logitpd)
				for logitpd in np.concatenate(
					(-np.logspace(-3, 1, 10)[::-1], np.logspace(-3, 1, 10))
				)
			],
			seq2=[
				math.exp(logitpd) / (1 + math.exp(logitpd))
				for logitpd in np.concatenate(
					(-np.logspace(-3, 1, 10)[::-1], np.logspace(-3, 1, 10))
				)
			]
		)

	def test_pd_to_grade(self) -> None:
		self.assertSequenceEqual(
			seq1=[crm.general.pd_to_grade(pd=pd) for pd in crm.cfg.PDS_MID],
			seq2=crm.cfg.GRADES
		)

	def test_pd_to_logitpd(self) -> None:
		self.assertSequenceEqual(
			seq1=[crm.general.pd_to_logit_pd(pd=pd) for pd in crm.cfg.PDS_MID[:-1]],
			seq2=[math.log(pd / (1 - pd)) for pd in crm.cfg.PDS_MID[:-1]]
		)


if __name__ == "__main__":
	unittest.main()
