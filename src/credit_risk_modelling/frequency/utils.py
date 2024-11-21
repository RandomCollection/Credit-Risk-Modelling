import pandas as pd


def calculate_statistics_frequency(
	df: pd.DataFrame,
	index: str,
	column: str = None,
	value: str = None,
	cohort: str = None
) -> pd.DataFrame:
	if column is None:
		df = (
			df[index]
			.value_counts(dropna=False)
			.to_frame(index)
		)
	elif cohort is not None:
		df = (
			pd.crosstab(
				index=df[cohort].fillna("NaN"),
				columns=df[column].fillna("NaN"),
				values=df[index].fillna("NaN"),
				aggfunc="max"
			)
			.dropna()
			.apply(lambda x: x.value_counts())
		)
	elif value is None:
		df = pd.crosstab(
			index=df[index].fillna("NaN"),
			columns=df[column].fillna("NaN")
		)
	else:
		df = pd.crosstab(
			index=df[index],
			columns=df[column],
			values=df[value],
			aggfunc="sum",
		)
	return df
