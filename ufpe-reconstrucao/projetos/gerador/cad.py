"""Base de desenho e modelo do edificio (unidades: metros)."""
import math, os
import ezdxf
from ezdxf.enums import TextEntityAlignment as TA

OUT = "/home/user/Geral-Le/ufpe-reconstrucao/projetos"
BAY = 7.2; NB = 15; L = BAY * NB            # 108.00
YD, YC, YB, YA = 0.0, 9.6, 12.0, 21.6       # eixos D (sul) ... A (norte)
WI, WE = 0.075, 0.10                        # meia espessura parede interna / externa
LEVELS = {"T": 1.20, "1": 5.70, "2": 10.20, "C": 14.70}

LAYERS = {  # nome: (cor ACI, espessura 1/100 mm)
    "EIXO": (8, 13), "PAREDE": (7, 50), "PILAR": (7, 35), "ESQUADRIA": (4, 18), "COTA": (8, 13),
    "TEXTO": (7, 18), "MOBILIA": (9, 13), "FOLHA": (7, 35), "BASE": (9, 13),
    "HID_AF": (5, 40), "HID_ES": (30, 40), "HID_EL": (6, 40), "HID_AP": (3, 40),
    "INC": (1, 40), "ELE": (1, 35), "ELE_LUM": (2, 18), "ELE_CALHA": (6, 35), "EST": (3, 35), "NOTA": (7, 18),
}


RGB = {8: (106, 106, 106), 9: (168, 168, 168), 2: (168, 127, 0), 4: (0, 127, 159), 3: (21, 128, 61), 5: (29, 78, 216), 1: (209, 26, 26), 6: (162, 28, 175), 30: (194, 87, 10)}


class Sheet:
    """Uma prancha A1. scale = denominador (200 -> 1:200). Origem do desenho no eixo 1/D."""

    def __init__(self, code, title, scale=200, origin=(70, 340), base=False):
        self.code, self.title, self.scale = code, title, scale
        self.k = scale / 1000.0                      # 1 mm de papel em metros
        self.doc = ezdxf.new("R2010", setup=True)
        self.doc.units = 6
        self.m = self.doc.modelspace()
        for n, (c, lw) in LAYERS.items():
            ly = self.doc.layers.add(n, color=c, lineweight=lw)
            if c in RGB: ly.rgb = RGB[c]
        self.W, self.H = 841 * self.k, 594 * self.k
        self.x0, self.y0 = -origin[0] * self.k, -origin[1] * self.k
        self.base = base
        self._frame()

    # ---------- primitivas ----------
    def lay(self, layer):
        return "BASE" if (self.base and layer in ("PAREDE", "PILAR", "ESQUADRIA", "MOBILIA", "TEXTO")) else layer

    def line(self, p, q, layer="PAREDE"):
        self.m.add_line(p, q, dxfattribs={"layer": self.lay(layer)})

    def poly(self, pts, layer="PAREDE", close=False):
        self.m.add_lwpolyline(pts, close=close, dxfattribs={"layer": self.lay(layer)})

    def rect(self, x, y, w, h, layer="PAREDE"):
        self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], layer, True)

    def circle(self, c, r, layer="TEXTO"):
        self.m.add_circle(c, r, dxfattribs={"layer": self.lay(layer)})

    def arc(self, c, r, a0, a1, layer="ESQUADRIA"):
        self.m.add_arc(c, r, a0, a1, dxfattribs={"layer": self.lay(layer)})

    def solid(self, x, y, w, h, layer="PILAR"):
        hch = self.m.add_hatch(dxfattribs={"layer": self.lay(layer)})
        hch.paths.add_polyline_path([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], is_closed=True)

    def text(self, s, p, mm=2.5, layer="TEXTO", al="c", rot=0):
        a = {"c": TA.MIDDLE_CENTER, "l": TA.MIDDLE_LEFT, "r": TA.MIDDLE_RIGHT}[al]
        t = self.m.add_text(s, height=mm * self.k, dxfattribs={"layer": self.lay(layer), "rotation": rot})
        t.set_placement(p, align=a)

    def lines(self, rows, p, mm=2.5, layer="NOTA", gap=1.7):
        x, y = p
        for r in rows:
            self.text(r, (x, y), mm, layer, "l"); y -= mm * self.k * gap
        return y

    def table(self, rows, p, widths, mm=2.2, layer="NOTA"):
        """rows: listas de strings; widths em mm de papel."""
        x, y = p; rh = mm * self.k * 2.2; tw = sum(widths) * self.k
        for i, r in enumerate(rows):
            cx = x
            for w, c in zip(widths, r):
                self.text(str(c), (cx + 1.2 * self.k, y - rh / 2), mm, layer, "l"); cx += w * self.k
            self.line((x, y - rh), (x + tw, y - rh), "COTA"); y -= rh
        self.rect(x, y, tw, rh * len(rows), "COTA")
        cx = x
        for w in widths[:-1]:
            cx += w * self.k; self.line((cx, y), (cx, y + rh * len(rows)), "COTA")
        return y

    def dim(self, p, q, off, txt=None, mm=2.0):
        """Cota linear horizontal ou vertical; off desloca a linha de cota."""
        (x1, y1), (x2, y2) = p, q; t = 0.9 * self.k
        if abs(y1 - y2) < 1e-6:
            y = y1 + off; self.line((x1, y), (x2, y), "COTA")
            for x in (x1, x2):
                self.line((x, y1 + math.copysign(t, off)), (x, y + math.copysign(t, off)), "COTA"); self.line((x - t, y - t), (x + t, y + t), "COTA")
            self.text(txt or f"{abs(x2 - x1):.2f}".replace(".", ","), ((x1 + x2) / 2, y + 1.6 * self.k), mm, "COTA")
        else:
            x = x1 + off; self.line((x, y1), (x, y2), "COTA")
            for y in (y1, y2):
                self.line((x1 + math.copysign(t, off), y), (x + math.copysign(t, off), y), "COTA"); self.line((x - t, y - t), (x + t, y + t), "COTA")
            self.text(txt or f"{abs(y2 - y1):.2f}".replace(".", ","), (x - 1.6 * self.k, (y1 + y2) / 2), mm, "COTA", rot=90)

    def tag(self, s, p, r_mm=3.2, layer="TEXTO", mm=2.0):
        self.circle(p, r_mm * self.k, layer); self.text(s, p, mm, layer)

    def level(self, z, p):
        k = self.k; x, y = p
        self.poly([(x - 1.5 * k, y + 1.5 * k), (x, y), (x + 1.5 * k, y + 1.5 * k)], "COTA", True)
        self.text(("+" if z >= 0 else "") + f"{z:.2f}".replace(".", ","), (x + 2.5 * k, y + 1.2 * k), 2.0, "COTA", "l")

    # ---------- folha ----------
    def _frame(self):
        k = self.k; x, y = self.x0, self.y0
        self.rect(x + 10 * k, y + 10 * k, self.W - 20 * k, self.H - 20 * k, "FOLHA")
        bx, by, bw, bh = x + self.W - 10 * k - 185 * k, y + 10 * k, 185 * k, 62 * k
        self.rect(bx, by, bw, bh, "FOLHA")
        for dy in (14, 28, 44):
            self.line((bx, by + dy * k), (bx + bw, by + dy * k), "FOLHA")
        self.line((bx + 120 * k, by), (bx + 120 * k, by + 28 * k), "FOLHA")
        self.text("UFPE - CAMPUS RECIFE - RECONSTRUCAO DO BLOCO DE LABORATORIOS", (bx + 3 * k, by + 53 * k), 3.0, "FOLHA", "l")
        self.text(self.title.upper(), (bx + 3 * k, by + 36 * k), 3.6, "FOLHA", "l")
        self.text("ANTEPROJETO - NAO VALIDO PARA EXECUCAO - SEM LEVANTAMENTO DO TERRENO", (bx + 3 * k, by + 21 * k), 2.1, "FOLHA", "l")
        self.text("Data 22/11/2026   Rev. R00   Unid.: metro", (bx + 3 * k, by + 7 * k), 2.2, "FOLHA", "l")
        self.text(self.code, (bx + 152 * k, by + 19 * k), 7.0, "FOLHA")
        self.text(f"Escala 1:{self.scale}   Formato A1", (bx + 152 * k, by + 6 * k), 2.4, "FOLHA")
        self.tb = (bx, by + bh)                       # topo do carimbo

    def save(self):
        os.makedirs(OUT + "/dxf", exist_ok=True)
        self.doc.saveas(f"{OUT}/dxf/{self.code}.dxf")
        return self


# ================= MODELO =================
def R(b0, b1, band, name, kind, **kw):
    d = dict(b0=b0, b1=b1, band=band, name=name, kind=kind); d.update(kw); return d

E1 = R(0, 1, "N", "ESCADA E1", "stair"); E3 = R(14, 15, "N", "ESCADA E3", "stair")
E2 = R(7, 8, "S", "ESCADA E2 + ELEVADORES", "stair")
SAN = R(6, 7, "N", "SANITARIOS / DML", "san")
FLOORS = {
 "T": [E1, R(1, 3, "N", "ADMINISTRACAO E SECRETARIA", "off"), R(3, 5, "N", "SALAS DE POS-GRADUACAO", "off"), R(5, 6, "N", "CONVIVENCIA", "off"), SAN,
       R(7, 8, "N", "HALL DE ENTRADA", "hall"), R(8, 11, "N", "AUDITORIO 120 LUG.", "teach"), R(11, 13, "N", "LAB. INFORMATICA 1", "teach"),
       R(13, 14, "N", "CENTRAL DE SEGURANCA", "sup"), E3,
       R(0, 2, "S", "RECEPCAO E TRIAGEM DE AMOSTRAS", "sup", wet=1), R(2, 4, "S", "BIORREPOSITORIO A", "crit"),
       R(4, 7, "S", "CENTRAL ANALITICA MULTIUSUARIO", "lab", wet=1), E2, R(8, 10, "S", "LAB. INFORMATICA 2", "teach"),
       R(10, 12, "S", "OFICINA E PROTOTIPAGEM", "lab"), R(12, 14, "S", "ALMOXARIFADO GERAL E DOCA", "sup"), R(14, 15, "S", "TRIAGEM DE RESIDUOS", "sup", wet=1)],
 "1": [E1, R(1, 3, "N", "SALAS DE PESQUISADORES", "off"), R(3, 5, "N", "SALA DE POS-GRADUANDOS", "off"), R(5, 6, "N", "REUNIOES", "off"), SAN,
       R(7, 8, "N", "ESTAR / SHAFTS", "hall"), R(8, 10, "N", "DATA CENTER E BACKUP", "crit"), R(10, 12, "N", "MODELAGEM MOLECULAR", "off"),
       R(12, 14, "N", "SALAS DE PESQUISADORES", "off"), E3,
       R(0, 3, "S", "QUIMICA MEDICINAL E SINTESE", "lab", wet=1), R(3, 5, "S", "FARMACOTECNICA", "lab", wet=1),
       R(5, 7, "S", "CONTROLE DE QUALIDADE", "lab", wet=1), E2, R(8, 10, "S", "CULTURA DE CELULAS NB-2", "lab", wet=1),
       R(10, 12, "S", "FARMACOLOGIA E ENSAIOS", "lab", wet=1), R(12, 13, "S", "LAVAGEM E ESTERILIZACAO", "sup", wet=1),
       R(13, 14, "S", "PESAGEM", "sup"), R(14, 15, "S", "REAGENTES", "crit")],
 "2": [E1, R(1, 3, "N", "SALAS DE PESQUISADORES", "off"), R(3, 5, "N", "SALA DE POS-GRADUANDOS", "off"), R(5, 6, "N", "REUNIOES", "off"), SAN,
       R(7, 8, "N", "ESTAR / SHAFTS", "hall"), R(8, 10, "N", "BIORREPOSITORIO B", "crit"), R(10, 12, "N", "BIOINFORMATICA", "off"),
       R(12, 14, "N", "SALAS DE PESQUISADORES", "off"), E3,
       R(0, 2, "S", "EXTRACAO DE DNA E RNA", "lab", wet=1), R(2, 3, "S", "PRE-PCR", "lab", wet=1), R(3, 4, "S", "PCR", "lab", wet=1),
       R(4, 5, "S", "POS-PCR", "lab", wet=1), R(5, 7, "S", "SEQUENCIAMENTO", "lab", wet=1), E2,
       R(8, 10, "S", "CULTURA DE CELULAS NB-2", "lab", wet=1), R(10, 12, "S", "CITOGENETICA E MICROSCOPIA", "lab", wet=1),
       R(12, 13, "S", "LAVAGEM E ESTERILIZACAO", "sup", wet=1), R(13, 14, "S", "SALA DE FREEZERS", "sup"), R(14, 15, "S", "REAGENTES", "crit")],
}
FLOOR_NAME = {"T": "TERREO", "1": "1o PAVIMENTO", "2": "2o PAVIMENTO"}


def box(r):
    """Faces internas da sala (x0,y0,x1,y1)."""
    x0 = r["b0"] * BAY + (WE if r["b0"] == 0 else WI); x1 = r["b1"] * BAY - (WE if r["b1"] == NB else WI)
    if r["band"] == "N":
        return x0, YB + WI, x1, YA - WE
    return x0, YD + WE, x1, YC - WI


def doors(r):
    """Portas para o corredor: lista (x_inicio, largura)."""
    x0, _, x1, _ = box(r); k = r["kind"]
    if k == "hall": return [(x0 + 0.9, x1 - x0 - 1.8)]
    w = {"lab": 1.10, "crit": 1.10, "teach": 1.60, "stair": 1.00, "san": 0.90}.get(k, 0.90)
    d = [(x0 + 0.8, w)]
    if r["b1"] - r["b0"] >= 3 or k == "teach": d.append((x1 - 0.8 - w, w))
    if k == "san": d.append((x1 - 0.8 - w, w))
    return d


def edge(s, p, q, gaps):
    """Parede horizontal de p a q com vaos [(x, w)]."""
    x = p[0]
    for gx, gw in sorted(gaps):
        if gx > x: s.line((x, p[1]), (gx, p[1]))
        x = gx + gw
    if x < q[0]: s.line((x, p[1]), (q[0], p[1]))


def stair(s, x, y, w=2.6, n=13, t=0.28, up=True):
    """Escada em dois lances, largura total w, n pisos por lance."""
    ln = (n - 1) * t; fw = (w - 0.2) / 2
    s.rect(x, y, w, ln + 2.6, "MOBILIA")
    for i in range(n):
        yy = y + 1.3 + i * t
        s.line((x, yy), (x + fw, yy), "MOBILIA"); s.line((x + fw + 0.2, yy), (x + w, yy), "MOBILIA")
    s.rect(x + fw, y + 1.3, 0.2, ln, "MOBILIA")
    s.text("SOBE", (x + fw / 2, y + 0.65), 1.6, "MOBILIA")


def draw_plan(s, fl, labels=True, dims=True, furniture=True):
    rooms = FLOORS[fl]
    # contorno externo
    s.rect(-WE, -WE, L + 2 * WE, YA + 2 * WE)
    cg_n, cg_s = [], []
    for r in rooms:
        x0, y0, x1, y1 = box(r); ds = doors(r); k = r["kind"]
        s.line((x0, y0), (x0, y1)); s.line((x1, y0), (x1, y1))
        if r["band"] == "N":
            s.line((x0, y1), (x1, y1)); edge(s, (x0, y0), (x1, y0), ds); cg_n += ds; yd, sg = y0, 1
        else:
            s.line((x0, y0), (x1, y0)); edge(s, (x0, y1), (x1, y1), ds); cg_s += ds; yd, sg = y1, -1
        for dx, dw in ds:                                   # folhas
            if k == "hall": continue
            if k == "teach":                                 # abre para fora (mais de 50 pessoas)
                s.line((dx, yd - sg * 2 * WI), (dx, yd - sg * (2 * WI + dw / 2)), "ESQUADRIA"); s.line((dx + dw, yd - sg * 2 * WI), (dx + dw, yd - sg * (2 * WI + dw / 2)), "ESQUADRIA")
            else:
                s.line((dx, yd), (dx, yd + sg * dw), "ESQUADRIA")
                s.arc((dx, yd), dw, 0 if sg > 0 else 270, 90 if sg > 0 else 360, "ESQUADRIA")
        # janelas na fachada
        if k not in ("crit", "stair"):
            yw = YA if r["band"] == "N" else YD
            for b in range(r["b0"], r["b1"]):
                for cx in (b * BAY + 1.8, b * BAY + 5.4):
                    s.rect(cx - 1.2, yw - WE, 2.4, 2 * WE, "ESQUADRIA"); s.line((cx - 1.2, yw), (cx + 1.2, yw), "ESQUADRIA")
        if labels:
            cx, cy = (x0 + x1) / 2, ((y0 + 1.3) if (k == "stair" and r["band"] == "N") else (y1 - 1.6) if k == "stair" else (y0 + y1) / 2)
            s.text(r["name"], (cx, cy + 0.55), 2.0); a = (x1 - x0) * (y1 - y0)
            s.text(f"{a:.1f} m2   {x1 - x0:.2f} x {y1 - y0:.2f}".replace(".", ","), (cx, cy - 0.25), 1.6)
            if k == "crit": s.text("PAREDES E PORTA TRRF 120", (cx, cy - 0.95), 1.6)
        if furniture:
            if k == "stair" and r["band"] == "N":
                stair(s, x0 + 0.3, y1 - 6.2 - 0.3); s.line((x0 + 0.8, YA - WE), (x0 + 1.8, YA - WE), "ESQUADRIA")
                s.text("SAIDA" if fl == "T" else "", (x0 + 4.6, y1 - 0.6), 1.6, "MOBILIA")
            if k == "stair" and r["band"] == "S":
                stair(s, x0 + 0.3, y0 + 0.3)
                for i in range(2):
                    s.rect(x0 + 3.4 + i * 1.75, y0 + 0.3, 1.6, 2.4, "MOBILIA"); s.text("ELEV", (x0 + 4.2 + i * 1.75, y0 + 1.5), 1.5, "MOBILIA")
                s.rect(x0 + 0.9, YD - WE, 1.0, 2 * WE, "ESQUADRIA")
                s.rect(x0 + 3.4, y0 + 3.2, 3.35, 1.4, "MOBILIA"); s.text("SHAFTS ELE / DADOS", (x0 + 5.07, y0 + 3.9), 1.4, "MOBILIA")
            if k == "san":
                xm = (x0 + x1) / 2; s.line((xm, y0 + 1.6), (xm, y1), "PAREDE"); s.line((x0, y0 + 1.6), (x1, y0 + 1.6), "PAREDE")
                for i in range(4):
                    s.rect(x0 + 0.1, y1 - 1.0 - i * 1.0, 0.7, 0.45, "MOBILIA"); s.rect(x1 - 0.8, y1 - 1.0 - i * 1.0, 0.7, 0.45, "MOBILIA")
                for i in range(3):
                    s.circle((xm - 0.45, y0 + 2.4 + i * 0.9), 0.22, "MOBILIA"); s.circle((xm + 0.45, y0 + 2.4 + i * 0.9), 0.22, "MOBILIA")
    # corredor
    if labels:
        s.text("CIRCULACAO  larg. livre 2,25", (BAY * 3.5, (YB + YC) / 2), 1.8); s.level(LEVELS[fl], (BAY * 1.5, (YB + YC) / 2 - 0.5))
    for xj in (7 * BAY, 8 * BAY):                              # portas corta-fogo nas juntas
        s.line((xj, YC + WI), (xj, YC + WI + 0.25)); s.line((xj, YB - WI), (xj, YB - WI - 0.25))
        s.line((xj, YC + 0.35), (xj + 0.85, YC + 0.75), "ESQUADRIA"); s.line((xj, YB - 0.35), (xj + 0.85, YB - 0.75), "ESQUADRIA")
        if labels: s.text("PCF P-90", (xj + 1.3, YC + 0.45), 1.4, "ESQUADRIA", "l")
    s.line((WE, YC + WI), (WE, YB - WI)); s.line((L - WE, YC + WI), (L - WE, YB - WI))
    # acessos no terreo
    if fl == "T" and labels:
        s.text("ACESSO PRINCIPAL", (7.5 * BAY, YA + 1.2), 2.2); s.text("SAIDA E2", (7.5 * BAY, YD - 1.0), 1.8)
    grid(s, dims)


def grid(s, dims=True, pillars=True):
    for i in range(NB + 1):
        x = i * BAY
        s.line((x, -3.0), (x, YA + 5.5), "EIXO"); s.tag(str(i + 1), (x, YA + 6.4), 3.0, "EIXO")
        if pillars:
            for y in (YD - 0.1, YC - 0.7, YB, YA - 0.6): s.solid(x - 0.2, y, 0.4, 0.7)
    for n, y in zip("DCBA", (YD, YC, YB, YA)):
        s.line((-5.5, y), (L + 2.5, y), "EIXO"); s.tag(n, (-6.4, y), 3.0, "EIXO")
    if dims:
        for i in range(NB): s.dim((i * BAY, YA), ((i + 1) * BAY, YA), 2.6)
        s.dim((0, YA), (7 * BAY, YA), 4.3, "BLOCO A  50,40"); s.dim((7 * BAY, YA), (8 * BAY, YA), 4.3, "7,20"); s.dim((8 * BAY, YA), (L, YA), 4.3, "BLOCO B  50,40")
        s.dim((0, YD), (L, YD), -2.6, "108,00")
        for a, b in ((YD, YC), (YC, YB), (YB, YA)): s.dim((0, a), (0, b), -2.6)
        s.dim((0, YD), (0, YA), -4.3, "21,60")
