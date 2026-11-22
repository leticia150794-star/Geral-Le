"""Pre-dimensionamentos (valores de anteprojeto)."""
import math
from cad import FLOORS, BAY, box

BAY_AREA = BAY * 9.6
AREA_FLOOR = 108.0 * 21.6

# ---------------- ELETRICA ----------------
V = 380.0; FP = 0.92
CABOS = [(16, 100), (25, 127), (35, 158), (50, 192), (70, 246), (95, 298), (120, 346), (150, 399), (185, 456), (240, 538)]  # mm2, A (Cu EPR 90C, bandeja)
FAG = 0.80                                           # fator de agrupamento adotado
DISJ = [32, 40, 50, 63, 80, 100, 125, 160, 200, 250, 320, 400, 500, 630, 800, 1000, 1250, 1600]


def lab_bays(fl, blk):
    n = 0
    for r in FLOORS[fl]:
        if r["kind"] == "lab":
            for b in range(r["b0"], r["b1"]):
                if (b < 7) == (blk == "A"): n += 1
    return n


def feeder(dem_kw):
    i = dem_kw * 1000 / (math.sqrt(3) * V * FP); ip = i * 1.25
    dj = next(d for d in DISJ if d >= ip)
    for n in (1, 2, 3, 4):
        for sec, amp in CABOS:
            if amp * FAG * n >= dj: return i, dj, (f"{n}x" if n > 1 else "") + f"3#{sec}+N+T"
    return i, dj, "barramento blindado"


def cargas():
    """Lista (quadro, descricao, kW instalado, fator de demanda, barra)."""
    L = []
    for fl in "T12":
        for blk in "AB":
            nb = lab_bays(fl, blk)
            if nb: L.append((f"QDL-{fl}{blk}", f"Equipamentos de laboratorio ({nb} modulos x 300 W/m2)", nb * BAY_AREA * 0.300, 0.40, "N"))
    area_blk = AREA_FLOOR / 2
    for fl in "T12":
        for blk in "AB":
            L.append((f"QDI-{fl}{blk}", "Iluminacao (7 W/m2 normal) + tomadas de uso geral (25 W/m2)", area_blk * (0.007 + 0.025), (0.007 * 1.0 + 0.025 * 0.5) / 0.032, "N"))
    L += [("QF-AC", "Central de agua gelada / climatizacao (aprox. 360 TR)", 395.0, 0.90, "N"),
          ("QF-VENT", "Ventiladores de insuflamento", 40.0, 0.90, "N"),
          ("QF-ELEV1", "Elevador social", 15.0, 0.50, "N"),
          ("QDE-ILUM", "Iluminacao de emergencia e seguranca (2 W/m2)", 14.0, 1.00, "E"),
          ("QDE-EXA", "Exaustao das capelas e salas NB-2", 50.0, 0.90, "E"),
          ("QDE-ACC", "Climatizacao de precisao (data center e biorrepositorios)", 44.0, 0.90, "E"),
          ("QDE-FRZ", "Ultrafreezers e camaras frias (40 un. x 1,2 kW)", 48.0, 1.00, "E"),
          ("QDE-DC", "Data center via no-break de 80 kVA", 60.0, 1.00, "E"),
          ("QDE-ELEV2", "Elevador de emergencia / macas", 15.0, 1.00, "E"),
          ("QDE-BOMB", "Bombas de agua fria e de drenagem", 20.0, 0.50, "E")]
    out = []
    for q, d, kw, fd, bus in L:
        dem = kw * fd; i, dj, cab = feeder(dem)
        out.append(dict(q=q, d=d, kw=kw, fd=fd, dem=dem, i=i, dj=dj, cab=cab, bus=bus))
    return out


def resumo_ele():
    c = cargas(); dn = sum(x["dem"] for x in c if x["bus"] == "N"); de = sum(x["dem"] for x in c if x["bus"] == "E")
    tot = dn + de
    return dict(inst=sum(x["kw"] for x in c), dn=dn, de=de, tot=tot, kva=tot / FP, traf=2 * 750, carreg=tot / FP / 1500,
                ger_kva=de / 0.8, ger=450, i_tr=750e3 / (math.sqrt(3) * V))


# ---------------- AGUA FRIA ----------------
PESO = {"bacia": 0.3, "lav": 0.3, "mic": 0.3, "pia": 0.7, "tanque": 0.7}
PVC = [(25, 21.6), (32, 27.8), (40, 35.2), (50, 44.0), (60, 53.4), (75, 66.6), (85, 75.6), (110, 97.8)]  # DE soldavel, DI (mm)


def tubo(q_ls, vmax=1.5):
    for de, di in PVC:
        v = q_ls / 1000 / (math.pi * (di / 1000) ** 2 / 4)
        if v <= vmax: return de, v
    return PVC[-1][0], v


def pias(fl, blk=None):
    n = 0
    for r in FLOORS[fl]:
        if r.get("wet"):
            for b in range(r["b0"], r["b1"]):
                if blk is None or (b < 7) == (blk == "A"): n += 2
    return n


def agua():
    san = 8 * PESO["bacia"] + 6 * PESO["lav"] + 2 * PESO["mic"] + PESO["tanque"]      # por pavimento
    col = {"AF-1 (sanitarios)": san * 3,
           "AF-2 (laboratorios bloco A)": sum(pias(f, "A") for f in "T12") * PESO["pia"],
           "AF-3 (laboratorios bloco B)": sum(pias(f, "B") for f in "T12") * PESO["pia"]}
    rows = []
    for k, p in col.items():
        q = 0.3 * math.sqrt(p); de, v = tubo(q); rows.append((k, p, q, de, v))
    pt = sum(col.values()); q = 0.3 * math.sqrt(pt); de, v = tubo(q)
    rows.append(("Barrilete / saida do reservatorio", pt, q, de, v))
    pop = 600; cons = pop * 50 / 1000 + 10.0                 # m3/dia (50 L/pessoa + 10 m3 de processo)
    return dict(rows=rows, pop=pop, cons=cons, res=cons * 1.5, sup=24, inf=36, san_p=san)


def esgoto():
    san = 8 * 6 + 6 * 1 + 2 * 2 + 3                           # UHC por pavimento (bacia 6, lavatorio 1, mictorio 2, tanque 3)
    labA = sum(pias(f, "A") for f in "12") * 3; labB = sum(pias(f, "B") for f in "12") * 3
    return dict(san=san, tq1=san * 2, elA=labA, elB=labB)    # terreo liga direto nas caixas


def pluvial(i_mmh=150.0, n=14):
    q = i_mmh * AREA_FLOOR / 60.0
    return dict(i=i_mmh, q=q, n=n, q1=q / n, a1=AREA_FLOOR / n)


def incendio():
    spk = 8.1 * 140; hose = 950.0; t = 60
    return dict(spk=spk, hose=hose, t=t, vol=(spk + hose) * t / 1000, hid=2 * 150 * 60 / 1000, n_spk=30 * 7)


def estrutura():
    g, q = 7.5, 5.0; ai = BAY * 6.0; ae = BAY * 4.8
    ni = ai * 4 * (g + q); ne = ae * 4 * (g + q)
    return dict(g=g, q=q, ai=ai, ae=ae, ni=ni, ne=ne, nid=ni * 1.4, nrd=0.85 * 35e3 / 1.4 * 0.28)


if __name__ == "__main__":
    for x in cargas(): print(x["q"], round(x["kw"], 1), round(x["dem"], 1), round(x["i"]), x["dj"], x["cab"])
    print(resumo_ele()); print(agua()); print(esgoto()); print(pluvial()); print(incendio()); print(estrutura())
