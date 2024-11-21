import matplotlib
import pandas as pd

from typing import Union

from .calibration.methods import Calibration
from .discrimination.methods import Discrimination
from .formatting.methods import Formatting
from .frequency.methods import Frequency
from .migration.methods import Migration
from .override.methods import Override
from .plotting.methods import Plotting
from .stability.methods import Stability

matplotlib.use("TkAgg")


@pd.api.extensions.register_dataframe_accessor("crm")
class CreditRiskModellingAccessor:
	def __init__(self, df: pd.DataFrame):
		self.df = df

	def calibration(self, default: str, score: str, by: str = None) -> Calibration:
		"""
		Initialise the DataFrame with the calibration method. Minimal working example:

		```py
		df.crm.calibration(default="DEFAULT", score="SCORE")
		```

		Args:
			default: Defines the default column, typically containing binary values.
			score: Defines the score column, typically containing Probabilities of Default (PDs) in absolute values. \
			Grades can be transformed to scores, for example, PDs via the module "general.py" if necessary.
			by: Defines the grouper to be applied to the DataFrame, for example, "DATE".

		Returns:
			Returns a class called "Calibration" providing calibration analytics methods.
		"""
		return Calibration(df=self.df.copy(), default=default, score=score, by=by)

	def discrimination(self, default: str, score: str, alpha: float = None, by: str = None) -> Discrimination:
		"""
		Initialise the DataFrame with the discrimination method. Minimal working example:

		```py
		df.crm.discrimination(default="DEFAULT", score="SCORE")
		```

		Args:
			default: Defines the default column, typically containing binary values.
			score: Defines the score column, typically containing Probabilities of Default (PDs) in absolute values. \
			Grades can be transformed to scores, for example, PDs via the module "general.py" if necessary.
			alpha: Defines the statistical significance in absolute terms, i.e. a significant level of 10% should be \
			entered as 0.1.
			by: Defines the grouper to be applied to the DataFrame, for example, "DATE".

		Returns:
			Returns a class called "Discrimination" providing discrimination analytics methods.
		"""
		return Discrimination(df=self.df.copy(), default=default, score=score, alpha=alpha, by=by)

	def formatting(self) -> Formatting:
		"""
		Initialise the DataFrame with the formatting method. Minimal working example:

		```py
		df.crm.formatting()
		```

		Returns:
			Returns a class called "Formatting" providing formatting analytics methods.
		"""
		return Formatting(df=self.df.copy())

	def frequency(self, index: str, column: str = None, value: str = None, cohort: str = None) -> Frequency:
		"""
		Initialise the DataFrame with the frequency method. Minimal working example:

		```py
		df.crm.frequency(index="GRADE")
		```

		The module can create four different frequency tables depending on the exact parameter input:

		1. `df.crm.frequency(index="GRADE")`: frequency table per index row.
		2. `df.crm.frequency(index="GRADE", column="DATE")`: frequency table per index row and column column.
		3. `df.crm.frequency(index="GRADE", column="DATE", cohort="COHORT")`: frequency table per index row and column \
		column and cohort adjustment.
		4. `df.crm.frequency(index="GRADE", column="DATE", value="EXPOSURE")`: actual crosstab module by pandas per \
		index row, column column, and value values with 'aggfunc="sum"'.

		In case the index is categorical and should include "NaN"s, the "NaN"s have to be explicitly added, for \
		example,

		```py
		bins = [-np.inf, 0, 10, np.inf]
		labels = ["0", "0-10", ">10"]
		df["EXPOSURE_NEW"] = pd.cut(df["EXPOSURE_OLD"], bins=bins, labels=labels, right=False).values.add_categories("NaN")
		df["EXPOSURE_NEW"] = df["EXPOSURE_NEW"].apply(lambda x: x if x in labels else "NaN")
		```

		Args:
			index: Defines the index column in accordance to the crosstab module by pandas, for example, "GRADE".
			column: Defines the column column in accordance to the crosstab module by pandas, for example, "DATE".
			value: Defines the value column in accordance to the crosstab module by pandas, for example, "EXPOSURE".
			cohort: Defines the cohort identifier, for example, "COHORT".

		Returns:
			Returns a class called "Frequency" providing frequency analytics methods.
		"""
		return Frequency(df=self.df.copy(), index=index, column=column, value=value, cohort=cohort)

	def migration(self, grade: str, date: str, cohort: str) -> Migration:
		"""
		Initialise the DataFrame with the migration method. Minimal working example:

		```py
		df.crm.migration(grade="GRADE", date="DATE", cohort="COHORT")
		```

		Args:
			grade: Defines the grade column. Scores can be transformed to grades via the module "general.py" if \
			necessary.
			date: Defines the date column. The date column should only contain two dates.
			cohort: Defines the cohort identifier.

		Returns:
			Returns a class called "Migration" providing migration analytics methods.
		"""
		return Migration(df=self.df.copy(), grade=grade, date=date, cohort=cohort)

	def override(self, grade_1: str, grade_2: str) -> Override:
		"""
		Initialise the DataFrame with the override method. Minimal working example:

		```py
		df.crm.override(grade_1="GRADE_1", grade_2="GRADE_2")
		```

		Args:
			grade_1: Defines the first grade column, for example, grades before an override. Scores can be transformed \
			to grades via the module "general.py" if necessary.
			grade_2: Defines the second grade column, for example, grades after an override. Scores can be transformed \
			to grades via the module "general.py" if necessary.

		Returns:
			Returns a class called "Override" providing override analytics methods.
		"""
		return Override(df=self.df.copy(), grade_1=grade_1, grade_2=grade_2)

	def plotting(self) -> Plotting:
		"""
		Initialise the DataFrame with the plotting method. Minimal working example:

		```py
		df.crm.plotting()
		```

		Returns:
			Returns a class called "Plotting" providing plotting analytics methods.
		"""
		return Plotting(df=self.df.copy())

	def stability(self, score_ref: str, score: Union[str, list]) -> Stability:
		"""
		Initialise the DataFrame with the stability method. Minimal working example:

		```py
		df.crm.stability(score_ref="SCORE_REFERENCE", score="SCORE")
		```

		```py
		(
			df
			.crm.frequency(index="GRADE", column="DATE", cohort="ID")
			.table()
			.crm.stability(score_ref="SCORE_REF", score="SCORE")
			.table()
		)
		```

		Args:
			score_ref: Defines the reference population.
			score: Defines the population to be compared to the reference population.

		Returns:
			Returns a class called "Stability" providing stability analytics methods.
		"""
		return Stability(df=self.df.copy(), score_ref=score_ref, score=score)
