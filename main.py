import math
import psychro


def error_handler(err):
    print(err)
    exit


def run_calc(db_1, wb_1):
    elev = 1000
    psychro.psychro_atm(elev)
    if db_1 < 0 and db_1 > 120:
        error_handler("Dry Bulb temp is out of range")

    if wb_1 < 0 and db_1 > 120:
        error_handler("Wet Bulb temp is out of range")
