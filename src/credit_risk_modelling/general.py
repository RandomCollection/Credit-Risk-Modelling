"""
The module contains several general functions that can be used for subsequent analyses.
"""

import math
import numpy as np
import pandas

from bisect import bisect
from typing import Union

from . import cfg


def grade_difference(grade_1: str, grade_2: str) -> Union[int, None]:
	"""
	Calculate the difference between two rating grades as grade 1 - grade 2 as integer. Rating grades can be configured
	in module "cfg.py". Minimal working example:

	```py
	df = df.assign(GRADE_DIFFERENCE=df.apply(lambda row: crm.general.grade_difference(grade_1=row["GRADE_1"], grade_2=row["GRADE_2"]), axis=1))
	```

	Args:
		grade_1: Defines the first rating grade.
		grade_2: Defines the second rating grade.

	Returns:
		Returns the difference between two rating grades as grade 1 - grade 2 as integer.
	"""
	if pandas.isna(grade_1) | pandas.isna(grade_2):
		return None
	assert grade_1 in cfg.GRADES, (
		f"Function 'grade_difference()' of the 'Credit Risk Modelling' package does not accept '{grade_1}' as rating "
		f"grade. Valid rating grades are {cfg.GRADES}, see module 'cfg.py' for more details."
	)
	assert grade_2 in cfg.GRADES, (
		f"Function 'grade_difference()' of the 'Credit Risk Modelling' package does not accept '{grade_2}' as rating "
		f"grade. Valid rating grades are {cfg.GRADES}, see module 'cfg.py' for more details."
	)
	return grade_to_index(grade=grade_1) - grade_to_index(grade=grade_2)


def grade_to_index(grade: str) -> Union[int, None]:
	"""
	Transform rating grade to index (starting from 0). Rating grades can be configured in module "cfg.py". Minimal
	working example:

	```py
	df = df.assign(INDEX=df["GRADE"].apply(lambda x: crm.general.grade_to_index(grade=x)))
	```

	Args:
		grade: Defines the rating grade.

	Returns:
		Returns the index of the rating grade (starting from 0).
	"""
	if pandas.isna(grade):
		return None
	assert grade in cfg.GRADES, (
		f"Function 'grade_to_index()' of the 'Credit Risk Modelling' package does not accept '{grade}' as rating "
		f"grade. Valid rating grades are {cfg.GRADES}, see module 'cfg.py' for more details."
	)
	return cfg.GRADES.index(grade)


def grade_to_pd(grade: str) -> Union[float, None]:
	"""
	Transform rating grade to Probability of Default (PD). Rating grades and PDs can be configured in module "cfg.py".
	Minimal working example:

	```py
	df = df.assign(PD=df["GRADE"].apply(lambda x: crm.general.grade_to_pd(grade=x)))
	```

	Args:
		grade: Defines the rating grade.

	Returns:
		Returns the PD of the rating grade.
	"""
	if pandas.isna(grade):
		return None
	assert grade in cfg.GRADES, (
		f"Function 'grade_to_pd()' of the 'Credit Risk Modelling' package does not accept '{grade}' as rating grade. "
		f"Valid rating grades are {cfg.GRADES}, see module 'cfg.py' for more details."
	)
	return cfg.PDS_MID[grade_to_index(grade)]


def index_to_grade(index: int) -> Union[str, None]:
	"""
	Transform index (starting from 0) to rating grade. Rating grades can be configured in module "cfg.py". Minimal
	working example:

	```py
	df = df.assign(GRADE=df["INDEX"].apply(lambda x: crm.general.index_to_grade(index=x)))
	```

	Args:
		index: Defines the index (starting from 0).

	Returns:
		Returns the rating grade.
	"""
	if pandas.isna(index):
		return None
	assert 0 <= index <= len(cfg.GRADES) - 1, (
		f"Function 'index_to_grade()' of the 'Credit Risk Modelling' package does not accept '{index}' as index. Valid "
		f"indices are {[cfg.GRADES.index(grade) for grade in cfg.GRADES]}, see module "
		f"'cfg.py' for more details."
	)
	return cfg.GRADES[index]


def logit_pd_to_pd(logit_pd: float) -> Union[float, None]:
	"""
	Transform logit Probability of Default (PD) to PD. PDs can be configured in module "cfg.py". Minimal working
	example:

	```py
	df = df.assign(PD=df["LOGIT_PD"].apply(lambda x: crm.general.logit_pd_to_pd(logit_pd=x)))
	```

	Args:
		logit_pd: Defines the logit PD.

	Returns:
		Returns the PD.
	"""
	if pandas.isna(logit_pd):
		return None
	elif logit_pd == -np.inf:
		return 0
	elif logit_pd == np.inf:
		return 1
	return math.exp(logit_pd) / (1 + math.exp(logit_pd))


def pd_to_grade(pd: float) -> Union[str, None]:
	"""
	Transform Probability of Default (PD) to rating grade based on minimum PD threshold. Rating grades and PDs can be
	configured in module "cfg.py". Minimal working example:

	```py
	df = df.assign(GRADE=df["PD"].apply(lambda x: crm.general.pd_to_grade(pd=x)))
	```

	Args:
		pd: Defines the PD.

	Returns:
		Returns the rating grade.
	"""
	if pandas.isna(pd):
		return None
	assert 0 <= pd <= 1, (
		f"Function 'pd_to_grade()' of the 'Credit Risk Modelling' package does not accept '{pd}' as Probability of "
		f"Default (PD). Valid PDs are between 0 and 1, see module 'cfg.py' for more details."
	)
	pd_min_breakpoints = cfg.PDS_MIN
	return cfg.GRADES[bisect(a=pd_min_breakpoints, x=pd) - 1]


def pd_to_logit_pd(pd: float) -> Union[float, None]:
	"""
	Transform Probability of Default (PD) to logit PD. PDs can be configured in module "cfg.py". Minimal working
	example:

	```py
	df = df.assign(LOGIT_PD=df["PD"].apply(lambda x: crm.general.pd_to_logit_pd(pd=x)))
	```

	Args:
		pd: Defines the PD.

	Returns:
		Returns the logit PD.
	"""
	if pandas.isna(pd):
		return None
	elif pd == 0:
		return -np.inf
	elif pd == 1:
		return np.inf
	assert 0 < pd < 1, (
		f"Function 'pd_to_logit_pd()' of the 'Credit Risk Modelling' package does not accept '{pd}' as Probability of "
		f"Default (PD). Valid PDs are between 0 and 1, see module 'cfg.py' for more details."
	)
	return math.log(pd / (1 - pd))


def set_pandas_options() -> None:
	"""
	Set the pandas display width to "320" and the display maximum columns to "None". Minimal working example:

	```py
	crm.set_pandas_options()
	```

	Returns:
		Set the pandas display width to "320" and the display maximum columns to "None".
	"""
	pandas.set_option("display.width", 320)
	pandas.set_option("display.max_columns", None)
	print("pandas options have been set to 'display.width = 320' and 'display.max_columns = None'.")
