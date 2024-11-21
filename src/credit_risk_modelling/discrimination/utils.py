import math
import pandas as pd

from scipy import stats
from sklearn.metrics import roc_auc_score

from .. import cfg


def calculate_accuracy_ratio(default: pd.Series, score: pd.Series, alpha: float = None) -> (float, float, float):
	if alpha is not None:
		auc, ci = calculate_area_under_the_curve(default=default, score=score, alpha=alpha)
		return 2 * auc - 1, tuple(2 * i - 1 for i in ci)
	return 2 * calculate_area_under_the_curve(default=default, score=score, alpha=alpha) - 1


def calculate_area_under_the_curve(default: pd.Series, score: pd.Series, alpha: float = None) -> (float, float, float):
	obs = len(default)
	default_obs = sum(default)
	auc = roc_auc_score(y_true=default, y_score=score)
	if alpha is not None:
		return auc, calculate_area_under_the_curve_confidence_interval(auc=auc, n_1=default_obs, n_2=obs, alpha=alpha)
	return auc


def calculate_area_under_the_curve_confidence_interval(auc: float, n_1: int, n_2: int, alpha: float) -> (float, float):
	z_alpha_half = stats.norm.ppf(alpha / 2)
	se = calculate_area_under_the_curve_standard_error(
		auc=auc,
		n_1=n_1,
		n_2=n_2 - n_1,
		q_1=auc / (2 - auc),
		q_2=2 * auc ** 2 / (1 + auc)
	)
	return auc + z_alpha_half * se, auc - z_alpha_half * se


def calculate_area_under_the_curve_standard_error(auc: float, n_1: int, n_2: int, q_1: float, q_2: float) -> float:
	# The following methodology is based on:
	# - Cortes, Corinna, and Mehryar Mohri, 2005, "Confidence Intervals for the Area Under the ROC Curve", Advances in
	#   Neural Information Processing Systems, 305-312.
	# - Hanley, James A., and Barbara J. McNeil, 1982, "The Meaning and Use of the Area Under a Receiver Operating
	#   Characteristic (ROC) Curve", Radiology 143.1, 29-36.
	return math.sqrt((auc * (1 - auc) + (n_1 - 1) * (q_1 - auc ** 2) + (n_2 - 1) * (q_2 - auc ** 2)) / (n_1 * n_2))


def calculate_statistics_discrimination(default: pd.Series, score: pd.Series, alpha: float = None) -> dict:
	obs = len(default)
	default_obs = sum(default)
	if (len(default) == 0) | (sum(default) == 0):
		ar, ar_bound_lower, ar_bound_upper = None, None, None
	elif alpha is not None:
		ar = calculate_accuracy_ratio(default=default, score=score, alpha=alpha)[0]
		ar_bound_lower, ar_bound_upper = calculate_accuracy_ratio(default=default, score=score, alpha=alpha)[1]
	else:
		ar = calculate_accuracy_ratio(default=default, score=score, alpha=alpha)
		ar_bound_lower, ar_bound_upper = None, None
	return {
		cfg.OBS: obs,
		cfg.DEFAULT_OBS: default_obs,
		cfg.AR: ar,
		cfg.AR_BOUND_LOWER: ar_bound_lower,
		cfg.AR_BOUND_UPPER: ar_bound_upper,
		cfg.ALPHA: alpha
	}
