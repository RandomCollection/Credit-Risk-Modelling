"""
The module contains several functions to clean a pandas DataFrame. In particular:

- "change_column_names": Change column names. Column names can be changed to all upper case (default), lower case, or
left unchanged.
- "drop_duplicates": Drop duplicates. Duplicates can be dropped (default) or kept.
- "reset_index": Reset index.
- "strip_strings": Strip strings of column names and object column rows.
- "transform_missing_strings_to_nan": Transform missing strings in object column rows to Numpy's np.nan. Missing strings
are defined as "", "nan", and "None".

The functions can be simultaneously applied with the succinct "clean" wrapper function. Minimal working example:

```py
df = crm.clean(df=df)
```
"""

import numpy as np
import pandas as pd


def change_column_names(df: pd.DataFrame, style: str = "upper") -> pd.DataFrame:
	"""
	Change column names. Column names can be changed to all upper case (default), lower case, or left unchanged. Minimal
	working example:

	```py
	df = crm.change_column_names(df=df)
	```

	Args:
		df: Defines the pandas DataFrame.
		style: Define the style of change of the column names. It can be either "upper", "lower", or "unchanged".

	Returns:
		Returns the cleaned DataFrame.
	"""
	df_copy = df.copy()
	if style == "upper":
		df_copy.columns = df_copy.columns.str.upper()
	elif style == "lower":
		df_copy.columns = df_copy.columns.str.lower()
	elif style == "unchanged":
		return df_copy
	else:
		raise ValueError(
			"Function 'change_column_names()' of the 'Credit Risk Modelling' package only accepts 'upper', 'lower', or"
			"'unchanged' as argument values for the 'style' parameter."
		)
	return df_copy


def clean(df: pd.DataFrame, style: str = "upper", drop: bool = True) -> pd.DataFrame:
	"""
	Clean pandas DataFrame. The function does the following:

	- Strips strings of column names and object column rows.
	- Transforms missing strings in object column rows to Numpy's np.nan. Missing strings are defined as "", "nan", and
	"None".
	- Changes column names. Column names can be changed to all upper case (default), lower case, or left unchanged.
	- Drops duplicates. Duplicates can be dropped (default) or kept.
	- Resets the index.

	Minimal working example:

	```py
	df = crm.clean(df=df)
	```

	Args:
		df: Defines the pandas DataFrame.
		style: Define the style of change of the column names. It can be either "upper", "lower", or "unchanged".
		drop: Define whether to drop ("True") or keep ("False") duplicates.

	Returns:
		Returns the cleaned DataFrame.
	"""
	return (
		df
		.pipe(strip_strings)
		.pipe(transform_missing_strings_to_nan)
		.pipe(change_column_names, style=style)
		.pipe(drop_duplicates, drop=drop)
		.pipe(reset_index)
	)


def drop_duplicates(df: pd.DataFrame, drop: bool = True) -> pd.DataFrame:
	"""
	Drop duplicates. Duplicates can be dropped (default) or kept. Minimal working example:

	```py
	df = crm.drop_duplicates(df=df)
	```

	Args:
		df: Defines the pandas DataFrame.
		drop: Define whether to drop ("True") or keep ("False") duplicates.

	Returns:
		Returns the cleaned DataFrame.
	"""
	df_copy = df.copy()
	if drop:
		df_copy.drop_duplicates(inplace=True)
	elif not drop:
		return df_copy
	else:
		raise ValueError(
			"Function 'drop_duplicates()' of the 'Credit Risk Modelling' package only accepts 'True' or 'False' as"
			"argument values for the 'drop' parameter."
		)
	return df_copy


def reset_index(df: pd.DataFrame) -> pd.DataFrame:
	"""
	Reset index. Minimal working example:

	```py
	df = crm.reset_index(df=df)
	```

	Args:
		df: Defines the pandas DataFrame.

	Returns:
		Returns the cleaned DataFrame.
	"""
	df_copy = df.copy()
	df_copy.reset_index(drop=True, inplace=True)
	return df_copy


def strip_strings(df: pd.DataFrame) -> pd.DataFrame:
	"""
	Strip strings of column names and object column rows. Minimal working example:

	```py
	df = crm.strip_strings(df=df)
	```

	Args:
		df: Defines the pandas DataFrame.

	Returns:
		Returns the cleaned DataFrame.
	"""
	df_copy = df.copy()
	df_copy.columns = df_copy.columns.str.strip()
	df_object = df_copy.select_dtypes(["object"])
	df_copy[df_object.columns] = df_object.apply(lambda x: x.astype(str).str.strip())
	return df_copy


def transform_missing_strings_to_nan(df: pd.DataFrame) -> pd.DataFrame:
	"""
	Transform missing strings in object column rows to Numpy's np.nan. Missing strings are defined as "", "nan", and
	"None". Minimal working example:

	```py
	df = crm.transform_missing_strings_to_nan(df=df)
	```

	Args:
		df: Defines the pandas DataFrame.

	Returns:
		Returns the cleaned DataFrame.
	"""
	df_copy = df.copy()
	df_copy.replace(to_replace=["", "nan", "None"], value=np.nan, inplace=True)
	return df_copy
