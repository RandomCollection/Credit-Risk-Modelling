"""
The module provides methods to perform migration analytics. In general, it can be used to analyse changes in grades
between two dates per cohort. For changes in grades per date, see the "override" method. It provides the number of
observations for two dates, the cohort outflows, the cohort inflows, the rating grade upgrades, the rating grade
downgrades, the rating grade migration rate (rating grade changes of more than one grade to number of cohort), and the
rating grade downgrade rate (rating grade downgrades of more than one grade to rating grade changes of more than one
grade). It also provides a "heatmap" migration matrix.
"""
