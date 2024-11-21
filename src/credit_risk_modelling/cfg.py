"""
This module contains some default configurations that can be adjusted according to own preferences. It contains five
sets of constants:

- Grades,
- Probabilities of Default (PDs),
- Colours,
- Date formats, and
- Column names.
"""

from colour import Color

# GRADES
GRADES = ["AAA", "AA", "A", "BBB", "BB", "B", "CCC", "D"]  # order from best to worse
GRADES_ORDER = {grade: order for order, grade in enumerate(GRADES)}

# PROBABILITIES OF DEFAULT (PDS)
PDS_MIN = [0.0000, 0.0005, 0.0010, 0.0025, 0.0160, 0.0600, 0.1500, 1.0000]
PDS_MID = [0.0003, 0.0008, 0.0018, 0.0093, 0.0380, 0.1050, 0.5750, 1.0000]
PDS_MAX = [0.0005, 0.0010, 0.0025, 0.0160, 0.0600, 0.1500, 1.0000, 1.0000]

# COLOURS
COLOURS = ["#6200EE", "#03DAC5", "#D81159", "#FBB13C", "#F5E663"]
COLOURS_AMBER = [colour.hex_l for colour in list(Color("#FFF9E6").range_to(value=Color("#FFC000"), steps=100))]
COLOURS_GREEN = [colour.hex_l for colour in list(Color("#E6F7EE").range_to(value=Color("#00B050"), steps=100))]
COLOURS_GREY = [colour.hex_l for colour in list(Color("#F2F2F2").range_to(value=Color("#7F7F7F"), steps=100))]
COLOURS_RED = [colour.hex_l for colour in list(Color("#FFE5E5").range_to(value=Color("#FF0000"), steps=100))]
COLOUR_BLACK = "#000000"
COLOUR_GREY = "#F5F5F5"
COLOUR_WHITE = "#FFFFFF"

# DATE FORMATS
DATE_FORMAT = "%Y-%m-%d"

# COLUMN NAMES
ALPHA = "ALPHA"
AR = "AR"
AR_BOUND_LOWER = "AR_BOUND_LOWER"
AR_BOUND_UPPER = "AR_BOUND_UPPER"
BY = "BY"
CT_PD_OBS = "CT_PD_OBS"
CT_PD_PRE = "CT_PD_PRE"
DEFAULT_OBS = "DEFAULT_OBS"
DEFAULT_PRE = "DEFAULT_PRE"
DOWN_1 = "DOWN_1"
DOWN_2 = "DOWN_2"
DOWN_3 = "DOWN_3"
DOWN_4M = "DOWN_>3"
DOWN_TOTAL = "DOWN_TOTAL"
DR = "DR"
GRADE_DIF = "GRADE_DIF"
GRADE_OBS = "GRADE_OBS"
GRADE_PRE = "GRADE_PRE"
INFLOWS = "INFLOWS"
MEAN = "Mean"
MR = "MR"
OBS = "OBS"
OBS_1 = "OBS_1"
OBS_1_COHORT = "OBS_1_COHORT"
OBS_2 = "OBS_2"
OBS_2_COHORT = "OBS_2_COHORT"
OUTFLOWS = "OUTFLOWS"
PD_OBS = "PD_OBS"
PD_PRE = "PD_PRE"
P_BINOM_OVE = "P_BINOM_OVE"
P_BINOM_UND = "P_BINOM_UND"
P_JEFFREYS = "P_JEFFREYS"
SUM = "Sum"
UNCHANGED = "UNCHANGED"
UP_1 = "UP_1"
UP_2 = "UP_2"
UP_3 = "UP_3"
UP_4M = "UP_>3"
UP_TOTAL = "UP_TOTAL"

COLS_CALIBRATION = [
	BY, OBS, DEFAULT_OBS, DEFAULT_PRE, PD_OBS, PD_PRE, GRADE_OBS, GRADE_PRE, GRADE_DIF, P_BINOM_UND, P_BINOM_OVE,
	P_JEFFREYS
]
COLS_DISCRIMINATION = [
	BY, OBS, DEFAULT_OBS, AR, AR_BOUND_LOWER, AR_BOUND_UPPER, ALPHA
]
COLS_OVERRIDE = [
	OBS_1, OUTFLOWS, OBS_1_COHORT, OBS_2, INFLOWS, OBS_2_COHORT, UNCHANGED, UP_1, UP_2, UP_3, UP_4M, UP_TOTAL, DOWN_1,
	DOWN_2, DOWN_3, DOWN_4M, DOWN_TOTAL
]
COLS_MIGRATION = COLS_OVERRIDE + [MR, DR]
