import psychro


cfm_1 = 1000
cfm_2 = 100
cfm_m = cfm_1 + cfm_2
db_1 = 96
wb_1 = 75
elevation = 1000
db_2 = 75
wb_2 = 62.5
db_m = ((db_1 * cfm_1) + (db_2 * cfm_2)) / cfm_m


def error_handler(err):
    print(err)
    exit


def run_calc_m(db, wb, atm_pressure):
    calculations = dict()
    vp_sat = psychro.psychro_pvs(db)
    calculations["Vapor Press. at saturation"] = vp_sat
    vp = psychro.psychro_pv1(db, wb, atm_pressure)
    calculations["Vapor Pressure"] = vp
    dew_point = psychro.psychro_dp(vp)
    calculations["Dew Point Temoerature"] = dew_point
    rel_humidity = psychro.psychro_rh(db, wb, atm_pressure)
    calculations["Relative Humidity"] = rel_humidity
    humidity_ratio = psychro.psychro_w(db, wb, atm_pressure)
    calculations["Humidity Ratio"] = humidity_ratio
    sp_vol = psychro.psychro_v(db, wb, atm_pressure)
    calculations["Specific Volume"] = sp_vol


def run_calc(cfm, db, wb, elev):
    calculations = dict()
    # elev = 1001
    # cfm = 1000
    atm_pressure = psychro.psychro_atm(elev)
    calculations["Atmospheric Pressure"] = atm_pressure
    vp_sat = psychro.psychro_pvs(db)
    calculations["Vapor Press. at saturation"] = vp_sat
    vp = psychro.psychro_pv1(db, wb, atm_pressure)
    calculations["Vapor Pressure"] = vp
    dew_point = psychro.psychro_dp(vp)
    calculations["Dew Point Temoerature"] = dew_point
    rel_humidity = psychro.psychro_rh(db, wb, atm_pressure)
    calculations["Relative Humidity"] = rel_humidity
    humidity_ratio = psychro.psychro_w(db, wb, atm_pressure)
    calculations["Humidity Ratio"] = humidity_ratio
    enthalpy = psychro.psychro_h(db, wb, atm_pressure)
    calculations["Enthalpy"] = enthalpy
    sp_vol = psychro.psychro_v(db, wb, atm_pressure)
    calculations["Specific Volume"] = sp_vol
    mfr_dry = cfm / sp_vol
    calculations["Mass Flow Rate, dry air"] = mfr_dry
    mfr_wv = humidity_ratio * mfr_dry
    calculations["Mass Flow Rate, water vapor"] = mfr_wv
    mfr_ma = mfr_dry + mfr_wv
    calculations["Mass Flow Rate, moist air"] = mfr_ma
    # print(calculations)
    if db < 0 and db > 120:
        error_handler("Dry Bulb temp is out of range")

    if wb < 0 and db > 120:
        error_handler("Wet Bulb temp is out of range")
    return calculations


air_flow_1 = run_calc(1000, 96, 75, 1000)
atm_pres = air_flow_1["Atmospheric Pressure"]
h_1 = air_flow_1["Enthalpy"]
humidity_ratio_1 = air_flow_1["Humidity Ratio"]
mfr_dry_1 = air_flow_1["Mass Flow Rate, dry air"]
mfr_wv_1 = air_flow_1["Mass Flow Rate, water vapor"]
mfr_ma_1 = air_flow_1["Mass Flow Rate, moist air"]
air_flow_2 = run_calc(100, 75, 62.5, 1000)
h_2 = air_flow_2["Enthalpy"]
humidity_ratio_2 = air_flow_2["Humidity Ratio"]
mfr_dry_2 = air_flow_2["Mass Flow Rate, dry air"]
mfr_wv_2 = air_flow_2["Mass Flow Rate, water vapor"]
mfr_ma_2 = air_flow_2["Mass Flow Rate, moist air"]
mfr_dry_m = mfr_dry_1 + mfr_dry_2
mfr_wv_m = mfr_wv_1 + mfr_wv_2
mfr_ma_m = mfr_dry_m + mfr_wv_m
h_m = ((h_1 * mfr_ma_1) + (h_2 * mfr_ma_2)) / mfr_ma_m
wb_m = psychro.psychro_wb(db_m, h_m, atm_pres)
humidity_ratio_m = ((humidity_ratio_1 * mfr_ma_1) +
                    (humidity_ratio_2 + mfr_ma_2)) / mfr_ma_m
air_flow_m = run_calc_m(db_m, wb_m, atm_pres)
print(wb_m)
# print(air_flow_1, air_flow_2)
