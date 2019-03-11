"""
@author: Julian
@brief: Functions to convert measure units
@description:
1px = 1cm = 0.01m
"""
PX2M_DIVIDER = 100


def px_2_metres(px):
    return px / PX2M_DIVIDER


def metres_2_px(metres):
    return metres * PX2M_DIVIDER
