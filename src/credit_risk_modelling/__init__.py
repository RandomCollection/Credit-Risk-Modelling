"""
Credit Risk Modelling is a Python library providing a curated selection of modules to perform credit risk modelling
analytics.
"""

from . import cfg, cleaning, docx, general, register_dataframe_accessor
from .data import load_data

print(
	"\nThe following DataFrame extension attributes from the Credit Risk Modelling package are now registered and "
	"available:"
	"\n- .calibration()"
	"\n- .discrimination()"
	"\n- .formatting()"
	"\n- .frequency()"
	"\n- .migration()"
	"\n- .override()"
	"\n- .plotting()"
	"\n- .stability()"
	"\nFor more information, visit https://github.com/RandomCollection/Credit-Risk-Modelling."
)
