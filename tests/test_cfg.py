import unittest

import credit_risk_modelling as crm


class TestCfg(unittest.TestCase):
	def test_lengths_grades_pds(self) -> None:
		self.assertEqual(first=len(crm.cfg.GRADES), second=len(crm.cfg.PDS_MIN))
		self.assertEqual(first=len(crm.cfg.PDS_MIN), second=len(crm.cfg.PDS_MID))
		self.assertEqual(first=len(crm.cfg.PDS_MID), second=len(crm.cfg.PDS_MAX))

	def test_pds_min(self) -> None:
		self.assertTrue((min(crm.cfg.PDS_MIN) >= 0) & (max(crm.cfg.PDS_MIN) <= 1))
		self.assertTrue(all(x <= y for x, y in zip(crm.cfg.PDS_MIN, crm.cfg.PDS_MIN[1:])))

	def test_pds_mid(self) -> None:
		self.assertTrue((min(crm.cfg.PDS_MID) >= 0) & (max(crm.cfg.PDS_MID) <= 1))
		self.assertTrue(all(x <= y for x, y in zip(crm.cfg.PDS_MID, crm.cfg.PDS_MID[1:])))
		self.assertTrue(all(pd_min <= pd_mid for pd_min, pd_mid in zip(crm.cfg.PDS_MIN, crm.cfg.PDS_MID)))

	def test_pds_max(self) -> None:
		self.assertTrue((min(crm.cfg.PDS_MAX) >= 0) & (max(crm.cfg.PDS_MAX) <= 1))
		self.assertTrue(all(x <= y for x, y in zip(crm.cfg.PDS_MAX, crm.cfg.PDS_MAX[1:])))
		self.assertTrue(all(pd_mid <= pd_max for pd_mid, pd_max in zip(crm.cfg.PDS_MID, crm.cfg.PDS_MAX)))


if __name__ == "__main__":
	unittest.main()
