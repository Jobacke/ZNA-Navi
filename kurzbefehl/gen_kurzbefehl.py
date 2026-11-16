"""Erzeugt den Siri-Kurzbefehl „Aktuelle Leitstelle“ (unsigniert) und die Nachschlagetabelle leitstellen-index.json.

Aufruf (im Repo-Ordner):  python3 kurzbefehl/gen_kurzbefehl.py
Neu erzeugen nur nötig, wenn sich in leitstellen.json die Landkreise (Feld "kreise") oder ILS-Namen ändern.
Funkgruppen ("funk") liest der Kurzbefehl bei jedem Aufruf direkt aus leitstellen.json – dafür nichts neu erzeugen.

Ablauf des Kurzbefehls:
  Standort → Landkreis (OpenStreetMap/Nominatim, wie in der App) → Schlüssel → leitstellen-index.json → ILS-Name
  → Eintrag in leitstellen.json → Funkgruppen → Ansage per Siri.
"""
import json, os, plistlib, re, uuid

KB_VERSION = "1.0"
BASIS = "https://zna.vjbackhaus.de/"
HIER = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HIER)
OBJ = "￼"

# ---------------------------------------------------------------- Normalisierung (identisch im Kurzbefehl)
PRAEFIX = r"^(landkreis|kreisfreie stadt|stadt|kreis)\s+"
def schluessel(name):
    """So rechnet der Kurzbefehl einen Nominatim-Namen in den Schlüssel um."""
    s = name.lower()
    s = re.sub(PRAEFIX, "", s)
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]", "", s)

def ausschreiben(s):   # Abkürzungen wie in kreisSchluessel der App
    s = re.sub(r"\ba\.\s*d\.\s*", "an der ", s, flags=re.I)
    s = re.sub(r"\bi\.\s*d\.\s*", "in der ", s, flags=re.I)
    s = re.sub(r"\ba\.\s*", "am ", s, flags=re.I)
    s = re.sub(r"\bi\.\s*", "im ", s, flags=re.I)
    return s.replace("OPf.", "Oberpfalz")

def schreibweisen(kreis):
    """Alle Schreibweisen, die Nominatim für diesen Kreis liefern kann (ohne „Landkreis“-Präfix)."""
    basis = re.sub(r"\s*\((Stadt|Landkreis)\)\s*$", "", kreis)
    v = {basis, ausschreiben(basis)}
    for x in list(v):
        ohne = re.sub(r"\s*\([^)]*\)\s*$", "", x)   # „Kempten (Allgäu)“ → „Kempten“
        v.add(ohne)
    return v

def baue_index(ils):
    idx = {}
    for e in ils:
        for k in e["kreise"]:
            for w in schreibweisen(k):
                key = schluessel(w)
                if not key: continue
                if idx.get(key, e["name"]) != e["name"]:
                    raise SystemExit(f"Schlüssel „{key}“ passt zu {idx[key]} und {e['name']} – bitte prüfen")
                idx[key] = e["name"]
    return dict(sorted(idx.items()))

# ---------------------------------------------------------------- Ansage-Text (identisch im Kurzbefehl)
FUNK_ERSETZEN = [   # (Suche, Ersatz) – reguläre Ausdrücke, nacheinander
    (r"RD_Betten_[A-Za-z0-9]+", "Bettenkanal"),
    (r"RD_ILS_[A-Za-z0-9]+", "Rettungsdienst"),
    (r"RD_[0-9]+_[A-Za-z0-9]+", "Rettungsdienst"),
    (r"\s*[–-]?\s*\(?Bettenanforderung\)?", ""),
    (r"[()]", ""),
    (r"\s*–\s*", ", "),
    (r"_", " "),
    (r"([0-9])(?=[0-9])", "$1 "),           # Kurzwahl Ziffer für Ziffer: 1913 → 1 9 1 3
]
NAME_ERSETZEN = [(r"^ILS\s+", "Leitstelle "), (r"\bFFB\b", "Fürstenfeldbruck"), (r"\s*/\s*", " und ")]
KREIS_ERSETZEN = [(r"\ba\.\s*d\.\s*", "an der "), (r"\bi\.\s*d\.\s*", "in der "), (r"\ba\.\s*", "am "),
                  (r"\bi\.\s*", "im "), (r"OPf\.", "Oberpfalz")]

def py_ersetzen(text, regeln):
    for suche, ersatz in regeln:
        text = re.sub(suche, ersatz.replace("$1", r"\1"), text)
    return text

def ansage(e, kreis):
    funk = py_ersetzen(". ".join(e.get("funk", [])), FUNK_ERSETZEN)
    return (f"Zuständig ist die {py_ersetzen(e['name'], NAME_ERSETZEN)}. {py_ersetzen(kreis, KREIS_ERSETZEN)}. "
            + (f"{funk}." if funk else "Keine Kurzwahlen hinterlegt."))

# ---------------------------------------------------------------- Bausteine Kurzbefehl (wie Wissen RD)
def U(): return str(uuid.uuid4()).upper()

def var(name, key=None, dict_coerce=False):
    v = {"Type": "Variable", "VariableName": name}
    agg = []
    if dict_coerce or key:
        agg.append({"Type": "WFCoercionVariableAggrandizement", "CoercionItemClass": "WFDictionaryContentItem"})
    if key:
        agg.append({"Type": "WFDictionaryValueVariableAggrandizement", "DictionaryKey": key})
    if agg: v["Aggrandizements"] = agg
    return v

def out(uid, name, dict_coerce=False):
    o = {"Type": "ActionOutput", "OutputUUID": uid, "OutputName": name}
    if dict_coerce:
        o["Aggrandizements"] = [{"Type": "WFCoercionVariableAggrandizement", "CoercionItemClass": "WFDictionaryContentItem"}]
    return o

def att(v): return {"Value": v, "WFSerializationType": "WFTextTokenAttachment"}

def tok(*teile):
    s, ranges = "", {}
    for t in teile:
        if isinstance(t, str):
            s += t
        else:
            pos = len(s.encode("utf-16-le")) // 2
            ranges[f"{{{pos}, 1}}"] = t
            s += OBJ
    return {"Value": {"string": s, "attachmentsByRange": ranges}, "WFSerializationType": "WFTextTokenString"}

def bedingung_input(v): return {"Type": "Variable", "Variable": att(v)}

A = []
def act(ident, **p):
    A.append({"WFWorkflowActionIdentifier": "is.workflow.actions." + ident, "WFWorkflowActionParameters": p})
    return p

def text(inhalt):
    u = U(); act("gettext", UUID=u, WFTextActionText=inhalt if isinstance(inhalt, dict) else tok(inhalt)); return u

def setvar(name, v): act("setvariable", WFVariableName=name, WFInput=att(v))

def wert(quelle, key):
    u = U(); act("getvalueforkey", UUID=u, WFInput=att(quelle), WFDictionaryKey=key, WFGetDictionaryValueType="Value"); return u

def ersetzen(eingabe, regeln, regex=True):
    vorher = eingabe
    for suche, ersatz in regeln:
        u = U()
        act("text.replace", UUID=u, WFInput=tok(vorher), WFReplaceTextFind=suche, WFReplaceTextReplace=ersatz,
            WFReplaceTextRegularExpression=regex, WFReplaceTextCaseSensitive=True)
        vorher = out(u, "Aktualisierter Text")
    return vorher

def laden(url):
    u = U(); act("downloadurl", UUID=u, WFURL=tok(url), WFHTTPMethod="GET"); return u

def sprechen(t): act("speaktext", WFText=t, WFSpeakTextWait=True, WFSpeakTextLanguage="de-DE")

def wenn_start(g, **p): act("conditional", GroupingIdentifier=g, WFControlFlowMode=0, **p)
def sonst(g): act("conditional", GroupingIdentifier=g, WFControlFlowMode=1)
def wenn_ende(g): act("conditional", GroupingIdentifier=g, WFControlFlowMode=2, UUID=U())
HAT_WERT, HAT_KEINEN_WERT, IST, ENTHAELT_NICHT = 100, 101, 4, 999

def bauen():
    A.clear()
    act("comment", WFCommentActionText=f"ZNA-Navi – Kurzbefehl „Aktuelle Leitstelle“ v{KB_VERSION}\n"
        "„Hey Siri, aktuelle Leitstelle“ → sagt die am Standort zuständige ILS (nach Landkreis) und die Kurzwahlen an.\n"
        f"Daten: {BASIS}leitstellen.json (Funkgruppen) und leitstellen-index.json (Landkreis → ILS). "
        "Erzeugt mit kurzbefehl/gen_kurzbefehl.py im Repo ZNA-Navi.")

    # 1) Standort → Landkreis (Nominatim, wie in der App; Koordinaten auf 4 Stellen genügen)
    st = U(); act("getcurrentlocation", UUID=st)
    la = U(); act("properties.locations", UUID=la, WFInput=att(out(st, "Aktueller Standort")), WFContentItemPropertyName="Latitude")
    lo = U(); act("properties.locations", UUID=lo, WFInput=att(out(st, "Aktueller Standort")), WFContentItemPropertyName="Longitude")
    url = text(tok(f"https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=", out(la, "Breitengrad"),
                   "&lon=", out(lo, "Längengrad"), "&zoom=10&addressdetails=1&accept-language=de"))
    # deutsches Zahlenformat (48,077) → Punkt
    url2 = ersetzen(out(url, "Text"), [(",", ".")], regex=False)
    nom = U()
    act("downloadurl", UUID=nom, WFURL=tok(url2), WFHTTPMethod="GET", ShowHeaders=True,
        WFHTTPHeaders={"Value": {"WFDictionaryFieldValueItems": [
            {"WFItemType": 0, "WFKey": tok("User-Agent"), "WFValue": tok("ZNA-Navi-Kurzbefehl/1.0 (zna.vjbackhaus.de)")}]},
            "WFSerializationType": "WFDictionaryFieldValue"})
    setvar("Ort", out(nom, "Inhalte der URL"))
    setvar("Kreis", out(wert(var("Ort", dict_coerce=True), "address.county"), "Wörterbuchwert"))
    for feld in ("city", "town", "municipality"):          # kreisfreie Städte haben kein „county“
        g = U(); wenn_start(g, WFCondition=HAT_KEINEN_WERT, WFInput=bedingung_input(var("Kreis")))
        setvar("Kreis", out(wert(var("Ort", dict_coerce=True), "address." + feld), "Wörterbuchwert"))
        wenn_ende(g)
    setvar("Land", out(wert(var("Ort", dict_coerce=True), "address.state"), "Wörterbuchwert"))

    g = U(); wenn_start(g, WFCondition=HAT_KEINEN_WERT, WFInput=bedingung_input(var("Kreis")))
    sprechen(tok("Der Landkreis konnte gerade nicht ermittelt werden. Bitte Standort und Netz prüfen."))
    act("exit")
    wenn_ende(g)

    # Ansage-Form des Landkreises (a.d. → an der …)
    setvar("KreisSprech", ersetzen(var("Kreis"), KREIS_ERSETZEN))

    # 2) Außerhalb Bayerns
    g = U(); wenn_start(g, WFCondition=ENTHAELT_NICHT, WFConditionalActionString="Bayern", WFInput=bedingung_input(var("Land")))
    sprechen(tok("Du bist außerhalb Bayerns, in ", var("KreisSprech"), ", ", var("Land"),
                 ". Dafür ist keine Leitstelle hinterlegt."))
    act("exit")
    wenn_ende(g)

    # 3) Schlüssel bilden (identisch zu schluessel() oben) und ILS nachschlagen
    u = U(); act("text.changecase", UUID=u, text=tok(var("Kreis")), WFCaseType="lowercase")
    k = ersetzen(out(u, "Aktualisierter Text"), [(PRAEFIX, "")])
    k = ersetzen(k, [("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")], regex=False)
    k = ersetzen(k, [("[^a-z0-9]", "")])
    setvar("Schluessel", k)
    idx = laden(BASIS + "leitstellen-index.json")
    i = U()
    act("getvalueforkey", UUID=i, WFInput=att(out(idx, "Inhalte der URL", dict_coerce=True)),
        WFDictionaryKey=tok(var("Schluessel")), WFGetDictionaryValueType="Value")
    setvar("ILS", out(i, "Wörterbuchwert"))

    g = U(); wenn_start(g, WFCondition=HAT_KEINEN_WERT, WFInput=bedingung_input(var("ILS")))
    sprechen(tok("Für ", var("KreisSprech"), " wurde keine Leitstelle gefunden."))
    act("exit")
    wenn_ende(g)

    # 4) Eintrag der ILS in leitstellen.json suchen → Funkgruppen
    ls = laden(BASIS + "leitstellen.json")
    setvar("Liste", out(ls, "Inhalte der URL"))
    r = U(); act("repeat.each", GroupingIdentifier=r, WFControlFlowMode=0, WFInput=att(var("Liste")))
    n = wert(var("Repeat Item", dict_coerce=True), "name")
    g = U(); wenn_start(g, WFCondition=IST, WFConditionalActionString=tok(var("ILS")), WFInput=bedingung_input(out(n, "Wörterbuchwert")))
    setvar("Treffer", var("Repeat Item"))
    wenn_ende(g)
    act("repeat.each", GroupingIdentifier=r, WFControlFlowMode=2, UUID=U())

    f = wert(var("Treffer", dict_coerce=True), "funk")
    c = U(); act("text.combine", UUID=c, text=att(out(f, "Wörterbuchwert")), WFTextSeparator="Custom", WFTextCustomSeparator=". ")
    setvar("Funk", ersetzen(out(c, "Kombinierter Text"), FUNK_ERSETZEN))
    setvar("Name", ersetzen(var("ILS"), NAME_ERSETZEN))

    # 5) Ansage
    g = U(); wenn_start(g, WFCondition=HAT_WERT, WFInput=bedingung_input(var("Funk")))
    sprechen(tok("Zuständig ist die ", var("Name"), ". ", var("KreisSprech"), ". ", var("Funk"), "."))
    sonst(g)
    sprechen(tok("Zuständig ist die ", var("Name"), ". ", var("KreisSprech"), ". Keine Kurzwahlen hinterlegt."))
    wenn_ende(g)

    return {
        "WFWorkflowClientVersion": "2607.0.2",
        "WFWorkflowMinimumClientVersion": 900,
        "WFWorkflowMinimumClientVersionString": "900",
        "WFWorkflowIcon": {"WFWorkflowIconStartColor": 4282601983, "WFWorkflowIconGlyphNumber": 59511},
        "WFWorkflowTypes": [],
        "WFWorkflowInputContentItemClasses": ["WFStringContentItem"],
        "WFWorkflowHasOutputFallback": False,
        "WFWorkflowHasShortcutInputVariables": False,
        "WFQuickActionSurfaces": [],
        "WFWorkflowImportQuestions": [],
        "WFWorkflowActions": list(A),
    }

if __name__ == "__main__":
    ils = json.load(open(os.path.join(REPO, "leitstellen.json"), encoding="utf-8"))
    idx = baue_index(ils)
    with open(os.path.join(REPO, "leitstellen-index.json"), "w", encoding="utf-8") as fh:
        fh.write("{\n  \"_hinweis\": \"Automatisch erzeugt aus leitstellen.json mit kurzbefehl/gen_kurzbefehl.py – Landkreis-Schlüssel → ILS für den Siri-Kurzbefehl „Aktuelle Leitstelle“. Funkgruppen stehen in leitstellen.json.\",\n"
                 + ",\n".join(f"  {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)}" for k, v in idx.items()) + "\n}\n")
    with open(os.path.join(HIER, "Aktuelle Leitstelle.unsigned.shortcut"), "wb") as fh:
        plistlib.dump(bauen(), fh, fmt=plistlib.FMT_BINARY)
    print(f"leitstellen-index.json: {len(idx)} Schlüssel · Kurzbefehl: {len(A)} Aktionen")
