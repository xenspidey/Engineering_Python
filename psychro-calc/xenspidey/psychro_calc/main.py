import psychro


cfm_1 = 1000
cfm_2 = 100
cfm_m = cfm_1 + cfm_2
dry_bulb_1 = 96
wet_bulb_1 = 75
elevation = 1000
dry_bulb_2 = 75
wet_bulb_2 = 62.5
dry_bulb_mixed = ((dry_bulb_1 * cfm_1) + (dry_bulb_2 * cfm_2)) / cfm_m


def error_handler(err):
    print(err)
    exit


def run_calc_mixed_air(dry_bulb, wet_bulb, atm_pressure):
    calculations = dict()
    vapor_pres_sat = psychro.psychro_pvs(dry_bulb)
    calculations["Vapor Press. at saturation"] = vapor_pres_sat
    vapor_pres = psychro.psychro_pv1(dry_bulb, wet_bulb, atm_pressure)
    calculations["Vapor Pressure"] = vapor_pres
    dew_point = psychro.psychro_dp(vapor_pres)
    calculations["Dew Point Temoerature"] = dew_point
    rel_humidity = psychro.psychro_rh(dry_bulb, wet_bulb, atm_pressure)
    calculations["Relative Humidity"] = rel_humidity
    humidity_ratio = psychro.psychro_w(dry_bulb, wet_bulb, atm_pressure)
    calculations["Humidity Ratio"] = humidity_ratio
    sp_vol = psychro.psychro_v(dry_bulb, wet_bulb, atm_pressure)
    calculations["Specific Volume"] = sp_vol


def run_calc(cfm, dry_bulb, wet_bulb, elev):
    calculations = dict()
    # elev = 1001
    # cfm = 1000
    atm_pressure = psychro.psychro_atm(elev)
    calculations["Atmospheric Pressure"] = atm_pressure
    vapor_pres_sat = psychro.psychro_pvs(dry_bulb)
    calculations["Vapor Press. at saturation"] = vapor_pres_sat
    vapor_pres = psychro.psychro_pv1(dry_bulb, wet_bulb, atm_pressure)
    calculations["Vapor Pressure"] = vapor_pres
    dew_point = psychro.psychro_dp(vapor_pres)
    calculations["Dew Point Temoerature"] = dew_point
    rel_humidity = psychro.psychro_rh(dry_bulb, wet_bulb, atm_pressure)
    calculations["Relative Humidity"] = rel_humidity
    humidity_ratio = psychro.psychro_w(dry_bulb, wet_bulb, atm_pressure)
    calculations["Humidity Ratio"] = humidity_ratio
    enthalpy = psychro.psychro_h(dry_bulb, wet_bulb, atm_pressure)
    calculations["Enthalpy"] = enthalpy
    sp_vol = psychro.psychro_v(dry_bulb, wet_bulb, atm_pressure)
    calculations["Specific Volume"] = sp_vol
    mass_flow_rate_dry = cfm / sp_vol
    calculations["Mass Flow Rate, dry air"] = mass_flow_rate_dry
    mass_flow_rate_wv = humidity_ratio * mass_flow_rate_dry
    calculations["Mass Flow Rate, water vapor"] = mass_flow_rate_wv
    mass_flow_rate_ma = mass_flow_rate_dry + mass_flow_rate_wv
    calculations["Mass Flow Rate, moist air"] = mass_flow_rate_ma
    return calculations


def main():
    air_flow_1 = run_calc(1000, 96, 75, 1000)
    atm_pres = air_flow_1["Atmospheric Pressure"]
    enthalpy_1 = air_flow_1["Enthalpy"]
    humidity_ratio_1 = air_flow_1["Humidity Ratio"]
    mass_flow_rate_dry_1 = air_flow_1["Mass Flow Rate, dry air"]
    mass_flow_rate_wv_1 = air_flow_1["Mass Flow Rate, water vapor"]
    mass_flow_rate_ma_1 = air_flow_1["Mass Flow Rate, moist air"]
    air_flow_2 = run_calc(100, 75, 62.5, 1000)
    enthalpy_2 = air_flow_2["Enthalpy"]
    humidity_ratio_2 = air_flow_2["Humidity Ratio"]
    mass_flow_rate_dry_2 = air_flow_2["Mass Flow Rate, dry air"]
    mass_flow_rate_wv_2 = air_flow_2["Mass Flow Rate, water vapor"]
    mass_flow_rate_ma_2 = air_flow_2["Mass Flow Rate, moist air"]
    mass_flow_rate_dry_m = mass_flow_rate_dry_1 + mass_flow_rate_dry_2
    mass_flow_rate_wv_m = mass_flow_rate_wv_1 + mass_flow_rate_wv_2
    mass_flow_rate_ma_m = mass_flow_rate_dry_m + mass_flow_rate_wv_m
    enthalpy_m = ((enthalpy_1 * mass_flow_rate_ma_1) +
                    (enthalpy_2 * mass_flow_rate_ma_2)) / mass_flow_rate_ma_m
    wet_bulb_m = psychro.psychro_wet_bulb(dry_bulb_mixed, enthalpy_m, atm_pres)
    humidity_ratio_m = ((humidity_ratio_1 * mass_flow_rate_ma_1) +
                        (humidity_ratio_2 + mass_flow_rate_ma_2)) / mass_flow_rate_ma_m
    air_flow_m = run_calc_m(dry_bulb_mixed, wet_bulb_m, atm_pres)
    print(wet_bulb_m)


main()
