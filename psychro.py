import math


def psychro_pvs(temp):
    # Calculate vapor pressure at saturation given dry bulb temp,
    # wet bulb temp, and elevation
    a1 = -7.90298
    a2 = 5.02808
    a3 = -0.00000013816
    a4 = 11.344
    a5 = 0.0081328
    a6 = -3.49149
    b1 = -9.09718
    b2 = -3.56654
    b3 = 0.876793
    b4 = 0.0060273
    ta = (temp + 459.688) / 1.8

    if ta > 273.16:
        z = 373.16 / ta
        p1 = (z - 1) * a1
        p2 = math.log10(z) * a2
        p3 = ((10 ** ((1 - (1 / z)) * a4)) - 1) * a3
        p4 = ((10 ** (a6 * (z - 1))) - 1) * a5
    else:
        z = 273.16 / ta
        p1 = b1 * (z - 1)
        p2 = b2 * math.log10(z)
        p3 = b3 * (1 - (1 / z))
        p4 = math.log10(b4)

    return 29.921 * (10 ** (p1 + p2 + p3 + p4))


def psychro_pv1(db, wb, atm):
    # Calculate Vapor Pressure given dry bulb temp, wet bulb temp,
    # and elevation
    pvp = psychro_pvs(wb)
    ws = (pvp / (atm - pvp)) * 0.62198
    if wb <= 32:
        return (pvp - 0.0005704) * atm * ((db - wb) / 1.8)
    else:
        hl = 1093.049 + (0.441 * (db - wb))
        ch = 0.24 + (0.441 * ws)
        wh = ws - (ch * (db - wb) / hl)
    return atm * (wh / (0.62198 + wh))


def psychro_dp(this_pv):
    # Calculate dew point temp. given Vapor Pressure
    y = math.log(this_pv)
    if this_pv < 0.18036:
        return 71.98 + (24.873 * y) + (0.8927 * y ** 2)
    else:
        return 79.047 + (30.579 * y) + (1.8893 * y ** 2)


def psychro_h(db, wb, atm):
    # Calculate Enthalpy given dry bulb temp, wet bulb temp, and elevation
    return (db * 0.24) + ((1061 + (0.444 * db)) * (psychro_w(db, wb, atm)))


def psychro_rh(db, wb, atm):
    # Calculate relative humidity given dry bulb temp, wet bulb temp,
    # and elevation
    return 100 * psychro_pv1(db, wb, atm) / psychro_pvs(db)


def psychro_v(db, wb, atm):
    # Calculate Specific Volume given dry bulb temp, wet bulb temp,
    # and elevation
    return (0.754 * (db + 459.7) *
            (1 + (7000 * psychro_w(db, wb, atm) / 4360))) / atm


def psychro_w(db, wb, atm):
    # Calculate Humidity Ratio given dry bulb temp, wet bulb temp,
    # and elevation
    vp = psychro_pv1(db, wb, atm)
    return 0.622 * vp / (atm - vp)


def psychro_wrh(db, rh, atm):
    # Calculate Humidity Ratio given dry bulb temp, relative humidity,
    # and elevation
    wsat = psychro_pvs(db)
    wtemp = 0.62198 * (wsat / (atm - wsat))
    return (rh / 100) * wtemp


def psychro_atm(elev):
    # Calculate Atmospheric pressure given elevation
    elev_map = {
        -1000: 31.02,
        -500: 30.47,
        0: 29.921,
        500: 29.38,
        1000: 28.86,
        2000: 27.82,
        3000: 26.82,
        4000: 25.82,
        5000: 24.9,
        6000: 23.98,
        7000: 23.09,
        8000: 22.22,
        9000: 21.39,
        10000: 20.48,
        15000: 16.89,
        20000: 13.76,
        30000: 8.9,
        40000: 5.56,
        50000: 3.44,
        60000: 2.14
    }
    min_list = []
    for key in elev_map:
        min_list.append(min(key, elev))
    while elev in min_list:
        min_list.remove(elev)
    return elev_map[max(min_list)]


def psychro_wb(db, h, atm):
    wbtest = db
    while True:
        htest = 0.24 * wbtest + (1061 + 0.444 * wbtest) *\
            psychro_w(wbtest, wbtest, atm)
        wbtest = wbtest - 1
        if htest < h:
            wbtest = wbtest + 2
            break
    while True:
        htest = 0.24 * wbtest + (1061 + 0.444 * wbtest) *\
            psychro_w(wbtest, wbtest, atm)
        wbtest = wbtest - 0.1
        if htest < h:
            wbtest = wbtest + 0.1
            break
    return wbtest
