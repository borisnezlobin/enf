/**
 * Code from mainsfrequency.com that gets European mains frequency data.
 * I translated this code to Python to get the data. mainsfrequency.com may be very against this.
 * Comments/Names are in German to preserve authenticity :)
 * This code has not been modified past formatting.
 */

let url0 = '', req = 0;
let urlProtokoll = 'https', urldomain = 'netzfrequenzmessung.de', urlPort = '9081', urlPage = 'frequenz02c.xml'; // 10.01.2023 Umbau auf 9081
let pfeil_pos = 1;
let frequenz = 0.0;
let frequenzAlt = 50.2;
let frequenzDelta = 0.0;
let frequenzPos = 50.2;
let masse = 5.0;
let feder = 75;
let daempfung = 3.0;
let beschl = 0;
let geschwindigkeit = 0;
let frequenzLinPol = 50.2;
let phasenwinkel = 0.0;
let phasenwinkelAlt = 0.0;
let phasenwinkelDelta = 0.0;
let RL = 0.0;
let RLAlt = 0.0;
let RLDelta = 0.0;
let RLPos = 0.0;
let pfeil_RL = 1;
let ergebnis = "ab";

let Winkel = -0.001;
let phasenwinkeltext = "  0";
let size = 20;
let sperr = false; let aktiv_a;

function AjaxAufruf() {
    if (req) {
        if ("withCredentials" in req) {  // nur wenn Browser CORS unterstützt gibt es Credentials
            req.open("GET", url0 + "?c=" + Math.round(Math.random() * 100000) * 31, true);  // verschiedene Namen da IE sonst cacht und nix erneuert
            req.onreadystatechange = CallbackFkt;
            req.setRequestHeader('Content-Type', "text/plain");
            try { req.send(null); } catch (e) { console.log('Fehler: ' + e); }
        }
    }
}


/** BEGIN INSERTED CODE */

// this is a sample fetch request being made to the server (c is randomly generated):
await fetch("https://netzfrequenzmessung.de:9081/frequenz02c.xml?c=2575511", {
    "credentials": "omit",
    "headers": {
        "User-Agent": "xxxxx",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "text/plain",
        "Sec-GPC": "1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site"
    },
    "referrer": "https://www.mainsfrequency.com/",
    "method": "GET",
    "mode": "cors"
});

// The response is an XML document with the following structure:
// <r>
// <f2>50.014</f2>
// <n>C_298</n>
// <z> 01.08.2024 01:26:59</z>
// <p>312.3</p>
// <d>007</d>
// <dt>0</dt>
// </r>

// z is the timestamp we need
// f2 is the frequency we need
// d is the phase angle (idk what this is)