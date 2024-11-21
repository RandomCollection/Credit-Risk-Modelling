import numpy as np
import pandas as pd

from typing import Union


def calculate_statistics_stability(df: pd.DataFrame, score_ref: str, score: Union[str, list]) -> pd.DataFrame:
	if type(score) is str:
		score = [score]
	for i in range(0, len(score)):
		df_app = pd.DataFrame(
			{
				f"PSI_{score_ref}-{score[i]}":
					df.apply(lambda z: psi(score_ref=z.loc[score_ref], score=z.loc[score[i]]), axis=1)
			}
		)
		df_app.replace(np.nan, 0, inplace=True)
		df = pd.concat([df, df_app], axis=1, sort=True)
	return df


def psi(score_ref: float, score: float) -> float:
	if (score_ref == 0) | (score == 0):
		return 0
	return (score_ref - score) * np.log(score_ref / score)
