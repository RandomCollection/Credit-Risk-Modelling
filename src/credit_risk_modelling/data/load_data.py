"""
The module provides dummy data to be used for examples or testing.
"""

import importlib_resources
import pandas as pd


def load_data() -> pd.DataFrame:
	"""
	Load dummy data to be used for examples or testing. Minimal working example:

	```py
	df = crm.load_data.load_data()
	```

	Returns:
		Returns dummy data to be used for examples or testing.
	"""
	return pd.read_parquet(path=importlib_resources.files(anchor="credit_risk_modelling.data").joinpath("data.parquet"))
