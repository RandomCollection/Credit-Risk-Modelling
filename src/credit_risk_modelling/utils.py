import numpy as np
import pandas as pd

from typing import Union

from . import cfg, general, validation


def help_add_sum(df: pd.DataFrame) -> pd.DataFrame:
	df = pd.concat([df, pd.DataFrame(df.sum(numeric_only=True)).T], ignore_index=True)
	df.iloc[-1, 0] = cfg.SUM
	return df


def help_append_result_list(result_list: list, dict_to_append: dict, cols: list, name: str) -> None:
	if type(dict_to_append) is not dict:
		raise Exception(f"{name} analysis: Can only append dictionaries.")
	if not (set(cols).issubset(set(dict_to_append.keys()))):
		raise Exception(f"{name} analysis: The keys are not complete '{cols}'.")
	result_list.append(dict_to_append)


def help_calculate_rate_downgrade(score_diffs: pd.Series, name: str) -> Union[float, None]:
	try:
		return len(score_diffs[lambda x: x > 1]) / len(score_diffs[lambda x: abs(x) > 1])
	except ZeroDivisionError:
		print(validation.MESSAGES[15].format(module=name))
		return None


def help_calculate_rate_migration(score_diffs: pd.Series, name: str) -> Union[float, None]:
	try:
		return len(score_diffs[lambda x: abs(x) > 1]) / len(score_diffs)
	except ZeroDivisionError:
		print(validation.MESSAGES[16].format(module=name))
		return None


def help_calculate_statistics_basic(df: pd.DataFrame) -> dict:
	obs_1 = df.iloc[:, 0].count()
	obs_2 = df.iloc[:, 1].count()
	inflows = sum(df.iloc[:, 0].isnull())
	outflows = sum(df.iloc[:, 1].isnull())
	obs_1_cohort = obs_1 - outflows
	obs_2_cohort = obs_2 - inflows
	return {
		cfg.OBS_1: obs_1,
		cfg.OUTFLOWS: outflows,
		cfg.OBS_1_COHORT: obs_1_cohort,
		cfg.OBS_2: obs_2,
		cfg.INFLOWS: inflows,
		cfg.OBS_2_COHORT: obs_2_cohort
	}


def help_calculate_statistics_movement(df: pd.DataFrame, name: str) -> dict:
	statistics_basic = help_calculate_statistics_basic(df=df)
	df.dropna(inplace=True)
	score_diffs = df.apply(lambda row: general.grade_difference(grade_1=row.iloc[1], grade_2=row.iloc[0]), axis=1)
	return {
		**statistics_basic,
		cfg.UNCHANGED: score_diffs[lambda x: x == 0].count(),
		cfg.UP_1: score_diffs[lambda x: x == -1].count(),
		cfg.UP_2: score_diffs[lambda x: x == -2].count(),
		cfg.UP_3: score_diffs[lambda x: x == -3].count(),
		cfg.UP_4M: score_diffs[lambda x: x < -3].count(),
		cfg.UP_TOTAL: score_diffs[lambda x: x < 0].count(),
		cfg.DOWN_1: score_diffs[lambda x: x == 1].count(),
		cfg.DOWN_2: score_diffs[lambda x: x == 2].count(),
		cfg.DOWN_3: score_diffs[lambda x: x == 3].count(),
		cfg.DOWN_4M: score_diffs[lambda x: x > 3].count(),
		cfg.DOWN_TOTAL: score_diffs[lambda x: x > 0].count(),
		cfg.MR: help_calculate_rate_migration(score_diffs=score_diffs, name=name),
		cfg.DR: help_calculate_rate_downgrade(score_diffs=score_diffs, name=name),
	}


def help_colour_hex8_to_hex6(hex8) -> str:
	r = int(hex8[1:3], 16)
	g = int(hex8[3:5], 16)
	b = int(hex8[5:7], 16)
	a = int(hex8[7:9], 16) / 255.0
	r_new = round((1 - a) * 255 + a * r)
	g_new = round((1 - a) * 255 + a * g)
	b_new = round((1 - a) * 255 + a * b)
	hex6 = f"#{r_new:02X}{g_new:02X}{b_new:02X}".upper()
	return hex6


def help_colour_wrapper(colours: list) -> list:
	return [help_colour_hex8_to_hex6(hex8=f"{color}{int(0.5 * 255):02x}") for color in colours]


def help_preparation(
		df: pd.DataFrame,
		values: Union[list, int],
		grade_range: list = None
) -> (pd.DataFrame, pd.DataFrame):
	_df = df.copy()
	col_0 = _df.columns[0]
	col_1 = _df.columns[1]
	_df["DUMMY"] = values
	value_counts = _df.iloc[:, 0:2].apply(lambda x: x.value_counts())
	grade_distinct = list(set(_df.iloc[:, 0]).union(set(_df.iloc[:, 1])))
	if grade_range is not None:
		grade_new = [grade for grade in grade_range if grade not in grade_distinct]
		grade_distinct = grade_distinct + grade_new
		grade_new_df = pd.DataFrame()
		for grade in grade_new:
			grade_new_df = pd.concat(
				[grade_new_df, pd.DataFrame(pd.Series({col_0: np.nan, col_1: np.nan}, name=grade)).T]
			)
		value_counts = pd.concat([value_counts, grade_new_df])
	_df = pd.concat(
		[_df, pd.DataFrame.from_dict({col_0: list(grade_distinct), col_1: list(grade_distinct)})],
		ignore_index=True
	)
	_df = _df.pivot_table(index=_df.columns[0], columns=_df.columns[1], values="DUMMY", aggfunc="count")
	_df.replace(0, np.nan, inplace=True)
	_df = _df.transpose() / _df.transpose().sum()
	_df = _df.transpose()
	grade_sorted = [x for _, x in sorted(zip([cfg.GRADES_ORDER[x] for x in grade_distinct], grade_distinct))]
	_df = _df.filter(items=grade_sorted).reindex(grade_sorted)
	value_counts = value_counts.reindex(grade_sorted)
	return _df, value_counts


def help_sort_by_list(df: pd.DataFrame, col: str, sort_by_list: list = None, sort_asc: bool = True) -> pd.DataFrame:
	return (
		df
		.assign(**{col: df[col].astype("category").cat.set_categories(sort_by_list)})
		.sort_values(by=col, ascending=sort_asc, ignore_index=True)
		.astype({col: "object"})
	)
