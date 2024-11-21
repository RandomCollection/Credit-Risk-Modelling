import pandas as pd

from . import cfg

INTRO = "Module '{module}' of the 'Credit Risk Modelling' package: "
MESSAGES = {
	1: (
		INTRO + "The data contains null values in the column '{col}'. These observations are dropped. Please "
		"investigate."
	),
	2: (
		INTRO + "The column '{col}' needs to be numeric with values 0 and 1 only. Please adjust."
	),
	4: (
		INTRO + "The parameter '{x_name}' needs to be numeric with values between 0 and 1 only. Please adjust."
	),
	5: (
		"Function 'format_cols()' of the 'Credit Risk Modelling' package only accepts a date for column '{col}'."
	),
	6: (
		"Function 'format_cols()' of the 'Credit Risk Modelling' package only accepts valid date format strings for "
		"the parameter 'date_format'."
	),
	7: (
		"Function 'format_cols()' of the 'Credit Risk Modelling' package cannot format column '{col}'. Either column "
		"'{col}' is already formatted or cannot be formatted."
	),
	11: (
		INTRO + "The column '{col}' does not contain two unique values. Please adjust."
	),
	12: (
		INTRO + "Number of observations of cohort 1 ({cohort_1}) differ from number of observations of cohort 2 "
		"({cohort_2}). Please investigate."
	),
	13: (
		INTRO + "The column '{col}' needs to be numeric. Please adjust."
	),
	14: (
		INTRO + "The parameter 'legend_label' and 'legend_label_2' need to have the same size as the 'by'-groups "
		"({number_of_groups}). Please adjust."
	),
	15: (
		INTRO + "There are no absolute score differences greater than 1. Hence, the downgrade rate is set to 'None'."
	),
	16: (
		INTRO + "There are no score differences. Hence, the migration rate is set to 'None'."
	)
}


def validate_binary(name: str, df: pd.DataFrame, col: str) -> None:
	assert set(df[col]) == {0, 1}, MESSAGES[2].format(module=name, col=col)


def validate_cohort(name: str, input_dict: dict) -> None:
	if input_dict[cfg.OBS_1_COHORT] != input_dict[cfg.OBS_2_COHORT]:
		raise UserWarning(
			MESSAGES[12].format(
				module=name,
				cohort_1=input_dict[cfg.OBS_1_COHORT],
				cohort_2=input_dict[cfg.OBS_2_COHORT]
			)
		)


def validate_dimension_2(name: str, df: pd.DataFrame, col: str) -> None:
	assert len(df[col].unique()) == 2, MESSAGES[11].format(module=name, col=col)


def validate_missing_value(name: str, df: pd.DataFrame, col: str) -> pd.DataFrame:
	if any(df[col].isnull()):
		print(MESSAGES[1].format(module=name, col=col))
		df = df[df[col].notnull()]
	return df


def validate_numeric(name: str, df: pd.DataFrame, col: str) -> None:
	assert pd.api.types.is_numeric_dtype(df[col]), MESSAGES[13].format(module=name, col=col)


def validate_range_bt_0_1(name: str, x: float, x_name: str) -> None:
	assert 0 <= x <= 1, MESSAGES[4].format(module=name, x_name=x_name)
