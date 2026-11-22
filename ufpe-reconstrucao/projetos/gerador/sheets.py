import math, sys
from cad import *
import calc
from render import render

NX, NY = 118.0, 46.0          # canto das notas (pranchas 1:200)
f2 = lambda v, n=2: f"{v:.{n}f}".replace(".", ",")
SHEETS = []


def done(s):
    s.save(); SHEETS.append((s.code, s.title, s.scale)); print(s.code, render(s)); sys.stdout.flush()


def notes(s, title, rows, p=None, mm=2.3):
    x, y = p or (NX, NY)
    s.text(title, (x, y), 3.2, "NOTA", "l")
    return s.lines(rows, (x, y - 8 * s.k), mm)


def areas_table(s, fl, p):
    rows = [["AMBIENTE", "AREA (m2)", "PISO", "FORRO"]]
    tot = 0
    for r in FLOORS[fl]:
        x0, y0, x1, y1 = box(r); a = (x1 - x0) * (y1 - y0); tot += a; k = r["kind"]
        piso = {"lab": "Vinilico em manta, rodape curvo", "crit": "Epoxi autonivelante", "san": "Porcelanato", "stair": "Concreto polido antiderrapante"}.get(k, "Porcelanato / vinilico")
        forro = {"lab": "Removivel lavavel", "crit": "Laje aparente pintada", "stair": "Laje aparente"}.get(k, "Removivel mineral")
        rows.append([r["name"], f2(a, 1), piso, forro])
    cor = (L - 2 * WE) * (YB - YC - 2 * WI); rows.append(["CIRCULACAO", f2(cor, 1), "Vinilico em manta", "Removivel mineral"])
    rows.append(["TOTAL UTIL DO PAVIMENTO", f2(tot + cor, 1), "", ""]); rows.append(["AREA CONSTRUIDA (108,20 x 21,80)", f2(108.2 * 21.8, 1), "", ""])
    s.text(f"QUADRO DE AREAS E ACABAMENTOS - {FLOOR_NAME[fl]}", (p[0], p[1] + 1.2), 2.8, "NOTA", "l")
    return s.table(rows, p, [70, 22, 56, 42])


ARQ_NOTES = ["1. Cotas em metros, tomadas de eixo a eixo. Niveis em metros sobre o terreno (0,00).",
             "2. Modulacao estrutural 7,20 x (9,60 + 2,40 + 9,60) m.",
             "3. Paredes externas 20 cm (bloco + revestimento); internas 15 cm.",
             "   Entre laboratorios: alvenaria ou drywall duplo ate a laje.",
             "4. Salas criticas (TRRF 120): alvenaria de bloco de concreto",
             "   19 cm ate a laje, porta corta-fogo P-120, sem janelas.",
             "5. Juntas de dilatacao nos eixos 8 e 9, com portas corta-fogo",
             "   P-90 no corredor, mantidas abertas por eletroima.",
             "6. Escadas E1, E2 e E3 enclausuradas, com porta P-90.",
             "7. Pe-direito livre 3,20 m; piso a piso 4,50 m.",
             "8. Janelas: 2 por modulo, 2,40 x 1,50 m, peitoril 1,10 m,",
             "   aluminio e vidro laminado. Fachada norte com brises.",
             "9. Portas: salas 0,90 m; laboratorios 1,10 m; auditorio e",
             "   informatica 1,60 m (2 folhas, abrindo para a saida).",
             "10. Acessibilidade conforme NBR 9050: rampa i = 8,33 % no",
             "   acesso principal, sanitario acessivel por pavimento.",
             "11. Areas indicadas sao areas uteis entre faces de parede."]


def arq_plan(code, fl):
    s = Sheet(code, f"Arquitetura - planta do {FLOOR_NAME[fl].lower()}")
    draw_plan(s, fl)
    s.text(f"PLANTA DO {FLOOR_NAME[fl]}   nivel +{f2(LEVELS[fl])}   escala 1:200", (0, -7.5), 3.5, "NOTA", "l")
    areas_table(s, fl, (0, -12))
    notes(s, "NOTAS", ARQ_NOTES)
    # corte markers
    for x in (3.5 * BAY,):
        s.line((x, YA + 8.5), (x, YA + 7.3), "TEXTO"); s.line((x, -3.2), (x, -4.4), "TEXTO"); s.text("A", (x + 0.8, YA + 8), 3, "TEXTO"); s.text("A", (x + 0.8, -3.8), 3, "TEXTO")
    s.text("B", (-9, 4.8), 3); s.text("B", (L + 4.2, 4.8), 3); s.line((-8, 4.8), (-7, 4.8)); s.line((L + 2.8, 4.8), (L + 3.6, 4.8))
    done(s)


def roof_base(s, labels=True):
    s.rect(-WE, -WE, L + 2 * WE, YA + 2 * WE); s.rect(0.3, 0.3, L - 0.6, YA - 0.6, "MOBILIA")       # platibanda
    for xj in (7 * BAY, 8 * BAY): s.line((xj, 0), (xj, YA), "EIXO")
    s.rect(7 * BAY + 0.3, 0.6, BAY - 0.6, 8.6); s.rect(7 * BAY + 0.6, 1.0, 2.9, 4.0, "MOBILIA"); s.rect(7 * BAY + 3.7, 1.0, 2.9, 4.0, "MOBILIA")
    s.rect(2 * BAY, 1.2, 4.5 * BAY, 7.6, "MOBILIA"); s.rect(8.5 * BAY, 1.2, 4.5 * BAY, 7.6, "MOBILIA")   # casas de maquinas
    for i in list(range(0, 7)) + list(range(8, 15)):                                                       # fotovoltaico
        s.rect(i * BAY + 0.6, 13.0, BAY - 1.2, 3.4, "ESQUADRIA"); s.rect(i * BAY + 0.6, 17.0, BAY - 1.2, 3.4, "ESQUADRIA")
    if labels:
        s.text("RESERV. SUPERIOR 2 x 12 m3", (7.5 * BAY, 6.2), 1.7); s.text("+ casa de maquinas dos elevadores", (7.5 * BAY, 5.5), 1.5)
        s.text("CASA DE MAQUINAS A - climatizacao e exaustao", (4.25 * BAY, 5), 2.0); s.text("CASA DE MAQUINAS B - climatizacao e exaustao", (10.75 * BAY, 5), 2.0)
        s.text("PAINEIS FOTOVOLTAICOS (aprox. 200 kWp)", (3.5 * BAY, 16.7), 2.0); s.text("PAINEIS FOTOVOLTAICOS", (11.5 * BAY, 16.7), 2.0)
        s.text("LAJE IMPERMEABILIZADA  i = 2 %", (1 * BAY, 10.8), 1.8); s.level(LEVELS["C"], (0.6 * BAY, 10.2))
    grid(s, True, False)


def arq_roof():
    s = Sheet("ARQ-05", "Arquitetura - planta de cobertura"); roof_base(s)
    s.text("PLANTA DE COBERTURA   nivel +14,70   escala 1:200", (0, -7.5), 3.5, "NOTA", "l")
    notes(s, "NOTAS", ["1. Cobertura em laje impermeabilizada com protecao mecanica,", "   caimento de 2 % para calhas junto as duas platibandas longas.",
                       "2. Platibanda h = 1,10 m (guarda-corpo de manutencao).", "3. Casas de maquinas com fechamento em veneziana acustica,",
                       "   h = 3,00 m; acesso pela escada E2.", "4. Chamines de exaustao das capelas com descarga a 3,0 m",
                       "   acima da laje, afastadas das tomadas de ar externo.", "5. Reservatorio superior sobre o nucleo: fundo em +16,20.",
                       "6. Paineis fotovoltaicos sobre a faixa norte, com corredores", "   de manutencao de 1,20 m.", "7. SPDA: malha captora e descidas conforme NBR 5419."])
    done(s)


# ---------------- cortes e fachadas ----------------
ZS = [1.20, 5.70, 10.20, 14.70]


def corte_transv(s, ox, oy, lab=True):
    P = lambda y, z: (ox + y, oy + z)
    s.line(P(-8, 0), P(30, 0)); s.text("0,00", P(-6, 0.5), 2)
    for y in (YD, YC, YB, YA):
        w = 0.7; y0 = {YD: -0.1, YC: YC - 0.7, YB: YB, YA: YA - 0.6}[y]
        s.solid(ox + y0, oy + 0, w, 14.7, "PILAR"); s.rect(ox + y0 - 0.5, oy - 1.2, w + 1.0, 1.2); s.line(P(y0 + 0.35, -1.2), P(y0 + 0.35, -5.0), "EIXO")
    for z in ZS:
        s.solid(ox - 0.3, oy + z - 0.35, YA + 0.6, 0.35, "PILAR"); s.level(z, P(YA + 2.5, z))
        if z < 14: s.line(P(0.2, z + 3.2), P(YA - 0.2, z + 3.2), "ESQUADRIA")
    for z in ZS[:3]:
        for y in (YC, YB): s.line(P(y, z), P(y, z + 3.2))
        for y, sg in ((YD, -1), (YA, 1)):                       # fachadas: peitoril + janela
            s.rect(ox + (y - 0.1 if sg < 0 else y - 0.1), oy + z, 0.2, 1.1); s.line(P(y, z + 1.1), P(y, z + 2.6), "ESQUADRIA"); s.rect(ox + y - 0.1, oy + z + 2.6, 0.2, 1.55)
        for k_ in range(6): s.line(P(YA + 0.4, z + 1.2 + k_ * 0.28), P(YA + 1.1, z + 1.32 + k_ * 0.28), "MOBILIA")   # brises norte
        if lab:
            s.text("LABORATORIO", P(4.8, z + 1.6), 2); s.text("CIRC.", P(10.8, z + 1.6), 1.6); s.text("PERMANENCIA", P(16.8, z + 1.6), 2)
            s.text("entreforro 0,95", P(4.8, z + 3.65), 1.5)
    s.rect(ox - 0.1, oy + 14.7, 0.2, 1.1); s.rect(ox + YA - 0.1, oy + 14.7, 0.2, 1.1)                 # platibanda
    s.rect(ox + 1.2, oy + 14.7, 7.6, 3.0, "MOBILIA"); s.rect(ox + 2.0, oy + 17.7, 0.5, 1.5, "MOBILIA")
    s.line(P(13, 15.3), P(16.4, 15.9), "ESQUADRIA"); s.line(P(17, 15.3), P(20.4, 15.9), "ESQUADRIA")
    if lab:
        s.text("CASA DE MAQUINAS", P(5, 16.2), 1.8); s.text("fotovoltaico", P(16.8, 16.6), 1.6); s.text("S", P(-2.5, 16), 3); s.text("N", P(YA + 2.5, 16.5), 3)
        s.text("estacas helice continua (prof. conforme sondagem)", P(10.8, -5.8), 1.8)
    s.dim(P(YD, -2.2), P(YC, -2.2), -1.2); s.dim(P(YC, -2.2), P(YB, -2.2), -1.2); s.dim(P(YB, -2.2), P(YA, -2.2), -1.2)
    for a, b in zip([0] + ZS, ZS): s.dim(P(-3.5, a), P(-3.5, b), -1.0)
    s.dim(P(-3.5, 14.7), P(-3.5, 17.7), -1.0)


def corte_long(s, ox, oy):
    P = lambda x, z: (ox + x, oy + z)
    s.line(P(-6, 0), P(L + 6, 0));
    for i in range(NB + 1):
        s.solid(ox + i * BAY - 0.2, oy, 0.4, 14.7, "PILAR"); s.rect(ox + i * BAY - 0.7, oy - 1.2, 1.4, 1.2); s.tag(str(i + 1), P(i * BAY, 21.5), 3.0, "EIXO"); s.line(P(i * BAY, 14.7), P(i * BAY, 20.5), "EIXO")
    for z in ZS:
        s.solid(ox - 0.3, oy + z - 0.35, L + 0.6, 0.35, "PILAR"); s.level(z, P(L + 3, z))
        if z < 14: s.line(P(0.2, z + 3.2), P(L - 0.2, z + 3.2), "ESQUADRIA")
    for fl, z in zip("T12", ZS):                                   # divisorias da faixa sul
        for r in FLOORS[fl]:
            if r["band"] == "S":
                s.line(P(r["b1"] * BAY, z), P(r["b1"] * BAY, z + 3.2)); s.text(r["name"], P((r["b0"] + r["b1"]) / 2 * BAY, z + 1.7), 1.6)
    for xj in (7 * BAY, 8 * BAY): s.line(P(xj + 0.25, 0), P(xj + 0.25, 15.8), "EIXO")
    s.rect(ox + 7 * BAY + 0.3, oy + 14.7, BAY - 0.6, 4.6); s.text("RESERV. SUP.", P(7.5 * BAY, 18.2), 1.6); s.text("fundo +16,20", P(7.5 * BAY, 17.4), 1.4)
    s.rect(ox + 2 * BAY, oy + 14.7, 4.5 * BAY, 3.0, "MOBILIA"); s.rect(ox + 8.5 * BAY, oy + 14.7, 4.5 * BAY, 3.0, "MOBILIA")
    s.text("CASA DE MAQUINAS A", P(4.25 * BAY, 16.2), 1.8); s.text("CASA DE MAQUINAS B", P(10.75 * BAY, 16.2), 1.8)
    for x in (3 * BAY, 11 * BAY): s.rect(ox + x - 0.3, oy + 17.7, 0.6, 1.6, "MOBILIA")
    s.rect(ox - 0.1, oy + 14.7, 0.2, 1.1); s.rect(ox + L - 0.1, oy + 14.7, 0.2, 1.1)
    for i in range(NB): s.dim(P(i * BAY, -1.8), P((i + 1) * BAY, -1.8), -1.2)
    s.dim(P(0, -1.8), P(L, -1.8), -3.0, "108,00")
    for a, b in zip([0] + ZS, ZS): s.dim(P(-3.5, a), P(-3.5, b), -1.0)


def cortes():
    s = Sheet("ARQ-06", "Arquitetura - cortes AA e BB")
    corte_long(s, 0, -2); s.text("CORTE BB - LONGITUDINAL PELA FAIXA SUL   escala 1:200", (0, -9.5), 3.5, "NOTA", "l")
    corte_transv(s, 6, -44); s.text("CORTE AA - TRANSVERSAL PELO EIXO 4-5   escala 1:200", (0, -53.5), 3.5, "NOTA", "l")
    notes(s, "NOTAS", ["1. Terreo elevado 1,20 m sobre o terreno (cota de", "   protecao contra alagamento, a confirmar com topografia).",
                       "2. Piso a piso 4,50 m = 3,20 livre + 0,95 de entreforro", "   tecnico + 0,35 de laje nervurada.",
                       "3. Altura do piso mais alto ate a saida: 9,00 m.", "4. Altura total ate o topo das casas de maquinas: 17,70 m.",
                       "5. Juntas de dilatacao com pilares duplos nos eixos 8 e 9."], (60, -20))
    done(s)


def fachada(s, ox, oy, norte):
    P = lambda x, z: (ox + x, oy + z)
    s.line(P(-6, 0), P(L + 6, 0)); s.rect(ox - 0.1, oy + 0, L + 0.2, 15.8)
    for z in ZS: s.line(P(0, z - 0.35), P(L, z - 0.35), "MOBILIA")
    for fl, z in zip("T12", ZS):
        for r in FLOORS[fl]:
            if r["band"] != ("N" if norte else "S"): continue
            for b in range(r["b0"], r["b1"]):
                xb = (NB - 1 - b) * BAY if norte else b * BAY
                if r["kind"] in ("crit", "stair"):
                    s.rect(ox + xb + 0.6, oy + z + 0.3, BAY - 1.2, 3.2, "MOBILIA")
                    if r["kind"] == "stair": s.rect(ox + xb + 2.9, oy + z + 1.1, 1.4, 1.5, "ESQUADRIA")
                    continue
                for cx in (1.8, 5.4):
                    s.rect(ox + xb + cx - 1.2, oy + z + 1.1, 2.4, 1.5, "ESQUADRIA")
                    if norte:
                        for k_ in range(6): s.line(P(xb + cx - 1.5, z + 1.15 + k_ * 0.28), P(xb + cx + 1.5, z + 1.15 + k_ * 0.28), "MOBILIA")
    xh = 7 * BAY
    if norte: s.rect(ox + xh + 1.8, oy + 1.2, 3.6, 2.6, "ESQUADRIA"); s.text("ACESSO", P(xh + 3.6, 0.6), 1.8); s.line(P(xh - 6, 0), P(xh + 1.8, 1.2), "MOBILIA")
    s.rect(ox + 7 * BAY + 0.3, oy + 15.8, BAY - 0.6, 3.5); s.rect(ox + 2 * BAY if not norte else ox + 8.5 * BAY, oy + 15.8, 4.5 * BAY, 1.9, "MOBILIA"); s.rect(ox + 8.5 * BAY if not norte else ox + 2 * BAY, oy + 15.8, 4.5 * BAY, 1.9, "MOBILIA")
    for z in ZS: s.level(z, P(L + 3, z))
    s.level(15.8, P(L + 3, 15.8))


def fachadas():
    s = Sheet("ARQ-07", "Arquitetura - fachadas norte e sul")
    fachada(s, 0, 0, True); s.text("FACHADA NORTE (principal) - brises horizontais de aluminio   escala 1:200", (0, -4), 3.5, "NOTA", "l")
    fachada(s, 0, -40, False); s.text("FACHADA SUL - laboratorios   escala 1:200", (0, -44), 3.5, "NOTA", "l")
    notes(s, "NOTAS", ["1. Estrutura de concreto aparente tratado nos pilares e", "   testeiras de laje.", "2. Fechamentos em alvenaria com revestimento ceramico",
                       "   ou pintura acrilica sobre massa, cores a definir.", "3. Brises horizontais fixos na fachada norte, calculados",
                       "   para sombrear as janelas das 9h as 15h.", "4. Paineis cegos nas salas criticas e caixas de escada.",
                       "5. Empenas leste e oeste cegas, com isolamento termico."], (NX, 40))
    done(s)


def implantacao():
    s = Sheet("ARQ-01", "Arquitetura - implantacao esquematica", 500, (150, 250))
    s.rect(-30, -34, 198, 92, "MOBILIA"); s.rect(-24, -28, 186, 80, "MOBILIA")
    s.text("ANEL VIARIO PARA VIATURAS - largura 6,00 m - raio interno minimo 9 m", (60, 55), 2.2)
    s.rect(-WE, -WE, L + 2 * WE, YA + 2 * WE); s.line((7 * BAY, 0), (7 * BAY, YA), "EIXO"); s.line((8 * BAY, 0), (8 * BAY, YA), "EIXO")
    s.text("BLOCO A", (3.5 * BAY, 10.8), 3); s.text("BLOCO B", (11.5 * BAY, 10.8), 3); s.text("3 pav. + cobertura tecnica", (3.5 * BAY, 7), 2); s.text("piso terreo +1,20", (11.5 * BAY, 7), 2)
    ax, ay = 123.0, 2.0
    s.rect(ax, ay, 18, 14)
    for i, n in enumerate(("SUBESTACAO", "GERADOR", "GASES", "QUIMICOS")):
        s.rect(ax + i * 4.5, ay, 4.5, 14); s.text(n, (ax + i * 4.5 + 2.25, ay + 7), 1.6, rot=90)
    s.text("ANEXO TECNICO 18,00 x 14,00", (ax + 9, ay - 2), 2)
    s.rect(ax, 22, 18, 9); s.line((ax + 5, 22), (ax + 5, 31)); s.line((ax + 14, 22), (ax + 14, 31))
    s.text("1", (ax + 2.5, 26.5), 2); s.text("2", (ax + 9.5, 26.5), 2); s.text("3", (ax + 16, 26.5), 2); s.text("1 CISTERNA 36 m3 - 2 RESERVA DE INCENDIO 130 m3 - 3 BOMBAS", (ax + 9, 33.5), 1.8)
    s.dim((L, -2), (ax, -2), -3, "15,00"); s.dim((0, 0), (L, 0), -8, "108,00"); s.dim((0, 0), (0, YA), -8, "21,60")
    s.circle((54, 40), 4, "ESQUADRIA"); s.text("PONTO DE ENCONTRO", (54, 46), 2.2)
    s.text("ACESSO PRINCIPAL", (54, 26), 2.4); s.line((54, 24.5), (54, 22), "TEXTO")
    s.rect(52.5, -16, 3, 3, "INC"); s.text("HIDRANTE DE RECALQUE", (54, -19), 2, "INC")
    s.line((150, 40), (150, 50), "TEXTO"); s.text("N", (150, 52), 4)
    notes(s, "NOTAS", ["1. Implantacao ESQUEMATICA. Nao houve levantamento topografico nem cadastral;",
                       "   posicao, orientacao e afastamentos devem ser ajustados ao terreno real.",
                       "2. Eixo longitudinal do predio no sentido leste-oeste; fachadas longas norte e sul.",
                       "3. Anexo tecnico terreo, afastado no minimo 15 m do predio, com paredes TRRF 120",
                       "   entre compartimentos e cobertura leve.",
                       "4. Reservatorio inferior e reserva tecnica de incendio semienterrados, com casa de bombas.",
                       "5. Via perimetral para viaturas do Corpo de Bombeiros em todo o contorno.",
                       "6. Arvores existentes e redes do campus a cadastrar antes do projeto executivo."], (-30, -45), 2.3)
    s.text("IMPLANTACAO   escala 1:500", (-30, -40), 3.5, "NOTA", "l")
    done(s)


# ---------------- estrutura ----------------
def estrutura():
    s = Sheet("EST-01", "Estrutura - pilares e forma do pavimento-tipo"); e = calc.estrutura()
    s.rect(-0.3, -0.3, L + 0.6, YA + 0.6, "EST")
    for y in (YD, YC, YB, YA):
        s.line((0, y - 0.6), (L, y - 0.6), "EST"); s.line((0, y + 0.6), (L, y + 0.6), "EST")
    for i in range(NB + 1):
        x = i * BAY; s.line((x - 0.2, 0), (x - 0.2, YA), "EST"); s.line((x + 0.2, 0), (x + 0.2, YA), "EST")
        for j, y in enumerate((YD - 0.1, YC - 0.7, YB, YA - 0.6)):
            s.text(f"P{j * 16 + i + 1}", (x + 1.0, y + 0.35 + (0.9 if j in (0, 2) else -0.9)), 1.6, "EST")
    for i in range(NB):
        for yc in (4.8, 16.8): s.text("LN h=35", (i * BAY + 3.6, yc), 1.8, "EST")
    for xj in (7 * BAY, 8 * BAY): s.line((xj + 0.3, -2), (xj + 0.3, YA + 2), "INC"); s.text("JUNTA", (xj + 0.3, -2.6), 1.8, "INC")
    grid(s, True, True)
    s.text("FORMA DO PAVIMENTO-TIPO E LOCACAO DE PILARES   escala 1:200", (0, -7.5), 3.5, "NOTA", "l")
    s.table([["ELEMENTO", "PRE-DIMENSIONAMENTO", "OBSERVACAO"],
             ["Pilares P1 a P64", "40 x 70 cm", "Duplos nas juntas (eixos 8 e 9)"],
             ["Lajes", "Nervurada bidirecional h = 35 cm (capa 7 cm)", "Cubetas 80 x 80 cm"],
             ["Vigas-faixa longitudinais", "120 x 35 cm nos eixos A, B, C, D", "Embutidas na altura da laje"],
             ["Vigas transversais", "40 x 60 cm nos eixos 1 a 16", "Vao maximo 9,60 m"],
             ["Concreto / aco", "fck 35 MPa / CA-50", "Classe de agressividade III"],
             ["Cobrimentos", "Pilares e vigas 40 mm; lajes 35 mm", "NBR 6118"],
             ["Carga permanente adotada", f"{f2(e['g'], 1)} kN/m2 (laje + revestimento + divisorias)", ""],
             ["Sobrecarga", f"{f2(e['q'], 1)} kN/m2 (7,5 nas salas criticas)", "NBR 6120"],
             ["Pilar interno: area de influencia", f"{f2(e['ai'], 1)} m2 x 4 lajes -> N = {e['ni']:.0f} kN (servico)", f"Nd = {e['nid']:.0f} kN < 0,85 fcd Ac = {e['nrd']:.0f} kN"],
             ["Pilar de fachada", f"{f2(e['ae'], 1)} m2 x 4 lajes -> N = {e['ne']:.0f} kN (servico)", ""],
             ["Fundacoes", "Blocos sobre 2 estacas helice continua D60 (internos) e D50 (fachada)", "A confirmar com 12 furos SPT"]],
            (0, -12), [62, 110, 80])
    notes(s, "NOTAS", ["1. Pre-dimensionamento para estudo de viabilidade.", "   O calculo estrutural completo (esforcos, flechas,",
                       "   vento, estabilidade global, incendio) cabe ao", "   projetista estrutural.", "2. Vento: V0 = 30 m/s (NBR 6123).",
                       "3. Resistencia ao fogo: 90 min na estrutura;", "   120 min nas escadas e salas criticas", "   (NBR 14432 e NBR 15200).",
                       "4. Verificar vibracao da laje na central", "   analitica (equipamentos sensiveis).", "5. Contrapiso do terreo: laje estruturada",
                       "   sobre vigas baldrame, vao ventilado de", "   1,20 m para instalacoes."])
    done(s)


# ---------------- hidraulica ----------------
COL_AF = {"AF-1": (6 * BAY + 3.6, YB + 1.0), "AF-2": (3 * BAY, YC - 0.5), "AF-3": (11 * BAY, YC - 0.5)}
COL_ES = {"TQ-1": (6 * BAY + 3.6, YA - 0.6), "EL-A": (3 * BAY - 0.8, YC - 0.5), "EL-B": (11 * BAY - 0.8, YC - 0.5)}


def wet_points(fl):
    pts = []
    for r in FLOORS[fl]:
        if r.get("wet"):
            for b in range(r["b0"], r["b1"]): pts += [(b * BAY + 1.8, 0.5), (b * BAY + 5.4, 0.5)]
    return pts


def showers(fl):
    return [(box(r)[0] + 2.6, YC - 0.7) for r in FLOORS[fl] if r.get("wet") and r["kind"] == "lab"]


def hid_af():
    s = Sheet("HID-01", "Hidraulica - agua fria e esquema vertical", base=True); fl = "2"; a = calc.agua()
    draw_plan(s, fl, True, False)
    for blk, col in (("A", "AF-2"), ("B", "AF-3")):
        xs = [p[0] for p in wet_points(fl) if (p[0] < 7 * BAY) == (blk == "A")]; cx, cy = COL_AF[col]
        if xs:
            s.line((min(xs), cy), (max(max(xs), cx), cy), "HID_AF")
            for x in xs: s.line((x, cy), (x, 0.9), "HID_AF"); s.rect(x - 0.3, 0.3, 0.6, 0.5, "HID_AF")
    for x, y in showers(fl): s.circle((x, y), 0.3, "HID_AP"); s.text("CE", (x + 0.8, y), 1.5, "HID_AP")
    x1, y1 = COL_AF["AF-1"]; s.line((x1 - 3, y1), (x1 + 3, y1), "HID_AF"); s.line((x1 - 3, y1), (x1 - 3, YA - 1), "HID_AF"); s.line((x1 + 3, y1), (x1 + 3, YA - 1), "HID_AF")
    for n, p in COL_AF.items(): s.circle(p, 0.35, "HID_AF"); s.text(n, (p[0], p[1] + 1.0), 2.2, "HID_AF")
    s.text("AGUA FRIA - 2o PAVIMENTO (os demais seguem o mesmo tracado)   escala 1:200", (0, -7.5), 3.5, "NOTA", "l")
    # esquema vertical
    ox, oy = 4, -58
    s.text("ESQUEMA VERTICAL - sem escala", (ox, oy + 43), 3, "NOTA", "l")
    s.rect(ox + 20, oy + 34, 14, 5, "HID_AF"); s.line((ox + 27, oy + 34), (ox + 27, oy + 39), "HID_AF"); s.text("RESERVATORIO SUPERIOR 2 x 12 m3 - fundo +16,20", (ox + 27, oy + 40.5), 2, "HID_AF")
    s.line((ox + 4, oy + 31), (ox + 58, oy + 31), "HID_AF"); s.line((ox + 27, oy + 34), (ox + 27, oy + 31), "HID_AF"); s.text("BARRILETE", (ox + 46, oy + 32.2), 2, "HID_AF")
    for (k, p, q, de, v), x in zip(a["rows"], (10, 30, 50)):
        s.line((ox + x, oy + 31), (ox + x, oy + 4), "HID_AF"); s.text(k.split(" ")[0], (ox + x, oy + 2.5), 2.4, "HID_AF"); s.text(f"DE {de} mm", (ox + x + 3.2, oy + 28), 1.8, "HID_AF")
        for z, n in ((22, "2o PAV +10,20"), (14, "1o PAV +5,70"), (6, "TERREO +1,20")):
            s.line((ox + x, oy + z), (ox + x + 6, oy + z), "HID_AF"); s.circle((ox + x + 1.5, oy + z), 0.4, "HID_AF")
            if x == 10: s.text(n, (ox - 2, oy + z), 1.8, "NOTA", "l"); s.line((ox + 4, oy + z - 2), (ox + 60, oy + z - 2), "COTA")
    s.line((ox + 66, oy + 2), (ox + 66, oy + 38), "HID_AP"); s.line((ox + 66, oy + 38), (ox + 34, oy + 38), "HID_AP"); s.rect(ox + 62, oy - 3, 10, 5, "HID_AP")
    s.text("CISTERNA 36 m3 + 2 BOMBAS", (ox + 67, oy - 4.5), 1.8, "HID_AP"); s.text("RECALQUE DE 40 mm", (ox + 67.8, oy + 20), 1.8, "HID_AP", rot=90)
    rows = [["TRECHO", "SOMA DE PESOS", "VAZAO (L/s)", "TUBO PVC (DE mm)", "VELOC. (m/s)"]] + [[k, f2(p, 1), f2(q), str(de), f2(v)] for k, p, q, de, v in a["rows"]]
    s.text("DIMENSIONAMENTO PRELIMINAR - metodo dos pesos, Q = 0,3 x raiz(soma P)", (84, -15), 2.8, "NOTA", "l"); s.table(rows, (84, -17), [70, 28, 24, 32, 26])
    s.table([["CONSUMO E RESERVACAO", ""], ["Populacao de calculo", f"{a['pop']} pessoas"], ["Consumo diario", f"{a['pop']} x 50 L + 10 m3 de processo = {f2(a['cons'], 0)} m3/dia"],
             ["Reserva (1,5 dia)", f"{f2(a['res'], 0)} m3 = {a['inf']} m3 inferior + {a['sup']} m3 superior"], ["Pressao estatica minima (2o pav.)", "16,20 - 11,30 = 4,9 mca (> 1,0 mca)"],
             ["Chuveiros de emergencia", "Rede propria pressurizada: 76 L/min a 2 bar por ponto"]], (84, -38), [60, 120])
    notes(s, "LEGENDA E NOTAS", ["AF-n  coluna de agua fria", "CE    chuveiro e lava-olhos de emergencia", "[ ]   pia de bancada (2 por modulo)",
                                 "", "1. Tubos e conexoes de PVC soldavel (NBR 5648);", "   distribuicao pelo entreforro, descidas embutidas.",
                                 "2. Registro de gaveta por laboratorio e por", "   sanitario, em altura acessivel.", "3. Agua purificada (osmose reversa) em anel",
                                 "   proprio de PP, com central por bloco.", "4. Hidrometro geral e medicao por bloco.", "5. Dimensionamento conforme NBR 5626, a refazer",
                                 "   com o layout definitivo de bancadas."])
    done(s)


def hid_es():
    s = Sheet("HID-02", "Hidraulica - esgoto - terreo e rede externa", base=True); e = calc.esgoto()
    draw_plan(s, "T", True, False)
    yn, ys, xe = YA + 3.0, -3.0, L + 4.0
    cis_n = [COL_ES["TQ-1"][0], 68.0, 90.0, xe]; cis_s = [COL_ES["EL-A"][0], 45.0, 68.0, COL_ES["EL-B"][0], xe]
    s.line((cis_n[0], yn), (xe, yn), "HID_ES"); s.line((cis_s[0], ys), (xe, ys), "HID_EL"); s.line((xe, ys), (xe, yn), "HID_ES")
    for i, x in enumerate(cis_n): s.rect(x - 0.4, yn - 0.4, 0.8, 0.8, "HID_ES"); s.text(f"CI-{i + 1}", (x, yn + 1.1), 1.8, "HID_ES")
    for i, x in enumerate(cis_s): s.rect(x - 0.4, ys - 0.4, 0.8, 0.8, "HID_EL"); s.text(f"CL-{i + 1}", (x, ys - 1.1), 1.8, "HID_EL")
    s.line(COL_ES["TQ-1"], (COL_ES["TQ-1"][0], yn), "HID_ES")
    for k in ("EL-A", "EL-B"):
        x, y = COL_ES[k]; s.line((x, y), (x, ys), "HID_EL"); s.rect(x - 1.0, ys + 0.8, 2.0, 1.2, "HID_EL"); s.text("TN 2 m3", (x + 2.6, ys + 1.4), 1.6, "HID_EL")
    for n, p in COL_ES.items(): s.circle(p, 0.35, "HID_ES" if n.startswith("TQ") else "HID_EL"); s.text(n, (p[0] + 1.3, p[1] + 0.6), 2.0, "HID_ES" if n.startswith("TQ") else "HID_EL")
    for x, y in wet_points("T"):
        s.rect(x - 0.3, 0.3, 0.6, 0.5, "HID_EL"); s.line((x, 0.3), (x, ys), "HID_EL")
    s.circle((xe + 3, yn), 0.8, "HID_ES"); s.line((xe, yn), (xe + 8, yn), "HID_ES"); s.text("PV - LIGACAO A REDE DO CAMPUS (a cadastrar)", (xe + 3, yn + 1.8), 1.8, "HID_ES")
    s.text("DN 150  i = 1 %", (80, yn - 0.9), 1.8, "HID_ES"); s.text("DN 150  i = 1 %   esgoto de laboratorio apos neutralizacao", (40, ys + 0.9), 1.8, "HID_EL")
    s.text("ESGOTO - TERREO E REDE EXTERNA   escala 1:200", (0, -9.5), 3.5, "NOTA", "l")
    s.table([["ELEMENTO", "CONTRIBUICAO (UHC)", "DIAMETRO", "OBSERVACAO"],
             ["Sanitarios, por pavimento", str(e["san"]), "Ramal DN 100", "8 bacias, 6 lavatorios, 2 mictorios, 1 tanque"],
             ["TQ-1 (tubo de queda sanitario)", str(e["tq1"]), "DN 100 + ventilacao DN 75", "1o e 2o pav.; terreo liga direto na CI-1"],
             ["EL-A (laboratorios bloco A)", str(e["elA"]), "DN 100 em PP", "Efluente quimico, segue ao tanque de neutralizacao"],
             ["EL-B (laboratorios bloco B)", str(e["elB"]), "DN 100 em PP", "Idem"],
             ["Subcoletores externos", str(e["san"] * 3 + e["elA"] + e["elB"]), "DN 150, i = 1 %", "Caixas de inspecao a cada 25 m no maximo"]], (0, -14), [62, 34, 48, 100])
    notes(s, "LEGENDA E NOTAS", ["TQ   tubo de queda de esgoto sanitario", "EL   coluna de esgoto de laboratorio", "CI   caixa de inspecao (sanitario)",
                                 "CL   caixa de inspecao (laboratorio)", "TN   tanque de neutralizacao com medicao de pH", "",
                                 "1. Sistema separador: o esgoto de laboratorio", "   nao se mistura ao sanitario antes do", "   tanque de neutralizacao.",
                                 "2. Tubos de PVC serie reforcada (sanitario) e", "   polipropileno (laboratorio).", "3. Ralos sifonados nas salas de lavagem e",
                                 "   sob os chuveiros de emergencia.", "4. Residuos quimicos concentrados NAO vao a", "   rede: coleta em bombonas e destinacao",
                                 "   por empresa licenciada.", "5. Dimensionamento conforme NBR 8160.", "6. Ponto de ligacao e cotas da rede do", "   campus a levantar."])
    done(s)


def hid_ap():
    s = Sheet("HID-03", "Hidraulica - aguas pluviais e barrilete", base=True); p = calc.pluvial()
    roof_base(s)
    s.line((0.6, 0.6), (L - 0.6, 0.6), "HID_AP"); s.line((0.6, YA - 0.6), (L - 0.6, YA - 0.6), "HID_AP")
    n = 0
    for i in range(1, NB + 1, 2):
        for y in (0.6, YA - 0.6):
            n += 1; s.circle((i * BAY, y), 0.4, "HID_AP"); s.text(f"AP-{n}", (i * BAY, y + (1.2 if y < 5 else -1.2)), 1.7, "HID_AP")
    for x in (10, 40, 70, 100):
        s.line((x, 9.6), (x, 2.0), "HID_AP"); s.line((x, 12), (x, YA - 2), "HID_AP"); s.text("2 %", (x + 1.2, 11), 1.6, "HID_AP")
    bx, by = 7.5 * BAY, 9.6
    s.line((COL_AF["AF-2"][0], by), (COL_AF["AF-3"][0], by), "HID_AF"); s.line((bx, 8.8), (bx, by), "HID_AF"); s.line((COL_AF["AF-1"][0], by), (COL_AF["AF-1"][0], COL_AF["AF-1"][1]), "HID_AF")
    for k, pt in COL_AF.items(): s.circle(pt if k == "AF-1" else (pt[0], by), 0.35, "HID_AF"); s.text(k, (pt[0], (pt[1] if k == "AF-1" else by) + 1.0), 2, "HID_AF")
    s.text("BARRILETE DE 50 mm sob a laje de cobertura", (bx + 14, by + 0.8), 1.8, "HID_AF")
    s.text("AGUAS PLUVIAIS E BARRILETE - COBERTURA   escala 1:200", (0, -7.5), 3.5, "NOTA", "l")
    s.table([["PARAMETRO", "VALOR"], ["Area de contribuicao", f"{f2(calc.AREA_FLOOR, 0)} m2"], ["Intensidade de chuva adotada", f"{p['i']:.0f} mm/h (conferir tabela da NBR 10844 para Recife)"],
             ["Vazao de projeto Q = i x A / 60", f"{p['q']:.0f} L/min"], ["Condutores verticais", f"{p['n']} x DN 150 (um a cada dois vaos, nas duas fachadas)"],
             ["Area e vazao por condutor", f"{f2(p['a1'], 0)} m2  -  {p['q1']:.0f} L/min"], ["Calhas", "Concreto impermeabilizado 40 x 25 cm, i = 0,5 %"],
             ["Destino", "Caixas de areia -> reservatorio de reuso de 30 m3 -> excedente a drenagem do campus"]], (0, -12), [70, 150])
    notes(s, "NOTAS", ["1. Calhas com extravasores (buzinotes) a cada", "   condutor, 5 cm acima do fundo.", "2. Condutores de PVC serie R, embutidos em",
                       "   shafts externos junto aos pilares de fachada.", "3. Agua de chuva e de condensado da climatizacao", "   reaproveitadas em bacias e irrigacao,",
                       "   em rede identificada (nao potavel).", "4. Dimensionamento conforme NBR 10844."])
    done(s)


def incendio():
    s = Sheet("INC-01", "Incendio - sprinklers, hidrantes e saidas - pav. tipo", base=True); c = calc.incendio()
    draw_plan(s, "1", True, False)
    ym = (YB + YC) / 2; s.line((1.8, ym), (L - 1.8, ym), "INC")
    ys = [1.54 + 3.087 * j for j in range(7)]
    for i in range(30):
        x = 1.8 + 3.6 * i; s.line((x, ys[0]), (x, ys[-1]), "INC")
        for y in ys: s.circle((x, y), 0.14, "INC")
    for n, x, y in (("H-1", BAY + 0.6, YB - 0.5), ("H-2", 7 * BAY + 0.8, YC + 0.5), ("H-3", 14 * BAY - 0.6, YB - 0.5)):
        s.rect(x - 0.45, y - 0.3, 0.9, 0.6, "INC"); s.text(n, (x, y + 1.0), 2.2, "INC")
    s.circle((7.9 * BAY, YB + 0.8), 0.5, "INC"); s.text("VGA", (7.9 * BAY + 1.6, YB + 0.8), 2.0, "INC")
    for xj in (7 * BAY, 8 * BAY): s.line((xj, -2), (xj, YA + 2), "INC")
    s.text("COMPARTIMENTO 1", (3.5 * BAY, -1.6), 2.4, "INC"); s.text("COMP. 2", (7.5 * BAY, -1.6), 2.0, "INC"); s.text("COMPARTIMENTO 3", (11.5 * BAY, -1.6), 2.4, "INC")
    s.text("CHUVEIROS AUTOMATICOS, HIDRANTES E COMPARTIMENTACAO - 1o PAVIMENTO (tipo)   escala 1:200", (0, -7.5), 3.5, "NOTA", "l")
    s.table([["SISTEMA", "CRITERIO DE ANTEPROJETO", "NORMA"],
             ["Chuveiros automaticos", f"Risco ordinario grupo 2: 8,1 mm/min sobre 140 m2 = {c['spk']:.0f} L/min; {c['n_spk']} bicos por pavimento (malha 3,60 x 3,09 m = 11,1 m2/bico)", "NBR 10897"],
             ["Reserva tecnica de incendio", f"({c['spk']:.0f} + {c['hose']:.0f} L/min de mangueiras) x {c['t']} min = {f2(c['vol'], 0)} m3 -> adotado 130 m3", "NBR 10897"],
             ["Hidrantes", "3 por pavimento, mangueira de 40 mm x 30 m, 2 em uso simultaneo; todo ponto do pavimento a menos de 30 m de um hidrante", "NBR 13714"],
             ["Bombas", "Principal eletrica + reserva a diesel + jockey, em casa de bombas no anexo", "NBR 10897"],
             ["Deteccao e alarme", "Enderecavel, detector em todos os ambientes e no entreforro; aspiracao nas salas criticas", "NBR 17240"],
             ["Saidas", "3 escadas enclausuradas (E1, E2, E3); distancia maxima a percorrer no corredor: 25 m", "NBR 9077"],
             ["Extintores", "PQS ABC 6 kg e CO2 6 kg a cada 15 m de caminhamento e junto a cada quadro eletrico", "NBR 12693"],
             ["Supressao por gas", "Agente limpo no data center, com pre-alarme e botoeira de bloqueio", ""]], (0, -12), [48, 205, 28])
    notes(s, "LEGENDA E NOTAS", ["o    chuveiro automatico (sprinkler) pendente", "H-n  hidrante de parede com abrigo", "VGA  valvula de governo e alarme do pavimento",
                                 "", "1. Valores de vazao, densidade e reserva sao", "   de referencia; o calculo hidraulico e a", "   classificacao de risco devem ser feitos",
                                 "   pelo projetista e aprovados no CBMPE", "   (COSCIP-PE).", "2. Chuveiros tambem no entreforro quando houver", "   material combustivel.",
                                 "3. Selagem corta-fogo em toda passagem de", "   tubulacao por laje ou parede de", "   compartimentacao.",
                                 "4. Iluminacao de emergencia e sinalizacao de", "   rota de fuga conforme NBR 10898 e", "   NBR 13434."])
    done(s)


# ---------------- eletrica ----------------
def unifilar():
    s = Sheet("ELE-01", "Eletrica - diagrama unifilar geral e quadro de cargas"); c = calc.cargas(); r = calc.resumo_ele()
    X0, Y = -4, 40
    s.text("REDE DO CAMPUS 13,8 kV", (X0 + 18, Y + 6), 2.6, "ELE"); s.line((X0 + 18, Y + 4.8), (X0 + 18, Y + 1), "ELE"); s.rect(X0 + 15, Y - 3, 6, 4, "ELE"); s.text("CUBICULO MT", (X0 + 18, Y - 0.4), 1.7, "ELE"); s.text("disj. + protecao", (X0 + 18, Y - 1.8), 1.5, "ELE")
    s.line((X0 + 18, Y - 3), (X0 + 18, Y - 5), "ELE"); s.line((X0 + 8, Y - 5), (X0 + 28, Y - 5), "ELE")
    for i, x in enumerate((X0 + 8, X0 + 28)):
        s.line((x, Y - 5), (x, Y - 7), "ELE"); s.circle((x, Y - 8), 1.0, "ELE"); s.circle((x, Y - 9.3), 1.0, "ELE"); s.line((x, Y - 10.3), (x, Y - 13), "ELE")
        s.text(f"TR-{i + 1} 750 kVA a seco", (x + 1.8, Y - 8.2), 1.8, "ELE", "l"); s.text("13,8 kV / 380-220 V", (x + 1.8, Y - 9.6), 1.6, "ELE", "l"); s.rect(x - 0.7, Y - 12.4, 1.4, 1.0, "ELE"); s.text("1250 A", (x + 1.8, Y - 11.9), 1.6, "ELE", "l")
    yb = Y - 13; normal = [x for x in c if x["bus"] == "N"]; emer = [x for x in c if x["bus"] == "E"]
    s.m.add_lwpolyline([(X0, yb), (X0 + 90, yb)], dxfattribs={"layer": "ELE", "const_width": 0.25}); s.text(f"QGBT - barramento 380/220 V - 2000 A - Icc a calcular", (X0 + 60, yb + 1.2), 2.0, "ELE")
    s.rect(X0 + 17.3, yb - 0.5, 1.4, 1.0, "ELE"); s.text("TIE", (X0 + 18, yb - 1.4), 1.4, "ELE")
    dx = 90 / (len(normal) + 2)
    for i, f in enumerate(normal + [None]):
        x = X0 + dx * (i + 0.7); s.line((x, yb), (x, yb - 5), "ELE"); s.rect(x - 0.6, yb - 3, 1.2, 1.0, "ELE")
        if f: s.text(f["q"], (x, yb - 11), 1.7, "ELE", rot=90); s.text(f"{f['dj']} A", (x + 1.3, yb - 2.5), 1.3, "ELE", rot=90)
    xg = X0 + dx * (len(normal) + 0.7); s.text("QGE", (xg, yb - 6.2), 1.9, "ELE")
    ye = yb - 20; s.line((xg, yb - 7), (xg, ye + 4), "ELE"); s.rect(xg - 2, ye + 1, 4, 3, "ELE"); s.text("QTA", (xg, ye + 2.5), 1.8, "ELE"); s.line((xg, ye + 1), (xg, ye), "ELE")
    s.circle((xg + 9, ye + 2.5), 1.6, "ELE"); s.text("G", (xg + 9, ye + 2.5), 2.4, "ELE"); s.line((xg + 2, ye + 2.5), (xg + 7.4, ye + 2.5), "ELE"); s.text(f"GERADOR DIESEL {r['ger']} kVA", (xg + 9, ye + 5.2), 1.8, "ELE")
    s.m.add_lwpolyline([(xg - 44, ye), (xg + 6, ye)], dxfattribs={"layer": "ELE", "const_width": 0.25}); s.text("QGE - barra de emergencia (cargas criticas)", (xg - 28, ye + 1.2), 2.0, "ELE")
    for i, f in enumerate(emer):
        x = xg - 42 + i * 6.5; s.line((x, ye), (x, ye - 5), "ELE"); s.rect(x - 0.6, ye - 3, 1.2, 1.0, "ELE"); s.text(f["q"], (x, ye - 11), 1.7, "ELE", rot=90); s.text(f"{f['dj']} A", (x + 1.3, ye - 2.5), 1.3, "ELE", rot=90)
    s.text("DIAGRAMA UNIFILAR GERAL - sem escala", (X0 + 40, Y + 6), 3.5, "NOTA", "l")
    rows = [["QUADRO", "CARGA", "INST. (kW)", "F.D.", "DEM. (kW)", "I (A)", "DISJ. (A)", "ALIMENTADOR Cu EPR (mm2)", "BARRA"]]
    for f in c: rows.append([f["q"], f["d"], f2(f["kw"], 1), f2(f["fd"]), f2(f["dem"], 1), f"{f['i']:.0f}", str(f["dj"]), f["cab"], "Normal" if f["bus"] == "N" else "Emergencia"])
    rows.append(["TOTAL", "", f2(r["inst"], 0), "", f2(r["tot"], 0), "", "", "", ""])
    s.text("QUADRO DE CARGAS E ALIMENTADORES (pre-dimensionamento)", (92, 44), 2.8, "NOTA", "l"); y = s.table(rows, (92, 42.5), [22, 104, 20, 12, 20, 13, 17, 42, 22], 1.9)
    s.table([["RESUMO", ""], ["Demanda total", f"{f2(r['tot'], 0)} kW = {f2(r['kva'], 0)} kVA (fp 0,92)"], ["Transformadores", f"2 x 750 kVA a seco - carregamento de {r['carreg'] * 100:.0f} %"],
             ["Corrente nominal por trafo (380 V)", f"{r['i_tr']:.0f} A -> disjuntor geral de 1250 A"], ["Demanda de emergencia", f"{f2(r['de'], 0)} kW = {f2(r['ger_kva'], 0)} kVA -> gerador de {r['ger']} kVA"],
             ["Tensao de utilizacao", "380/220 V, 60 Hz, esquema TN-S"]], (92, y - 3), [70, 140], 2.0)
    notes(s, "NOTAS", ["1. Cargas estimadas por indices de area; refazer com a lista real de equipamentos.",
                       "2. Corrente = demanda / (raiz(3) x 380 V x 0,92). Disjuntor >= 1,25 x corrente. Cabo escolhido para",
                       "   capacidade em bandeja com fator de agrupamento 0,80. Verificar queda de tensao (max. 4 %) e curto-circuito.",
                       "3. Barramento do QGBT dividido em duas secoes com interligacao (TIE) normalmente aberta.",
                       "4. Transferencia automatica (QTA) em ate 15 s; no-break de 80 kVA sustenta o data center na transicao.",
                       "5. Todos os circuitos terminais com dispositivo DR; circuitos de laboratorio com detector de arco (AFDD).",
                       "6. Bomba de incendio com alimentacao independente, antes do disjuntor geral.",
                       "7. Projeto conforme NBR 5410 (baixa tensao), NBR 14039 (media tensao) e NBR 5419 (SPDA)."], (X0, -42), 2.2)
    done(s)


def ele_plan():
    s = Sheet("ELE-02", "Eletrica - iluminacao e quadros - pavimento-tipo", base=True); fl = "1"
    draw_plan(s, fl, True, False)
    for r in FLOORS[fl]:
        if r["kind"] in ("stair", "san", "hall"): continue
        yb0 = YB if r["band"] == "N" else YD
        for b in range(r["b0"], r["b1"]):
            for cx in (1.2, 3.6, 6.0):
                for j in range(6): s.rect(b * BAY + cx - 0.15, yb0 + 0.8 + 1.6 * j - 0.6, 0.3, 1.2, "ELE_LUM")
    for i in range(30): s.rect(1.8 + 3.6 * i - 0.6, (YB + YC) / 2 - 0.15, 1.2, 0.3, "ELE_LUM")
    yc = YB - 0.45; s.rect(0.6, yc - 0.15, L - 1.2, 0.3, "ELE_CALHA"); s.text("ELETROCALHA 300 x 100 (forca) + 200 x 100 (dados) no entreforro", (2.5 * BAY, yc + 0.7), 1.6, "ELE_CALHA")
    for n, x in ((f"QDI-{fl}A", 2 * BAY + 0.5), (f"QDL-{fl}A", 3 * BAY + 1.2), (f"QDL-{fl}B", 11 * BAY + 1.2), (f"QDI-{fl}B", 12 * BAY + 0.5)):
        s.solid(x, YC + 0.1, 0.9, 0.25, "ELE"); s.text(n, (x + 0.45, YC + 0.95), 1.9, "ELE")
    s.rect(7 * BAY + 3.5, 3.3, 3.2, 1.3, "ELE"); s.text("PRUMADAS", (7 * BAY + 5.1, 5.1), 1.6, "ELE")
    for x in (0.6, 7 * BAY - 0.8, 8 * BAY + 0.8, L - 0.6):
        s.circle((x, (YB + YC) / 2 + 0.7), 0.3, "INC"); s.text("EM", (x, (YB + YC) / 2 + 1.4), 1.4, "INC")
    s.text("ILUMINACAO, QUADROS E ELETROCALHAS - 1o PAVIMENTO (tipo)   escala 1:200", (0, -7.5), 3.5, "NOTA", "l")
    s.table([["AMBIENTE", "ILUMINANCIA", "LUMINARIAS POR MODULO DE 69 m2", "POTENCIA"],
             ["Laboratorios, salas e informatica", "500 lux", "18 paineis LED 40 W / 4000 lm (3 x 6); N = 500 x 69,1 / (4000 x 0,60 x 0,80) = 18", "10,4 W/m2"],
             ["Salas criticas e apoio", "300 lux", "12 paineis LED 40 W", "6,9 W/m2"],
             ["Circulacao", "150 lux", "1 luminaria linear 20 W a cada 3,60 m", "2,3 W/m2"],
             ["Escadas", "150 lux", "Arandelas blindadas com bloco autonomo", ""]], (0, -12), [60, 26, 130, 26])
    s.table([["QUADRO", "ATENDE", "CIRCUITOS TIPICOS"],
             [f"QDI-{fl}A / QDI-{fl}B", "Iluminacao e tomadas de uso geral do bloco", "Iluminacao 220 V em circuitos de 10 A (ate 1200 W); tomadas de 20 A a cada 3 m de parede"],
             [f"QDL-{fl}A / QDL-{fl}B", "Bancadas e equipamentos de laboratorio", "Subquadro por laboratorio com botao de desligamento geral na porta; 1 circuito de 20 A a cada 3 tomadas de bancada"],
             ["QDE (emergencia)", "Freezers, capelas, iluminacao de seguranca", "Tomadas vermelhas identificadas, alimentadas pelo gerador"]], (0, -32), [42, 70, 170])
    notes(s, "LEGENDA E NOTAS", ["[]   luminaria LED 30 x 120 cm embutida", "EM   bloco autonomo de emergencia", "QDI  quadro de iluminacao e tomadas",
                                 "QDL  quadro de laboratorios", "", "1. Comando da iluminacao por sala, com sensor", "   de presenca em circulacoes e sanitarios.",
                                 "2. Eletrocalhas separadas para forca e dados,", "   com septos e tampas; selagem corta-fogo", "   nas juntas (eixos 8 e 9).",
                                 "3. Tomadas de bancada em canaleta de aluminio", "   a 1,10 m; pontos junto a pias com IP44.", "4. Aterramento e equipotencializacao por",
                                 "   laboratorio (barra BEL).", "5. Cabos nao halogenados (NBR 13248) em todo", "   o predio.", "6. Ver detalhe do modulo na prancha DET-01."])
    done(s)


# ---------------- modulo-tipo ----------------
def modulo():
    s = Sheet("DET-01", "Detalhe - modulo-tipo de laboratorio", 50, (60, 230))
    W_, D_ = 7.05, 9.425

    def base(ox, title):
        s.rect(ox - 0.15, -0.2, W_ + 0.3, D_ + 0.35); s.rect(ox, 0, W_, D_)
        s.rect(ox, 0, W_, 0.75, "MOBILIA")                                    # bancada de fachada
        for bx in (ox + 1.95, ox + 4.35): s.rect(bx, 1.95, 0.75 if False else 1.5, 5.2, "MOBILIA")   # bancadas centrais (ilhas 1,50)
        s.rect(ox, 7.6, 0.75, 1.3, "MOBILIA"); s.rect(ox + W_ - 1.0, 7.9, 1.0, 1.5, "MOBILIA")
        s.line((ox + 0.8, D_), (ox + 0.8, D_ - 1.1), "ESQUADRIA"); s.arc((ox + 0.8, D_), 1.1, 270, 360, "ESQUADRIA")
        for cx in (1.725, 5.325): s.rect(ox + cx - 1.2, -0.2, 2.4, 0.2, "ESQUADRIA")
        s.text(title, (ox + W_ / 2, -1.6), 3.2, "NOTA"); s.dim((ox, D_), (ox + W_, D_), 0.9); s.dim((ox, 0), (ox, D_), -0.9)

    base(0, "ARQUITETURA - layout de bancadas")
    s.text("BANCADA DE FACHADA 0,75", (3.5, 0.38), 1.8, "MOBILIA"); s.text("ILHA 1,50 x 5,20", (2.7, 4.5), 1.8, "MOBILIA", rot=90); s.text("ILHA 1,50 x 5,20", (5.1, 4.5), 1.8, "MOBILIA", rot=90)
    s.text("CAPELA", (6.55, 8.65), 1.6, "MOBILIA", rot=90); s.text("ARM. CORTA-FOGO", (0.38, 8.25), 1.4, "MOBILIA", rot=90)
    s.dim((0, 1.3), (1.95, 1.3), 0.0, "1,95"); s.dim((3.45, 1.3), (4.35, 1.3), 0.0, "0,90 (*)"); s.dim((5.85, 1.3), (7.05, 1.3), 0.0, "1,20")
    s.text("(*) entre ilhas: 0,90 m minimo; recomenda-se 1,50 m com uma ilha a menos em laboratorios de uso intenso", (0, -2.6), 1.9, "NOTA", "l")
    ox = 10
    base(ox, "HIDRAULICA - pontos de agua e esgoto")
    s.line((ox + 0.3, D_ - 0.35), (ox + W_ - 0.3, D_ - 0.35), "HID_AF"); s.text("AF 32 mm no entreforro", (ox + 3.5, D_ - 0.8), 1.8, "HID_AF")
    for cx in (1.725, 5.325):
        s.line((ox + cx, D_ - 0.35), (ox + cx, 0.55), "HID_AF"); s.rect(ox + cx - 0.3, 0.15, 0.6, 0.45, "HID_AF"); s.text("PIA  AF 25 / ES 50", (ox + cx, 1.05), 1.7, "HID_AF")
        s.line((ox + cx + 0.15, 0.15), (ox + cx + 0.15, -0.9), "HID_EL")
    s.line((ox + 0.6, -0.9), (ox + W_ - 0.4, -0.9), "HID_EL"); s.text("EL 75 mm em PP sob a laje, i = 2 %", (ox + 3.5, -0.55), 1.7, "HID_EL")
    s.circle((ox + 2.3, D_ - 1.0), 0.3, "HID_AP"); s.text("CE - chuveiro e lava-olhos, AF 32 mm + ralo DN 100", (ox + 2.8, D_ - 1.45), 1.7, "HID_AP", "l")
    s.circle((ox + 6.55, 8.65), 0.2, "HID_AF"); s.text("ponto de agua e dreno na capela", (ox + 6.2, 7.5), 1.6, "HID_AF", "r")
    s.circle((ox + 3.5, 4.5), 0.14, "INC"); s.text("sprinkler", (ox + 3.5, 4.1), 1.5, "INC")
    for (px, py) in ((1.7, 1.54), (5.3, 1.54), (1.7, 7.7), (5.3, 7.7), (1.7, 4.63), (5.3, 4.63)): s.circle((ox + px, py), 0.14, "INC")
    ox = 20
    base(ox, "ELETRICA - iluminacao e tomadas")
    for cx in (1.125, 3.525, 5.925):
        for j in range(6): s.rect(ox + cx - 0.15, 0.8 + 1.6 * j - 0.6 + 0.0, 0.3, 1.2, "ELE_LUM")
    for i in range(11): s.circle((ox + 0.4 + i * 0.6, 0.72), 0.07, "ELE")
    for bx in (1.95, 4.35):
        for j in range(8): s.circle((ox + bx + 0.75, 2.2 + j * 0.66), 0.07, "ELE")
    s.solid(ox + 2.0, D_ - 0.12, 0.8, 0.12, "ELE"); s.text("QD-LAB + botao de desligamento geral", (ox + 2.9, D_ - 0.6), 1.7, "ELE", "l")
    s.text("tomadas 2P+T 20 A / 220 V a cada 0,60 m", (ox + 3.5, 1.15), 1.7, "ELE"); s.text("canaleta central da ilha", (ox + 3.55, 7.45), 1.6, "ELE")
    s.circle((ox + 6.55, 8.65), 0.12, "ELE"); s.text("capela: 220 V + intertravamento", (ox + 6.2, 9.15), 1.5, "ELE", "r")
    s.circle((ox + 0.38, 8.25), 0.12, "INC"); s.text("TE (emergencia)", (ox + 0.9, 8.25), 1.5, "INC", "l")
    s.table([["ITEM", "QUANT. POR MODULO", "ESPECIFICACAO"],
             ["Luminarias", "18", "Painel LED 30 x 120, 40 W, 4000 K, IRC > 80 - 500 lux"],
             ["Tomadas de bancada", "27", "2P+T 20 A, 220 V, em canaleta; 9 circuitos de 20 A com DR 30 mA"],
             ["Tomadas de emergencia", "2", "Vermelhas, pela barra do gerador (freezers e estufas)"],
             ["Pias", "2", "Cuba de inox ou resina epoxi, torneira de bancada; esgoto de laboratorio"],
             ["Chuveiro de emergencia", "1 por laboratorio", "Com lava-olhos, acionamento por alavanca, a ate 10 s de percurso"],
             ["Capela de exaustao", "conforme programa", "Vazao variavel, velocidade de face 0,5 m/s, duto proprio ate a cobertura"],
             ["Sprinklers", "6", "Pendente, resposta rapida, 68 C"],
             ["Pontos de dados", "8", "Cat. 6A em canaleta separada"]], (0, -4.5), [44, 44, 130], 2.2)
    done(s)


if __name__ == "__main__":
    implantacao(); arq_plan("ARQ-02", "T"); arq_plan("ARQ-03", "1"); arq_plan("ARQ-04", "2"); arq_roof(); cortes(); fachadas(); modulo()
    estrutura(); hid_af(); hid_es(); hid_ap(); incendio(); unifilar(); ele_plan()
    import json; json.dump(SHEETS, open(OUT + "/sheets.json", "w"))
