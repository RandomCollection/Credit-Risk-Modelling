import numpy as np
import pandas as pd

from scipy import stats

from .. import cfg, general


def calculate_statistics_calibration(default: pd.Series, score: pd.Series) -> dict:
	basic_statistics = wrapper_calculate_basic_statistics(default=default, score=score)
	return {
		**basic_statistics,
		**wrapper_calculate_grade_difference(
			grade_1=basic_statistics[cfg.GRADE_OBS],
			grade_2=basic_statistics[cfg.GRADE_PRE]
		),
		**wrapper_calculate_test_binomial(
			obs=basic_statistics[cfg.OBS],
			default_obs=basic_statistics[cfg.DEFAULT_OBS],
			pd_pre=basic_statistics[cfg.PD_PRE]
		),
		**wrapper_calculate_test_jeffreys(
			obs=basic_statistics[cfg.OBS],
			default_obs=basic_statistics[cfg.DEFAULT_OBS],
			pd_pre=basic_statistics[cfg.PD_PRE]
		)
	}


def wrapper_calculate_basic_statistics(default: pd.Series, score: pd.Series) -> dict:
	obs = len(default)
	default_obs = sum(default)
	pd_obs = default_obs / obs
	pd_pre = float(np.mean(score))
	default_pre = round(pd_pre * obs, 0)
	grade_obs = general.pd_to_grade(pd=pd_obs)
	grade_pre = general.pd_to_grade(pd=pd_pre)
	return {
		cfg.OBS: obs,
		cfg.DEFAULT_OBS: default_obs,
		cfg.DEFAULT_PRE: default_pre,
		cfg.PD_OBS: pd_obs,
		cfg.PD_PRE: pd_pre,
		cfg.GRADE_OBS: grade_obs,
		cfg.GRADE_PRE: grade_pre
	}


def wrapper_calculate_grade_difference(grade_1: str, grade_2: str) -> dict:
	grade_dif = abs(general.grade_difference(grade_1=grade_1, grade_2=grade_2))
	return {
		cfg.GRADE_DIF: grade_dif
	}


def wrapper_calculate_test_binomial(obs: int, default_obs: int, pd_pre: float) -> dict:
	p_binom_und = stats.binomtest(k=default_obs, n=obs, p=pd_pre, alternative="greater").pvalue
	p_binom_ove = stats.binomtest(k=default_obs, n=obs, p=pd_pre, alternative="less").pvalue
	return {
		cfg.P_BINOM_UND: p_binom_und,
		cfg.P_BINOM_OVE: p_binom_ove
	}


def wrapper_calculate_test_jeffreys(obs: int, default_obs: int, pd_pre: float) -> dict:
	p_jeffreys = stats.beta.cdf(x=pd_pre, a=default_obs + 1 / 2, b=obs - default_obs + 1 / 2)
	return {
		cfg.P_JEFFREYS: p_jeffreys
	}
