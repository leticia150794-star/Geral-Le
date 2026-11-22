from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as CL
from cad import *
import calc, detail

F = Font(name="Arial", size=10); FB = Font(name="Arial", size=10, bold=True); FT = Font(name="Arial", size=13, bold=True)
HDR = PatternFill("solid", fgColor="1F3A4D"); FH = Font(name="Arial", size=10, bold=True, color="FFFFFF"); INP = PatternFill("solid", fgColor="FFFF00")
FIN = Font(name="Arial", size=10, color="0000FF"); thin = Side(style="thin", color="BBBBBB"); BD = Border(top=thin, bottom=thin, left=thin, right=thin)
wb = Workbook()


def sheet(name, title, headers, widths):
    ws = wb.create_sheet(name); ws["A1"] = title; ws["A1"].font = FT
    for i, (h, w) in enumerate(zip(headers, widths), 1):
        c = ws.cell(3, i, h); c.font = FH; c.fill = HDR; c.alignment = Alignment(wrap_text=True, vertical="center"); c.border = BD; ws.column_dimensions[CL(i)].width = w
    ws.freeze_panes = "A4"; return ws


def put(ws, r, vals, fmt=None, bold=False):
    for i, v in enumerate(vals, 1):
        c = ws.cell(r, i, v); c.font = FB if bold else F; c.border = BD
        if fmt and i in fmt: c.number_format = fmt[i]


# ---------- Leia-me ----------
ws = wb.active; ws.title = "Leia-me"; ws.column_dimensions["A"].width = 120
for i, t in enumerate(["Reconstrucao do bloco de laboratorios da UFPE - quantitativos e quadros (anteprojeto R00, 22/11/2026)", "",
                       "Esta planilha acompanha o caderno de pranchas. Os numeros saem do mesmo modelo geometrico das plantas.",
                       "E um levantamento de anteprojeto: nao houve visita, topografia nem sondagem, e os quantitativos sao aproximados.",
                       "", "Como usar:", "- Celulas amarelas sao para preencher ou ajustar (precos unitarios, comprimento de estaca, parametros).",
                       "- Texto azul marca hipoteses adotadas; mude o valor e as formulas recalculam.",
                       "- A linha marcada EXEMPLO na aba Quantitativos mostra o formato esperado; o preco dela e ilustrativo, nao e cotacao.",
                       "- Precos unitarios devem vir do SINAPI (Caixa) do mes de referencia, para Pernambuco, ou de cotacoes.", "",
                       "Abas: Ambientes, Esquadrias, Cargas gerais, Quadros eletricos, Resumo quadros, Hidraulica, Quantitativos."], 1):
    ws.cell(i, 1, t).font = FT if i == 1 else F

# ---------- Ambientes ----------
ws = sheet("Ambientes", "Ambientes - areas, perimetros e acabamentos", ["Pavimento", "Bloco", "Ambiente", "Tipo", "Largura (m)", "Profundidade (m)", "Area util (m2)", "Perimetro (m)", "Pe-direito (m)", "Area de parede (m2)", "Piso", "Forro"], [13, 8, 36, 12, 12, 14, 14, 13, 12, 16, 30, 24])
TIPO = {"lab": "Laboratorio", "off": "Permanencia", "teach": "Ensino", "sup": "Apoio", "crit": "Sala critica", "stair": "Escada", "san": "Sanitario", "hall": "Hall / estar"}
PISO = {"lab": "Vinilico em manta, rodape curvo", "crit": "Epoxi autonivelante", "san": "Porcelanato", "stair": "Concreto polido antiderrapante"}
FORRO = {"lab": "Removivel lavavel", "crit": "Laje aparente pintada", "stair": "Laje aparente"}
r = 4
for fl in "T12":
    for rm in FLOORS[fl]:
        x0, y0, x1, y1 = box(rm); blk = "Nucleo" if rm["b0"] == 7 else ("A" if rm["b0"] < 7 else "B"); k = rm["kind"]
        put(ws, r, [FLOOR_NAME[fl], blk, rm["name"], TIPO[k], round(x1 - x0, 2), round(y1 - y0, 3), f"=E{r}*F{r}", f"=2*(E{r}+F{r})", 3.2, f"=H{r}*I{r}", PISO.get(k, "Porcelanato / vinilico"), FORRO.get(k, "Removivel mineral")],
            {5: "0.00", 6: "0.00", 7: "0.0", 8: "0.0", 9: "0.00", 10: "0.0"}); r += 1
    put(ws, r, [FLOOR_NAME[fl], "Todos", "CIRCULACAO", "Circulacao", round(L - 2 * WE, 2), round(YB - YC - 2 * WI, 2), f"=E{r}*F{r}", f"=2*(E{r}+F{r})", 3.2, f"=H{r}*I{r}", "Vinilico em manta", "Removivel mineral"], {5: "0.00", 6: "0.00", 7: "0.0", 8: "0.0", 9: "0.00", 10: "0.0"}); r += 1
AMB_LAST = r - 1
put(ws, r, ["TOTAL", "", "", "", "", "", f"=SUM(G4:G{AMB_LAST})", "", "", f"=SUM(J4:J{AMB_LAST})", "", ""], {7: "#,##0.0", 10: "#,##0.0"}, True)
ws.cell(r + 2, 1, "Area de parede = perimetro x pe-direito livre, sem descontar vaos; cada parede divisoria aparece nos dois ambientes que separa.").font = F

# ---------- Esquadrias ----------
ws = sheet("Esquadrias", "Quadro de esquadrias - predio inteiro", ["Tipo", "Largura (m)", "Altura (m)", "Quantidade", "Area unitaria (m2)", "Area total (m2)", "Especificacao"], [12, 12, 12, 12, 16, 16, 70])
cnt = detail.esquadrias()
ESQ = [("P1", 0.90, 2.10, "Porta de madeira laminada, batente metalico"), ("P2", 1.10, 2.10, "Porta de laboratorio com visor, mola e barra"), ("P3", 1.60, 2.10, "Porta dupla, abre no sentido da saida, barra antipanico"),
       ("PCF-90", 1.00, 2.10, "Porta corta-fogo 90 min (escadas e juntas do corredor)"), ("PCF-120", 1.10, 2.10, "Porta corta-fogo 120 min (salas criticas)"), ("J1", 2.40, 1.50, "Janela de aluminio, vidro laminado 8 mm, peitoril 1,10 m")]
for i, (t, w, h, d) in enumerate(ESQ, 4): put(ws, i, [t, w, h, cnt[t], f"=B{i}*C{i}", f"=D{i}*E{i}", d], {2: "0.00", 3: "0.00", 5: "0.00", 6: "0.0"})
put(ws, 10, ["TOTAL", "", "", "=SUM(D4:D9)", "", "=SUM(F4:F9)", ""], {6: "0.0"}, True)

# ---------- Cargas gerais ----------
ws = sheet("Cargas gerais", "Quadro geral de cargas e alimentadores", ["Quadro", "Carga", "Instalada (kW)", "Fator de demanda", "Demanda (kW)", "Corrente (A)", "Disjuntor minimo 1,25 x I (A)", "Disjuntor adotado (A)", "Alimentador Cu EPR (mm2)", "Barra"], [12, 62, 14, 12, 14, 13, 16, 14, 22, 12])
ws["L3"] = "Tensao de linha (V)"; ws["M3"] = 380; ws["L4"] = "Fator de potencia"; ws["M4"] = 0.92; ws["L5"] = "Potencia dos transformadores (kVA)"; ws["M5"] = 1500
for c in ("L3", "L4", "L5"): ws[c].font = F
for c in ("M3", "M4", "M5"): ws[c].font = FIN; ws[c].fill = INP
ws.column_dimensions["L"].width = 34
cg = calc.cargas()
for i, x in enumerate(cg, 4):
    put(ws, i, [x["q"], x["d"], round(x["kw"], 1), round(x["fd"], 3), f"=C{i}*D{i}", f"=E{i}*1000/(SQRT(3)*$M$3*$M$4)", f"=1.25*F{i}", x["dj"], x["cab"], "Normal" if x["bus"] == "N" else "Emergencia"], {3: "0.0", 4: "0.00", 5: "0.0", 6: "0", 7: "0"})
    ws.cell(i, 3).font = FIN; ws.cell(i, 4).font = FIN
n = 4 + len(cg); CG_LAST = n - 1
put(ws, n, ["TOTAL", "", f"=SUM(C4:C{CG_LAST})", "", f"=SUM(E4:E{CG_LAST})", "", "", "", "", ""], {3: "#,##0", 5: "#,##0"}, True)
put(ws, n + 1, ["Demanda aparente (kVA)", "", "", "", f"=E{n}/$M$4"], {5: "#,##0"}); put(ws, n + 2, ["Carregamento dos transformadores", "", "", "", f"=E{n + 1}/$M$5"], {5: "0%"})
put(ws, n + 3, ["Demanda de emergencia (kW)", "", "", "", f'=SUMIFS(E4:E{CG_LAST},J4:J{CG_LAST},"Emergencia")'], {5: "#,##0"}); put(ws, n + 4, ["Gerador minimo, fp 0,8 (kVA)", "", "", "", f"=E{n + 3}/0.8"], {5: "#,##0"})
ws.cell(n + 6, 1, "Cargas em azul sao estimativas por indice de area (300 W/m2 de equipamentos em laboratorio; 7 + 25 W/m2 de iluminacao e tomadas). Disjuntor e cabo adotados vem do pre-dimensionamento do caderno.").font = F

# ---------- Quadros eletricos ----------
ws = sheet("Quadros eletricos", "Circuitos dos quadros de iluminacao e tomadas (QDI)", ["Quadro", "Circuito", "Descricao", "Potencia (W)", "Fase", "Tensao (V)", "Corrente (A)", "Cabo (mm2)", "Disjuntor (A)", "DR"], [12, 10, 52, 13, 8, 11, 12, 11, 13, 10])
r = 4; boards = []
for fl in "T12":
    for blk in "AB":
        q = f"QDI-{fl}{blk}"; boards.append(q)
        for nn, d, w, ph, sec, dj, _ in detail.circuitos(fl, blk):
            put(ws, r, [q, nn, d, w, ph, 220, f"=D{r}/F{r}", sec, dj, "30 mA"], {7: "0.0", 8: "0.0"}); r += 1
QE_LAST = r - 1
ws2 = sheet("Resumo quadros", "Resumo por quadro e por fase", ["Quadro", "Circuitos", "Potencia total (W)", "Fase R (W)", "Fase S (W)", "Fase T (W)", "Desequilibrio maximo"], [14, 12, 18, 14, 14, 14, 20])
for i, q in enumerate(boards, 4):
    rng = f"'Quadros eletricos'!$A$4:$A${QE_LAST}"; pw = f"'Quadros eletricos'!$D$4:$D${QE_LAST}"; ph = f"'Quadros eletricos'!$E$4:$E${QE_LAST}"
    put(ws2, i, [q, f"=COUNTIF({rng},A{i})", f"=SUMIFS({pw},{rng},A{i})"] + [f'=SUMIFS({pw},{rng},$A{i},{ph},"{p}")' for p in "RST"] + [f"=(MAX(D{i}:F{i})-MIN(D{i}:F{i}))/AVERAGE(D{i}:F{i})"], {3: "#,##0", 4: "#,##0", 5: "#,##0", 6: "#,##0", 7: "0%"})
put(ws2, 10, ["TOTAL", "=SUM(B4:B9)", "=SUM(C4:C9)", "=SUM(D4:D9)", "=SUM(E4:E9)", "=SUM(F4:F9)", ""], {3: "#,##0", 4: "#,##0", 5: "#,##0", 6: "#,##0"}, True)
ws2.cell(12, 1, "Fases distribuidas em rodizio simples; o equilibrio fino cabe ao projeto executivo. Circuitos de laboratorio ficam nos quadros QDL (ver prancha ELE-03).").font = F

# ---------- Hidraulica ----------
ws = sheet("Hidraulica", "Aparelhos e contribuicoes por pavimento", ["Pavimento", "Bacias", "Lavatorios", "Mictorios", "Tanques", "Pias de laboratorio", "Chuveiros de emergencia", "Soma de pesos (agua fria)", "UHC (esgoto)"], [14, 10, 12, 11, 10, 18, 22, 22, 14])
for c, v in (("L3", "Peso bacia"), ("L4", "Peso lavatorio"), ("L5", "Peso mictorio"), ("L6", "Peso tanque"), ("L7", "Peso pia"), ("L8", "UHC bacia"), ("L9", "UHC lavatorio"), ("L10", "UHC mictorio"), ("L11", "UHC tanque"), ("L12", "UHC pia")): ws[c] = v; ws[c].font = F
for c, v in (("M3", 0.3), ("M4", 0.3), ("M5", 0.3), ("M6", 0.7), ("M7", 0.7), ("M8", 6), ("M9", 1), ("M10", 2), ("M11", 3), ("M12", 3)): ws[c] = v; ws[c].font = FIN; ws[c].fill = INP
ws.column_dimensions["L"].width = 16
for i, fl in enumerate("T12", 4):
    ce = sum(1 for rm in FLOORS[fl] if rm.get("wet") and rm["kind"] == "lab")
    put(ws, i, [FLOOR_NAME[fl], 8, 6, 2, 1, calc.pias(fl), ce, f"=B{i}*$M$3+C{i}*$M$4+D{i}*$M$5+E{i}*$M$6+F{i}*$M$7", f"=B{i}*$M$8+C{i}*$M$9+D{i}*$M$10+E{i}*$M$11+F{i}*$M$12"], {8: "0.0"})
put(ws, 7, ["TOTAL"] + [f"=SUM({CL(c)}4:{CL(c)}6)" for c in range(2, 10)], {8: "0.0"}, True)
put(ws, 9, ["Vazao maxima provavel no barrilete (L/s)", "", "", "", "", "", "", "=0.3*SQRT(H7)"], {8: "0.00"})
ws.cell(11, 1, "Pesos e unidades Hunter de contribuicao (UHC) adotados como referencia, a conferir na NBR 5626 e na NBR 8160.").font = F

# ---------- Quantitativos ----------
ws = sheet("Quantitativos", "Quantitativos de anteprojeto e planilha de precos", ["Grupo", "Item", "Unidade", "Quantidade", "Como foi obtido", "Preco unitario (R$)", "Total (R$)"], [16, 52, 9, 14, 70, 18, 18])
for c, v, val in (("J3", "Comprimento medio de estaca (m)", 20), ("J4", "Espessura media equivalente da laje nervurada (m)", 0.20), ("J5", "Area de um pavimento pelas faces externas (m2)", 108.2 * 21.8), ("J6", "Numero de lajes (terreo + 3)", 5), ("J7", "Altura total dos pilares (m)", 15.9)):
    ws[c] = v; ws[c].font = F; k = "K" + c[1:]; ws[k] = val; ws[k].font = FIN; ws[k].fill = INP
ws.column_dimensions["J"].width = 46; ws.column_dimensions["K"].width = 12
lum = sum(x[2] for fl in "T12" for blk in "AB" for x in detail.circuitos(fl, blk) if x[1].startswith("Ilum")) // 40
lab_lum = sum(18 * (rm["b1"] - rm["b0"]) for fl in "T12" for rm in FLOORS[fl] if rm["kind"] == "lab")
Q = [("EXEMPLO", "Concreto usinado fck 35 MPa (linha de exemplo, apagar)", "m3", 100, "Valor ilustrativo para mostrar o preenchimento", 600),
     ("Fundacoes", "Estacas helice continua D60", "m", "=64*$K$3", "64 estacas x comprimento medio (celula K3)", None),
     ("Fundacoes", "Estacas helice continua D70", "m", "=64*$K$3", "64 estacas x comprimento medio (celula K3)", None),
     ("Fundacoes", "Concreto dos blocos", "m3", "=32*1.1*2.8*1+32*1.1*3.2*1.2", "32 blocos B1 + 32 blocos B2 (prancha EST-02)", None),
     ("Fundacoes", "Vigas baldrame 30 x 70", "m3", "=(4*108+16*21.6)*0.3*0.7", "4 linhas longitudinais + 16 transversais", None),
     ("Estrutura", "Concreto dos pilares 40 x 70", "m3", "=64*0.4*0.7*$K$7", "64 pilares x secao x altura (K7)", None),
     ("Estrutura", "Concreto das lajes nervuradas", "m3", "=$K$5*$K$6*$K$4", "area x numero de lajes x espessura equivalente", None),
     ("Estrutura", "Concreto das vigas transversais 40 x 60 (parte abaixo da laje)", "m3", "=16*21.6*0.4*0.25*$K$6", "16 eixos x 21,6 m x 0,40 x 0,25 x lajes", None),
     ("Estrutura", "Forma de laje (cubetas)", "m2", "=$K$5*$K$6", "area x numero de lajes", None),
     ("Vedacoes", "Paredes internas (area bruta)", "m2", f"=Ambientes!J{AMB_LAST + 1}/2", "metade da soma das areas de parede dos ambientes (cada divisoria conta duas vezes)", None),
     ("Vedacoes", "Paredes externas", "m2", "=2*(108.2+21.8)*13.5-Esquadrias!F9", "perimetro x 13,5 m de altura, menos janelas", None),
     ("Pisos", "Piso acabado", "m2", f"=Ambientes!G{AMB_LAST + 1}", "soma das areas uteis", None),
     ("Cobertura", "Impermeabilizacao da laje de cobertura", "m2", "=$K$5", "area de um pavimento", None),
     ("Esquadrias", "Portas (todas)", "un", "=SUM(Esquadrias!D4:D8)", "aba Esquadrias", None),
     ("Esquadrias", "Janelas J1", "un", "=Esquadrias!D9", "aba Esquadrias", None),
     ("Eletrica", "Luminarias LED 40 W (todas, inclusive laboratorios)", "un", lum, "potencia dos circuitos de iluminacao dos QDI / 40 W", None),
     ("Eletrica", "Transformadores a seco 750 kVA", "un", 2, "prancha ELE-01", None), ("Eletrica", "Grupo gerador diesel 450 kVA", "un", 1, "prancha ELE-01", None),
     ("Eletrica", "Quadros de distribuicao (QDI + QDL)", "un", 12, "2 por bloco por pavimento", None),
     ("Incendio", "Chuveiros automaticos", "un", "=210*3", "210 por pavimento (prancha INC-01)", None), ("Incendio", "Hidrantes de parede", "un", 9, "3 por pavimento", None),
     ("Incendio", "Reserva tecnica de incendio", "m3", 130, "prancha INC-01", None),
     ("Hidraulica", "Bacias sanitarias", "un", "=Hidraulica!B7", "aba Hidraulica", None), ("Hidraulica", "Lavatorios", "un", "=Hidraulica!C7", "aba Hidraulica", None),
     ("Hidraulica", "Pias de laboratorio", "un", "=Hidraulica!F7", "aba Hidraulica", None), ("Hidraulica", "Chuveiros de emergencia com lava-olhos", "un", "=Hidraulica!G7", "aba Hidraulica", None),
     ("Climatizacao", "Resfriadores de liquido 180 TR", "un", 3, "prancha CLI-01 (2 em operacao + 1 reserva)", None),
     ("Transporte", "Elevadores", "un", 2, "1 social + 1 de emergencia / macas", None)]
for i, (g, it, u, q, how, pr) in enumerate(Q, 4):
    put(ws, i, [g, it, u, q, how, pr, f'=IF(F{i}="","",D{i}*F{i})'], {4: "#,##0.0", 6: "#,##0.00", 7: "#,##0.00"})
    ws.cell(i, 6).fill = INP; ws.cell(i, 6).font = FIN
n = 4 + len(Q)
put(ws, n, ["TOTAL (sem a linha EXEMPLO)", "", "", "", "", "", f"=SUM(G5:G{n - 1})"], {7: "#,##0.00"}, True)
ws.cell(n + 2, 1, "Lista parcial: faltam, entre outros, armaduras, revestimentos, forros, tubulacoes, cabos, dutos, bancadas, capelas e canteiro. Preencha os precos em amarelo com SINAPI ou cotacoes.").font = F
wb.save(OUT + "/quantitativos-e-quadros.xlsx"); print("ok", QE_LAST - 3, "circuitos")
