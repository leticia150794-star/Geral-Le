"""Pranchas de detalhamento (segunda etapa)."""
import math
from cad import *
import calc
from sheets import done, notes, f2, COL_AF, COL_ES, wet_points

DOOR_TAG = {"lab": "P2", "crit": "PCF-120", "teach": "P3", "stair": "PCF-90", "san": "P1"}
DOOR_W = {"P1": 0.90, "P2": 1.10, "P3": 1.60, "PCF-90": 1.00, "PCF-120": 1.10}


def furniture(s, r):
    x0, y0, x1, y1 = box(r); k = r["kind"]; M = "MOBILIA"
    if k == "lab":
        s.rect(x0, y0, x1 - x0, 0.75, M)
        for b in range(r["b0"], r["b1"]):
            for ox in (1.95, 4.35): s.rect(b * BAY + ox, y0 + 1.95, 1.5, 5.2, M); s.line((b * BAY + ox + 0.75, y0 + 1.95), (b * BAY + ox + 0.75, y0 + 7.15), M)
            if r.get("wet"):
                for ox in (1.8, 5.4): s.rect(b * BAY + ox - 0.3, y0 + 0.15, 0.6, 0.45, "HID_AF")
        s.rect(x1 - 1.0, y1 - 1.6, 1.0, 1.5, M); s.text("CAPELA", (x1 - 0.5, y1 - 0.85), 1.5, M, rot=90)
        if r.get("wet"): s.circle((x0 + 2.6, y1 - 0.7), 0.3, "HID_AP"); s.text("CE", (x0 + 3.3, y1 - 0.7), 1.6, "HID_AP")
    elif k == "off":
        for b in range(r["b0"], r["b1"]):
            for c in (0.9, 4.1):
                for j in range(4):
                    yy = y0 + 1.6 + j * 2.0; s.rect(b * BAY + c, yy, 1.4, 0.7, M); s.circle((b * BAY + c + 0.7, yy - 0.4), 0.22, M)
    elif k == "teach" and "AUDIT" in r["name"]:
        xm = (x0 + x1) / 2; s.rect(x0 + 0.6, y1 - 1.9, x1 - x0 - 1.2, 1.3, M); s.text("PALCO", (xm, y1 - 1.25), 1.8, M)
        for j in range(6):
            yy = y0 + 1.6 + j * 1.0
            s.rect(x0 + 1.2, yy, xm - x0 - 2.0, 0.5, M); s.rect(xm + 0.8, yy, x1 - xm - 2.0, 0.5, M)
        s.text("6 fileiras x 20 poltronas = 120 lugares", (xm, y0 + 0.9), 1.6, M)
    elif k == "teach":
        for j in range(4):
            yy = y0 + 1.5 + j * 1.9; s.rect(x0 + 1.0, yy, x1 - x0 - 2.0, 0.7, M)
        s.text("4 fileiras x 10 postos = 40 postos", ((x0 + x1) / 2, y0 + 0.8), 1.6, M)
    elif k == "crit":
        n = int((x1 - x0 - 1.0) / 1.0)
        ya, yb_ = (y1 - 1.2, y0 + 3.8) if r["band"] == "N" else (y0 + 0.2, y0 + 4.6)
        for i in range(n):
            s.rect(x0 + 0.5 + i * 1.0, ya, 0.9, 1.0, M); s.rect(x0 + 0.5 + i * 1.0, yb_, 0.9, 1.0, M)
    elif k == "sup":
        s.rect(x0, y0 if r["band"] == "S" else y1 - 0.6, x1 - x0, 0.6, M)
        if r.get("wet"):
            for b in range(r["b0"], r["b1"]):
                for ox in (1.8, 5.4): s.rect(b * BAY + ox - 0.3, y0 + 0.1, 0.6, 0.45, "HID_AF")
    elif k == "san":
        xm = (x0 + x1) / 2; s.line((xm, y0 + 1.6), (xm, y1)); s.line((x0, y0 + 1.6), (x1, y0 + 1.6))
        for i in range(4):
            for xx in (x0, x1 - 0.95):
                s.rect(xx, y1 - 1.5 - i * 1.5, 0.95, 1.5, M); s.rect(xx + 0.2, y1 - 1.0 - i * 1.5, 0.45, 0.6, M)
        for i in range(3):
            s.circle((xm - 0.45, y0 + 2.4 + i * 0.9), 0.22, M); s.circle((xm + 0.45, y0 + 2.4 + i * 0.9), 0.22, M)
    elif k == "stair":
        if r["band"] == "N": stair(s, x0 + 0.3, y1 - 6.5)
        else:
            stair(s, x0 + 0.3, y0 + 0.3)
            for i in range(2): s.rect(x0 + 3.4 + i * 1.75, y0 + 0.3, 1.6, 2.4, M); s.text("ELEV", (x0 + 4.2 + i * 1.75, y0 + 1.5), 1.8, M)
            s.rect(x0 + 3.4, y0 + 3.2, 3.35, 1.4, M); s.text("SHAFTS ELE / DADOS", (x0 + 5.07, y0 + 3.9), 1.6, M)


def block_plan(code, fl, blk):
    lo, hi = (0, 8) if blk == "A" else (7, 15)
    s = Sheet(code, f"Arquitetura - {FLOOR_NAME[fl].lower()} - bloco {blk} - layout", 100, (110 - lo * 72, 300))
    xl, xh = lo * BAY, hi * BAY; rooms = [r for r in FLOORS[fl] if r["b0"] >= lo and r["b1"] <= hi]
    xa, xb = xl - (WE if lo == 0 else 0), xh + (WE if hi == NB else 0)
    s.line((xa, -WE), (xb, -WE)); s.line((xa, YA + WE), (xb, YA + WE))
    if lo == 0: s.line((-WE, -WE), (-WE, YA + WE))
    else: s.line((xl, -1.5), (xl, YA + 1.5), "EIXO"); s.text("CONTINUA NO BLOCO A", (xl - 0.6, 4.8), 2, "COTA", rot=90)
    if hi == NB: s.line((L + WE, -WE), (L + WE, YA + WE))
    else: s.line((xh, -1.5), (xh, YA + 1.5), "EIXO"); s.text("CONTINUA NO BLOCO B", (xh + 0.6, 4.8), 2, "COTA", rot=90)
    rows = [["AMBIENTE", "AREA UTIL (m2)", "LARG. x PROF. (m)", "PERIMETRO (m)", "PORTAS"]]
    for r in rooms:
        x0, y0, x1, y1 = box(r); ds = doors(r); k = r["kind"]; tag = DOOR_TAG.get(k, "P1")
        s.line((x0, y0), (x0, y1)); s.line((x1, y0), (x1, y1))
        if r["band"] == "N": s.line((x0, y1), (x1, y1)); edge(s, (x0, y0), (x1, y0), ds); yd, sg = y0, 1
        else: s.line((x0, y0), (x1, y0)); edge(s, (x0, y1), (x1, y1), ds); yd, sg = y1, -1
        for dx, dw in ds:
            if k == "hall": continue
            if k == "teach":
                for xx in (dx, dx + dw): s.line((xx, yd - sg * 0.15), (xx, yd - sg * (0.15 + dw / 2)), "ESQUADRIA")
            else:
                s.line((dx, yd), (dx, yd + sg * dw), "ESQUADRIA"); s.arc((dx, yd), dw, 0 if sg > 0 else 270, 90 if sg > 0 else 360, "ESQUADRIA")
            s.text(tag, (dx + dw / 2, yd - sg * 0.55), 1.7, "ESQUADRIA")
        if k not in ("crit", "stair"):
            yw = YA if r["band"] == "N" else YD
            for b in range(r["b0"], r["b1"]):
                for cx in (b * BAY + 1.8, b * BAY + 5.4):
                    s.rect(cx - 1.2, yw - WE, 2.4, 2 * WE, "ESQUADRIA"); s.line((cx - 1.2, yw), (cx + 1.2, yw), "ESQUADRIA")
                    s.text("J1", (cx, yw + (0.6 if r["band"] == "N" else -0.6)), 1.7, "ESQUADRIA")
        furniture(s, r)
        cx, cy = (x0 + x1) / 2, (y0 + 1.1) if r["band"] == "N" else (y1 - 1.2)
        if k == "stair": cy = (y0 + 1.1) if r["band"] == "N" else (y1 - 2.6)
        a = (x1 - x0) * (y1 - y0)
        s.text(r["name"], (cx + (1.2 if k != "stair" else 0), cy + 0.3), 2.4); s.text(f"{f2(a, 1)} m2", (cx + (1.2 if k != "stair" else 0), cy - 0.3), 2.0)
        rows.append([r["name"], f2(a, 1), f"{f2(x1 - x0)} x {f2(y1 - y0)}", f2(2 * (x1 - x0 + y1 - y0), 1), f"{len(ds)} x {tag}" if k != "hall" else "vao livre"])
    s.line((xa + (WE if lo == 0 else 0), YC + WI), (xa + (WE if lo == 0 else 0), YB - WI)) if lo == 0 else None
    if hi == NB: s.line((L - WE, YC + WI), (L - WE, YB - WI))
    for xj in (7 * BAY, 8 * BAY):
        s.line((xj, YC + WI), (xj, YC + 0.3)); s.line((xj, YB - WI), (xj, YB - 0.3))
        s.line((xj, YC + 0.3), (xj + 0.8, YC + 0.65), "ESQUADRIA"); s.line((xj, YB - 0.3), (xj + 0.8, YB - 0.65), "ESQUADRIA"); s.text("PCF-90", (xj + 1.3, (YB + YC) / 2), 1.7, "ESQUADRIA")
    s.text("CIRCULACAO - largura livre 2,25", ((xl + xh) / 2 - 8, (YB + YC) / 2), 2.2); s.level(LEVELS[fl], ((xl + xh) / 2 + 6, (YB + YC) / 2 - 0.3))
    for i in range(lo, hi + 1):
        x = i * BAY; s.line((x, -2.0), (x, YA + 3.6), "EIXO"); s.tag(str(i + 1), (x, YA + 4.2), 3.5, "EIXO", 2.5)
        for y in (YD - 0.1, YC - 0.7, YB, YA - 0.6): s.solid(x - 0.2, y, 0.4, 0.7)
        if i < hi: s.dim((x, YA), (x + BAY, YA), 1.8, None, 2.2)
    s.dim((xl, YA), (xh, YA), 2.8, f2(xh - xl), 2.2)
    for n, y in zip("DCBA", (YD, YC, YB, YA)): s.line((xl - 3.4, y), (xh + 1.5, y), "EIXO"); s.tag(n, (xl - 4.0, y), 3.5, "EIXO", 2.5)
    for a, b in ((YD, YC), (YC, YB), (YB, YA)): s.dim((xl, a), (xl, b), -1.8, None, 2.2)
    s.dim((xl, YD), (xl, YA), -2.8, "21,60", 2.2)
    # cadeia de paredes da faixa sul
    xs = sorted({r["b0"] * BAY for r in rooms if r["band"] == "S"} | {xh})
    for a, b in zip(xs, xs[1:]): s.dim((a, YD), (b, YD), -1.6, None, 2.2)
    s.text(f"PLANTA DO {FLOOR_NAME[fl]} - BLOCO {blk} - LAYOUT   nivel +{f2(LEVELS[fl])}   escala 1:100", (xl, -4.2), 3.5, "NOTA", "l")
    s.text("QUADRO DE AMBIENTES", (xl, -6.3), 2.8, "NOTA", "l"); s.table(rows, (xl, -7.0), [80, 30, 40, 30, 34], 2.2)
    notes(s, "LEGENDA", ["P1  porta de madeira 0,90 x 2,10", "P2  porta de laboratorio 1,10 x 2,10 com visor", "P3  porta dupla 1,60 x 2,10, abre no sentido da saida",
                         "PCF-90 / PCF-120  porta corta-fogo", "J1  janela 2,40 x 1,50, peitoril 1,10", "CE  chuveiro e lava-olhos de emergencia",
                         "Bancadas: fachada 0,75 m; ilhas 1,50 x 5,20 m", "Layout de mobiliario indicativo, a validar", "com cada grupo de pesquisa."], (xl + 26, -6.3), 2.3)
    done(s)


def esquadrias():
    cnt = {}
    for fl in "T12":
        for r in FLOORS[fl]:
            if r["kind"] == "hall": continue
            t = DOOR_TAG.get(r["kind"], "P1"); cnt[t] = cnt.get(t, 0) + len(doors(r))
            if r["kind"] not in ("crit", "stair"): cnt["J1"] = cnt.get("J1", 0) + 2 * (r["b1"] - r["b0"])
    cnt["PCF-90"] += 2 * 3 + 3      # portas das juntas no corredor + saidas das escadas no terreo
    return cnt


def det_san_escada():
    s = Sheet("DET-02", "Detalhes - sanitarios, escada e quadro de esquadrias", 50, (60, 250)); W_, D_ = 7.05, 9.425; M = "MOBILIA"

    def san(ox, hid=False):
        s.rect(ox - 0.15, -0.15, W_ + 0.3, D_ + 0.3); s.rect(ox, 0, W_, D_); xm = ox + W_ / 2
        s.line((xm - 0.075, 1.8), (xm - 0.075, D_)); s.line((xm + 0.075, 1.8), (xm + 0.075, D_)); s.line((ox, 1.8), (ox + 2.4, 1.8)); s.line((ox + W_ - 2.4, 1.8), (ox + W_, 1.8))
        s.rect(ox + 2.55, 0, 1.95, 1.7); s.text("SANIT. ACESSIVEL", (ox + 3.52, 1.3), 1.8); s.text("1,95 x 1,70", (ox + 3.52, 0.95), 1.6); s.rect(ox + 2.7, 0.15, 0.45, 0.65, M); s.circle((ox + 4.2, 0.35), 0.2, M)
        s.text("DML", (ox + 5.8, 0.9), 1.8); s.rect(ox + 6.2, 0.2, 0.6, 0.6, M); s.text("HALL", (ox + 1.2, 0.9), 1.8)
        for side, x in (("FEM.", ox), ("MASC.", ox + W_ - 0.95)):
            for i in range(4):
                if side == "MASC." and i > 1:
                    s.rect(x + 0.55, D_ - 1.1 - i * 1.0 + 0.2, 0.4, 0.5, M); continue
                s.rect(x, D_ - 1.5 - i * 1.5, 0.95, 1.5, M); s.rect(x + 0.25, D_ - 1.0 - i * 1.5, 0.45, 0.65, M)
            s.text(side, (ox + (1.9 if side == "FEM." else W_ - 1.9), D_ - 0.6), 2.2)
        for i in range(3):
            for xx in (xm - 0.55, xm + 0.55): s.rect(xx - 0.3, 2.6 + i * 1.0, 0.6, 0.5, M); s.circle((xx, 2.85 + i * 1.0), 0.17, M)
        s.dim((ox, D_), (ox + W_, D_), 0.8); s.dim((ox, 0), (ox, D_), -0.8); s.dim((ox, D_ - 1.5), (ox + 0.95, D_ - 1.5), -0.0, "0,95")
        if hid:
            s.circle((ox + 3.6, 2.2), 0.12, "HID_AF"); s.text("AF-1 40 mm", (ox + 3.6, 1.95), 1.5, "HID_AF")
            for x in (ox + 0.5, ox + W_ - 0.5): s.line((ox + 3.6, 2.2), (x, 2.2), "HID_AF"); s.line((x, 2.2), (x, D_ - 0.4), "HID_AF"); s.text("AF 25", (x + (0.5 if x < xm else -0.5), 5), 1.5, "HID_AF", rot=90)
            s.line((xm, 2.2), (xm, 5.2), "HID_AF")
            s.circle((ox + 3.3, D_ - 0.3), 0.14, "HID_ES"); s.text("TQ-1 DN 100 + CV DN 75", (ox + 3.5, D_ - 0.75), 1.5, "HID_ES")
            for x in (ox + 0.75, ox + W_ - 0.75): s.line((x, D_ - 5.6), (x, D_ - 0.3), "HID_ES"); s.line((x, D_ - 0.3), (ox + 3.3, D_ - 0.3), "HID_ES"); s.text("ES 100, i = 1 %", (x + (0.35 if x < xm else -0.35), 6.5), 1.5, "HID_ES", rot=90)
            s.line((xm + 0.3, 2.6), (xm + 0.3, D_ - 0.3), "HID_ES"); s.text("ES 50 lavatorios", (xm + 0.6, 6.0), 1.5, "HID_ES", rot=90)
            for (x, y) in ((ox + 1.9, 4), (ox + W_ - 1.9, 4)): s.rect(x - 0.1, y - 0.1, 0.2, 0.2, "HID_ES"); s.text("RS", (x, y - 0.35), 1.4, "HID_ES")

    san(0); s.text("SANITARIOS - ARQUITETURA   1:50", (0, -1.2), 3.0, "NOTA", "l")
    san(9.5, True); s.text("SANITARIOS - AGUA FRIA E ESGOTO   1:50", (9.5, -1.2), 3.0, "NOTA", "l")
    # escada
    ox, oy = 19.5, 0.5; s.rect(ox - 0.15, oy - 0.15, 3.5 + 0.3, 6.6 + 0.3); s.rect(ox, oy, 3.5, 6.6)
    fx = ox + 0.45
    for i in range(13):
        yy = oy + 1.3 + i * 0.28; s.line((fx, yy), (fx + 1.2, yy), M); s.line((fx + 1.4, yy), (fx + 2.6, yy), M)
    s.rect(fx + 1.2, oy + 1.3, 0.2, 3.36, M); s.rect(fx, oy, 2.6, 1.3, M); s.rect(fx, oy + 4.66, 2.6, 1.3, M)
    s.dim((fx, oy + 6.6), (fx + 1.2, oy + 6.6), 0.6, "1,20"); s.dim((fx + 1.4, oy + 6.6), (fx + 2.6, oy + 6.6), 0.6, "1,20")
    s.dim((ox, oy + 1.3), (ox, oy + 4.66), -0.7, "12 x 0,28 = 3,36"); s.dim((ox, oy), (ox, oy + 1.3), -0.7, "1,30"); s.dim((ox, oy + 4.66), (ox, oy + 5.96), -0.7, "1,30")
    s.text("SOBE", (fx + 0.6, oy + 0.65), 1.8, M); s.text("patamar", (fx + 1.3, oy + 5.3), 1.6, M)
    s.text("ESCADA ENCLAUSURADA TIPO   1:50", (ox - 0.8, -1.2), 3.0, "NOTA", "l")
    s.lines(["Desnivel 4,50 m = 26 espelhos de 17,3 cm", "2 lances de 13 espelhos; piso de 28 cm", "2 x 17,3 + 28 = 62,6 cm (Blondel: 63 a 64)",
             "Largura de cada lance 1,20 m", "Corrimao continuo nos dois lados, h = 0,92 m", "Guarda-corpo h = 1,10 m", "Porta corta-fogo P-90 de 1,00 x 2,10 m",
             "Paredes TRRF 120; sem instalacoes cruzando a caixa", "Verificar largura pela populacao (NBR 9077)"], (ox - 0.8, -2.2), 2.2)
    c = esquadrias()
    spec = {"P1": ("0,90 x 2,10", "Madeira laminada, batente metalico"), "P2": ("1,10 x 2,10", "Laminado melaminico com visor 20 x 60, mola e barra"),
            "P3": ("1,60 x 2,10 (2 folhas)", "Abre no sentido da saida, barra antipanico"), "PCF-90": ("1,00 x 2,10", "Corta-fogo 90 min, com mola; no corredor com eletroima"),
            "PCF-120": ("1,10 x 2,10", "Corta-fogo 120 min nas salas criticas"), "J1": ("2,40 x 1,50, peitoril 1,10", "Aluminio anodizado, vidro laminado 8 mm, maxim-ar")}
    rows = [["TIPO", "DIMENSOES (m)", "QUANT.", "ESPECIFICACAO"]] + [[k, spec[k][0], str(c[k]), spec[k][1]] for k in ("P1", "P2", "P3", "PCF-90", "PCF-120", "J1")]
    s.text("QUADRO DE ESQUADRIAS - predio inteiro", (0, -6.0), 3.0, "NOTA", "l"); s.table(rows, (0, -6.7), [26, 50, 20, 110], 2.3)
    s.lines(["RS = ralo sifonado DN 100. Bacias com caixa acoplada; mictorios com valvula de fechamento automatico.",
             "Sanitario acessivel com barras de apoio, giro de 1,50 m e porta de 0,90 m abrindo para fora (NBR 9050)."], (0, -9.4), 2.2)
    done(s)


def fundacoes():
    s = Sheet("EST-02", "Estrutura - planta de fundacoes"); e = calc.estrutura()
    for i in range(NB + 1):
        x = i * BAY
        for y, d, bl in ((YD + 0.25, 0.6, 2.8), (YC - 0.35, 0.7, 3.2), (YB + 0.35, 0.7, 3.2), (YA - 0.25, 0.6, 2.8)):
            s.rect(x - bl / 2, y - 0.55, bl, 1.1, "EST"); sp = 3 * d / 2
            for sx in (-sp, sp): s.circle((x + sx, y), d / 2, "EST")
            s.solid(x - 0.2, y - 0.35, 0.4, 0.7)
    for y in (YD + 0.25, YC - 0.35, YB + 0.35, YA - 0.25): s.line((0, y), (L, y), "EIXO")
    grid(s, True, False)
    for xj in (7 * BAY, 8 * BAY): s.text("JUNTA", (xj + 0.3, -2.6), 1.8, "INC")
    s.text("PLANTA DE FUNDACOES   escala 1:200", (0, -7.5), 3.5, "NOTA", "l")
    s.table([["BLOCO", "PILARES", "CARGA EM SERVICO (kN)", "ESTACAS", "CARGA POR ESTACA (kN)", "BLOCO (m)"],
             ["B1 (fachada, eixos A e D)", "32", f"{e['ne']:.0f}", "2 helice continua D60", f"{e['ne'] / 2:.0f}", "1,10 x 2,80 x 1,00"],
             ["B2 (internos, eixos B e C)", "32", f"{e['ni']:.0f}", "2 helice continua D70", f"{e['ni'] / 2:.0f}", "1,10 x 3,20 x 1,20"]], (0, -12), [58, 22, 42, 46, 44, 40])
    s.lines(["Cargas: area de influencia x 5 lajes (terreo estruturado + 3 pisos + cobertura) x 12,5 kN/m2, sem peso proprio de pilares e blocos.",
             "Capacidade estrutural de referencia das estacas (tensao de 5 MPa no concreto): D60 = 1.410 kN; D70 = 1.920 kN.",
             "A capacidade geotecnica, o comprimento e ate o tipo de fundacao dependem da sondagem; em solo mole de varzea sao esperadas estacas de 15 a 25 m.",
             "Total previsto: 128 estacas (64 D60 + 64 D70). Vigas baldrame de 30 x 70 cm ligando todos os blocos nas duas direcoes.",
             "Blocos dos eixos B e C alongados no sentido longitudinal para nao interferirem entre si (eixos a 2,40 m)."], (0, -26), 2.3)
    done(s)


def hid_outros():
    s = Sheet("HID-04", "Hidraulica - agua fria e esgoto - terreo e 1o pavimento", base=True)
    for fl, oy in (("1", 0), ("T", -52)):
        sub = _Shift(s, oy); draw_plan(sub, fl, True, False)
        pts = wet_points(fl)
        for blk, col, el in (("A", "AF-2", "EL-A"), ("B", "AF-3", "EL-B")):
            xs = [p[0] for p in pts if (p[0] < 7 * BAY) == (blk == "A")]; cx, cy = COL_AF[col]
            if xs:
                s.line((min(min(xs), cx), cy + oy), (max(max(xs), cx), cy + oy), "HID_AF"); s.line((min(min(xs), cx), 1.6 + oy), (max(max(xs), COL_ES[el][0]), 1.6 + oy), "HID_EL")
                s.line((COL_ES[el][0], 1.6 + oy), (COL_ES[el][0], COL_ES[el][1] + oy), "HID_EL")
                for x in xs: s.line((x, cy + oy), (x, 0.9 + oy), "HID_AF"); s.rect(x - 0.3, 0.3 + oy, 0.6, 0.5, "HID_AF"); s.line((x + 0.2, 0.8 + oy), (x + 0.2, 1.6 + oy), "HID_EL")
        for n, p in COL_AF.items(): s.circle((p[0], p[1] + oy), 0.35, "HID_AF"); s.text(n, (p[0], p[1] + oy + 1.0), 2.2, "HID_AF")
        for n, p in COL_ES.items(): s.circle((p[0], p[1] + oy), 0.3, "HID_EL" if n[0] == "E" else "HID_ES"); s.text(n, (p[0] - 1.6, p[1] + oy - 0.2), 2.0, "HID_EL" if n[0] == "E" else "HID_ES")
        s.text(f"AGUA FRIA (azul) E ESGOTO DE LABORATORIO (magenta) - {FLOOR_NAME[fl]}   escala 1:200", (0, -7.5 + oy), 3.2, "NOTA", "l")
    notes(s, "NOTAS", ["1. Agua fria pelo entreforro do proprio", "   pavimento; esgoto de laboratorio sob a", "   laje, no entreforro do pavimento de baixo.",
                       "2. Ramal de esgoto de laboratorio DN 75 em", "   PP, i = 2 %, ate a coluna EL do bloco.", "3. No terreo o esgoto corre no vao sob a laje",
                       "   (1,20 m) ate as caixas externas.", "4. Registros de bloqueio na entrada de cada", "   laboratorio.", "5. Ver HID-01 (dimensionamento), HID-02",
                       "   (rede externa) e DET-02 (sanitarios)."])
    done(s)


class _Shift:
    """Desenha na mesma folha com deslocamento vertical."""
    def __init__(self, s, oy): self.s, self.oy, self.k = s, oy, s.k
    def _p(self, p): return (p[0], p[1] + self.oy)
    def line(self, p, q, layer="PAREDE"): self.s.line(self._p(p), self._p(q), layer)
    def rect(self, x, y, w, h, layer="PAREDE"): self.s.rect(x, y + self.oy, w, h, layer)
    def circle(self, c, r, layer="TEXTO"): self.s.circle(self._p(c), r, layer)
    def arc(self, c, r, a0, a1, layer="ESQUADRIA"): self.s.arc(self._p(c), r, a0, a1, layer)
    def solid(self, x, y, w, h, layer="PILAR"): self.s.solid(x, y + self.oy, w, h, layer)
    def text(self, t, p, mm=2.5, layer="TEXTO", al="c", rot=0): self.s.text(t, self._p(p), mm, layer, al, rot)
    def tag(self, t, p, r_mm=3.2, layer="TEXTO", mm=2.0): self.s.tag(t, self._p(p), r_mm, layer, mm)
    def level(self, z, p): self.s.level(z, self._p(p))
    def dim(self, p, q, off, txt=None, mm=2.0): self.s.dim(self._p(p), self._p(q), off, txt, mm)


ZONAS = [("Laboratorios (faixa sul)", "lab", 300, "100 % ar externo, 8 trocas/h, capelas VAV"), ("Salas criticas", "crit", 350, "Precisao, redundancia N+1, no gerador"),
         ("Salas de permanencia (faixa norte)", "off", 130, "Fan-coil com ar externo tratado"), ("Ensino", "teach", 200, "Fan-coil dedicado, controle por CO2"),
         ("Apoio e sanitarios", "sup", 120, "Fan-coil / exaustao mecanica"), ("Circulacoes e hall", "circ", 80, "Insuflamento de ar tratado")]


def clima_tab():
    area = {}
    for fl in "T12":
        for r in FLOORS[fl]:
            k = {"san": "sup", "hall": "circ", "stair": None}.get(r["kind"], r["kind"])
            if k: area[k] = area.get(k, 0) + (r["b1"] - r["b0"]) * BAY * 9.6
    area["circ"] += 3 * 108 * 2.4
    out = []
    for n, k, w, sysd in ZONAS: out.append((n, area[k], w, area[k] * w / 1000, sysd))
    return out


def clima():
    s = Sheet("CLI-01", "Climatizacao e exaustao - esquema do pavimento-tipo", base=True); draw_plan(s, "1", True, False); t = clima_tab(); tot = sum(x[3] for x in t)
    for x0_, x1_, sh in ((0.8, 7 * BAY - 0.8, 3 * BAY + 1.6), (8 * BAY + 0.8, L - 0.8, 11 * BAY + 1.6)):
        s.rect(x0_, YC - 1.5, x1_ - x0_, 0.6, "HID_AF"); s.rect(x0_, YC - 2.4, x1_ - x0_, 0.5, "INC")
        s.rect(sh - 0.6, YC - 0.75, 1.2, 0.6, "HID_AF"); s.text("PRUMADA AR EXT.", (sh + 4.2, YC - 0.45), 1.5, "HID_AF")
        s.rect(x0_, YB + 0.9, x1_ - x0_, 0.5, "HID_AP")
    for r in FLOORS["1"]:
        x0, y0, x1, y1 = box(r)
        if r["kind"] == "lab":
            for b in range(r["b0"], r["b1"]):
                for ox in (1.8, 5.4): s.line((b * BAY + ox, YC - 1.5), (b * BAY + ox, 2.0), "HID_AF"); s.rect(b * BAY + ox - 0.3, 3.0, 0.6, 0.6, "HID_AF"); s.rect(b * BAY + ox - 0.3, 6.0, 0.6, 0.6, "HID_AF")
            s.rect(x1 - 1.0, y1 - 1.6, 1.0, 1.5, "INC"); s.line((x1 - 0.5, y1 - 1.6), (x1 - 0.5, YC - 2.4), "INC")
        if r["kind"] in ("off", "teach") and r["band"] == "N":
            for b in range(r["b0"], r["b1"]): s.rect(b * BAY + 2.8, YB + 1.8, 1.6, 0.9, "HID_AP"); s.text("FC", (b * BAY + 3.6, YB + 2.25), 1.5, "HID_AP"); s.line((b * BAY + 3.6, YB + 2.7), (b * BAY + 3.6, YB + 7.5), "HID_AP")
    s.text("INSUFLAMENTO 100 % AR EXTERNO (azul) - EXAUSTAO DAS CAPELAS (vermelho) - AGUA GELADA / FAN-COILS (verde)   1o PAVIMENTO (tipo)   escala 1:200", (0, -7.5), 3.0, "NOTA", "l")
    rows = [["ZONA", "AREA (m2)", "CARGA (W/m2)", "CARGA TERMICA (kW)", "SISTEMA"]] + [[n, f2(a, 0), str(w), f2(q, 0), d] for n, a, w, q, d in t]
    rows.append(["TOTAL", f2(sum(x[1] for x in t), 0), "", f"{f2(tot, 0)} kW = {f2(tot / 3.517, 0)} TR", "Central de agua gelada: 3 resfriadores de 180 TR (2 em operacao + 1 reserva)"])
    s.table(rows, (0, -12), [60, 24, 26, 40, 135])
    vol = t[0][1] * 3.2
    s.lines([f"Vazao de ar externo dos laboratorios: {f2(t[0][1], 0)} m2 x 3,20 m x 8 trocas/h = {vol * 8:,.0f} m3/h".replace(",", "."),
             "Capelas: 0,5 m/s de velocidade de face; exaustao por dutos individuais ou coletor por prumada, com ventiladores na cobertura ligados ao gerador.",
             "Laboratorios em pressao negativa em relacao ao corredor; salas NB-2 com filtragem HEPA na exaustao.",
             "Registros corta-fogo em todo duto que atravessa parede de compartimentacao (eixos 8 e 9) ou laje.",
             "Cargas termicas por indice de area. O calculo real (NBR 16401) depende de orientacao, equipamentos e ocupacao."], (0, -32), 2.3)
    done(s)


# ---------------- quadros terminais ----------------
def circuitos(fl, blk):
    """Circuitos do QDI de um bloco/pavimento: iluminacao por faixa e tomadas de uso geral por modulo."""
    lo, hi = (0, 7) if blk == "A" else (8, 15); C = []
    for r in FLOORS[fl]:
        if not (r["b0"] >= lo and r["b1"] <= hi): continue
        nb = r["b1"] - r["b0"]; k = r["kind"]
        lum = {"stair": 4, "san": 8, "crit": 12, "sup": 12, "hall": 8}.get(k, 18) * nb
        C.append((f"Iluminacao - {r['name'].title()}", lum * 40, 1.5 if lum * 40 <= 1200 else 2.5, 10 if lum * 40 <= 1200 else 16))
        if k not in ("stair", "lab"):
            for i in range(nb): C.append((f"Tomadas - {r['name'].title()}" + (f" ({i + 1})" if nb > 1 else ""), 1700 if k != "san" else 800, 2.5, 20))
    n = 7 if blk == "A" else 7
    C.append(("Iluminacao - Circulacao", n * 2 * 20, 1.5, 10)); C.append(("Tomadas - Circulacao e limpeza", 1500, 2.5, 20))
    out = []
    for i, (d, w, sec, dj) in enumerate(C): out.append((i + 1, d, w, "RST"[i % 3], sec, dj, w / 220))
    return out


def ele_quadros():
    s = Sheet("ELE-03", "Eletrica - quadros terminais"); c = circuitos("1", "A")
    rows = [["CIRC.", "DESCRICAO", "POT. (W)", "FASE", "I (A)", "CABO (mm2)", "DISJ. (A)", "DR"]]
    for n, d, w, ph, sec, dj, i in c: rows.append([str(n), d, str(w), ph, f2(i, 1), f2(sec, 1), str(dj), "30 mA"])
    tot = sum(x[2] for x in c); fases = {p: sum(x[2] for x in c if x[3] == p) for p in "RST"}
    rows.append(["", "TOTAL INSTALADO", str(tot), "", "", "", "", ""]); rows.append(["", f"Por fase: R {fases['R']} W - S {fases['S']} W - T {fases['T']} W", "", "", "", "", "", ""])
    s.text("QDI-1A - iluminacao e tomadas de uso geral - 1o pavimento, bloco A (220 V fase-neutro)", (-6, 44), 3.0, "NOTA", "l"); y = s.table(rows, (-6, 42.5), [14, 110, 20, 14, 16, 22, 20, 16], 2.0)
    lab = [["CIRC.", "DESCRICAO", "POT. (W)", "FASE", "I (A)", "CABO (mm2)", "DISJ. (A)", "PROTECAO"]]
    L_ = [("Bancada de fachada - tomadas 1 a 4", 1500), ("Bancada de fachada - tomadas 5 a 8", 1500), ("Bancada de fachada - tomadas 9 a 11", 1500), ("Ilha 1 - lado A", 1500), ("Ilha 1 - lado B", 1500),
          ("Ilha 2 - lado A", 1500), ("Ilha 2 - lado B", 1500), ("Estufa / forno (circuito exclusivo)", 3000), ("Autoclave / equipamento trifasico", 6000), ("Capela de exaustao", 800), ("Reserva", 0), ("Reserva", 0)]
    for i, (d, w) in enumerate(L_):
        tri = "trifasico" in d
        lab.append([str(i + 1), d, str(w), "RST" if tri else "RST"[i % 3], f2(w / (380 * 1.732) if tri else w / 220, 1), "4,0" if w >= 3000 else "2,5", "25" if w >= 3000 else "20", "DR 30 mA + AFDD"])
    lab.append(["", "TOTAL INSTALADO POR MODULO (aprox. 300 W/m2)", str(sum(w for _, w in L_)), "", "", "", "", ""])
    s.text("QD-LAB - quadro-tipo de um modulo de laboratorio (subquadro do QDL)", (86, 44), 3.0, "NOTA", "l"); s.table(lab, (86, 42.5), [14, 100, 20, 14, 16, 22, 20, 36], 2.0)
    s.lines(["1. Os demais quadros QDI seguem a mesma regra: 1 circuito de iluminacao por ambiente e 1 circuito de tomadas por modulo de 69 m2.",
             "   A lista completa de circuitos de todos os quadros esta na planilha quantitativos-e-quadros.xlsx.",
             "2. Tomadas de emergencia (freezers) saem do QDE, nao deste quadro.",
             "3. Cada QD-LAB tem contator geral comandado por botao junto a porta, para desligar todo o laboratorio de uma vez.",
             "4. Potencias de tomadas sao de previsao; equipamentos acima de 2 kW pedem circuito exclusivo.",
             "5. Equilibrar fases no projeto executivo; queda de tensao maxima de 4 % ate o ponto mais distante."], (86, 6), 2.3)
    done(s)
