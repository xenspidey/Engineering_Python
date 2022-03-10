onload = function () {
    var e = document.getElementById('mod');
    e.oninput = mod;
};
function log10(val) {
    "use strict";
	return Math.log(val) / Math.LN10;
}

function psychro_pvs(temp) {
    "use strict";
	var a1 = -7.90298,
	    a2 = 5.02808,
	    a3 = -0.00000013816,
	    a4 = 11.344,
	    a5 = 0.0081328,
	    a6 = -3.49149,
	    b1 = -9.09718,
	    b2 = -3.56654,
	    b3 = 0.876793,
	    b4 = 0.0060273,
	    ta = (temp + 459.688) / 1.8,
	    z,
        p1,
        p2,
        p3,
        p4;
	
	if (ta > 273.16) {
		z = 373.16 / ta;
		p1 = (z - 1) * a1;
		p2 = log10(z) * a2;
		p3 = (Math.pow(10, ((1 - (1 / z)) * a4)) - 1) * a3;
		p4 = (Math.pow(10, (a6 * (z - 1))) - 1) * a5;
	} else {
		z = 273.16 / ta;
		p1 = b1 * (z - 1);
		p2 = b2 * log10(z);
		p3 = b3 * (1 - (1 / z));
		p4 = log10(b4);
	}
	return (29.921 * (Math.pow(10, (p1 + p2 + p3 + p4))));
}

function psychro_atm(elev) {
    "use strict";
    //formula for stmospheric pressure
    //p is pressure in Pa, h is altitude in m
    //p = 101325*(1 - 2.25577*10^-5*h)^5.25588

    //convert feet to m
    elev = elev / 3.2808;
  
    //get pressure from elevation
    var pressure = 101325 * Math.pow((1 - 2.25577 * Math.pow(10, (-5)) * elev), 5.25588);
  
    //convert pa to in hg
    pressure = pressure * 2.96 * Math.pow(10, -4);
    return pressure;
}

function psychro_pv1(db, wb, atm) {
    "use strict";
	var pvp = psychro_pvs(wb),
        ws = (pvp / (atm - pvp)) * 0.62198,
        hl,
        ch,
        wh;
	if (wb <= 32) {
		return ((pvp - 0.0005704) * atm * ((db - wb) / 1.8));
	} else {
        hl = 1093.049 + (0.441 * (db - wb));
        ch = 0.24 + (0.441 * ws);
        wh = ws - (ch * (db - wb) / hl);
		return (atm * (wh / (0.62198 + wh)));
	}
}
function psychro_w(db, wb, atm) {
    "use strict";
    var vp = psychro_pv1(db, wb, atm);
    return (0.622 * vp / (atm - vp));
}

function psychro_h(db, wb, elev) {
    "use strict";
    var atm = psychro_atm(elev);
    return ((db * 0.24) + ((1061 + (0.444 * db)) * (psychro_w(db, wb, atm))));
}
function psychro_v(db, wb, atm) {
  return ((0.754 * (db + 459.7) * (1 + (7000 * psychro_w(db, wb, atm) / 4360))) / atm);
}


function psychro_wb(db, h, atm){
    "use strict";
    var wbtest = db;
    do{
      var htest = ((0.24 * wbtest + (1061 + 0.444 * wbtest)) * psychro_w(wbtest, wbtest, atm));
      wbtest--;
      console.log("htest:", htest, "h:", h, "wbtest:", wbtest);
    }    
    while(htest > h);
    console.log("wbtest", wbtest);
    wbtest += 2;
    do {
        console.log("htest1:", htest);
        console.log("wbtest1:", wbtest);
      var htest = ((0.24 * wbtest + (1061 + 0.444 * wbtest)) * psychro_w(wbtest, wbtest, atm));
      wbtest -= 0.1;
    }
    while (htest > h);
    wbtest += 0.1;
    return (wbtest);
}

//main function that launches everything
function go() {
    "use strict";
	//validate input    
	//calculate()    
	var db_1 = parseInt(document.getElementById("db_1").value, 10),
        wb_1 = parseInt(document.getElementById("wb_1").value, 10),
        db_2 = parseInt(document.getElementById("db_2").value, 10),
        wb_2 = parseInt(document.getElementById("wb_2").value, 10),
        db_m, wb_m,
        cfm_1 = parseInt(document.getElementById("cfm_1").value, 10),
        cfm_2 = parseInt(document.getElementById("cfm_2").value, 10),
        elev = parseInt(document.getElementById("elev").value, 10),
        atm_1, cfm_m, pvs, h_1, h_2, h_m, mfrd_1, mfrw_1, mfrm_1, mfrd_2,mfrw_2, mfrm_2, mfrd_m, mfrw_m, mfrm_m, sv_1, sv_2, sv_m;

    if (elev === "") {
        elev = 1000;
    }
    
    atm_1 = psychro_atm(elev);
    pvs = psychro_pvs(db_1);//run calcs
    cfm_1 = parseInt(cfm_1, 10);
    cfm_2 = parseInt(cfm_2, 10);
    cfm_m = cfm_1 + cfm_2;
    cfm_m = cfm_m.toFixed(0);
    document.getElementById("cfm_m").innerHTML = cfm_m.toString();
	
	//display values	
    h_1 = psychro_h(db_1, wb_1, elev);
    document.getElementById("h_1").innerHTML = h_1.toFixed(2);
    h_2 = psychro_h(db_2, wb_2, elev);
    document.getElementById("h_2").innerHTML = h_2.toFixed(2);
    db_m = ((db_1 * cfm_1) + (db_2 * cfm_2)) / cfm_m;
    document.getElementById("db_m").innerHTML = db_m.toFixed(0);

    sv_1 = psychro_v(db_1, wb_1, atm_1);
    mfrd_1 = cfm_1 / sv_1;
    mfrw_1 = psychro_w(db_1, wb_1, atm_1) * mfrd_1;
    mfrm_1 = mfrw_1 + mfrd_1;

    sv_2 = psychro_v(db_2, wb_2, atm_1);
    mfrd_2 = cfm_2 / sv_2;
    mfrw_2 = psychro_w(db_2, wb_2, atm_1) * mfrd_2;
    mfrm_2 = mfrw_2 + mfrd_2;

    mfrd_m = mfrd_1 + mfrd_2;
    mfrw_m = mfrw_1 + mfrw_2;
    mfrm_m = mfrd_m + mfrw_m;
    // console.log('1: ', mfrd_1, mfrw_1, mfrm_1);
    // console.log('2: ', mfrd_2, mfrw_2, mfrm_2);
    // console.log('m: ', mfrd_m, mfrw_m, mfrm_m);
    // console.log('sv:', sv_1, sv_2);
    // console.log('atm', atm_1);

    h_m = ((h_1 * mfrm_1) + (h_2 * mfrm_2)) / mfrm_m;
    document.getElementById("h_m").innerHTML = h_m.toFixed(2);
    // document.getElementById("h_m").style.backgroundColor = "red";
    wb_m = psychro_wb(db_m, h_m, atm_1);
    document.getElementById("wb_m").innerHTML = wb_m.toFixed(2);
    document.getElementById("wb_m").style.backgroundColor = "red";
    

}

function mod() {
    "use strict";
    var table_mod = document.getElementById("modulus");
    var table_out = document.getElementById("output");
    var table_outRows = table_out.getElementsByTagName('tr');
    var row_count = table_outRows.length;
    if (row_count > 1) {
        // var i = table_outRows.length;
        while (--row_count) {
            table_out.deleteRow(row_count);
        }
    }
    var cfm_mod = parseInt(document.getElementById("mod").value, 10),
        i,
        x,
        result = [];
    for (i = 1; i <= cfm_mod; i += 1) {
        if (cfm_mod % i === 0) {
            result.push(i);
        }
    }
    for (i = 0; i < result.length / 2; i += 1) {
        var row = table_out.insertRow(-1);
        var cell  = row.insertCell(-1);
        cell.innerHTML = result[i] + ' x ' + cfm_mod / result[i];
    }
}

//Heating leaving air temp given BTU's and CFM
function delta_t() {
    //Q = cfm*1.08*delta_t
    var Q, cfm, d_t;
    
}
