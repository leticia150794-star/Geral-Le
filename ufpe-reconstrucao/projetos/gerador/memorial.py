import json, calc
from cad import OUT
f=lambda v,n=1: f"{v:.{n}f}".replace(".",",")
c=calc.cargas(); r=calc.resumo_ele(); a=calc.agua(); e=calc.esgoto(); p=calc.pluvial(); i=calc.incendio(); s=calc.estrutura()
sheets=json.load(open(OUT+"/sheets.json"))
m=["# Memorial descritivo e de cálculo — anteprojeto","",
"Reconstrução do bloco de laboratórios da UFPE (Campus Recife). Revisão R00, 22/11/2026.","",
"> **Alcance.** Este caderno é um anteprojeto gerado sem visita, levantamento topográfico, sondagem ou cadastro de redes. Os cálculos são pré-dimensionamentos por índices e métodos simplificados. Não substitui os projetos legais e executivos, que precisam de responsáveis técnicos habilitados (RRT/ART) e de aprovação no Corpo de Bombeiros (COSCIP-PE), na Prefeitura e na concessionária.","",
"## 1. Lista de pranchas","","| Prancha | Conteúdo | Escala |","|---|---|---|"]
m+=[f"| {x[0]} | {x[1]} | 1:{x[2]} |" for x in sheets]
m+=["","Cada prancha existe em PDF (`pdf/`) e em DXF (`dxf/`, em metros, para AutoCAD, BricsCAD, QCAD ou LibreCAD). O arquivo `caderno-de-projetos.pdf` reúne todas.","",
"## 2. Arquitetura","",
"- Barra de 108,00 × 21,60 m entre eixos, térreo mais dois pavimentos e cobertura técnica; área construída de 3 × 2.358,8 = 7.076 m² pelas faces externas (6.998 m² pelos eixos).",
"- Malha de 15 vãos de 7,20 m; faixas de 9,60 m (sul, laboratórios), 2,40 m (corredor) e 9,60 m (norte, permanência).",
"- Níveis: térreo +1,20; 1º pavimento +5,70; 2º pavimento +10,20; cobertura +14,70. Piso a piso 4,50 m, pé-direito livre 3,20 m.",
"- Dois blocos de 50,40 m e núcleo central de 7,20 m, separados por juntas de dilatação que coincidem com as barreiras corta-fogo.",
"- Três escadas enclausuradas (E1, E2, E3), dois elevadores, sanitários e shafts em todos os pavimentos.",
"- Quadros de áreas e de acabamentos por ambiente nas pranchas ARQ-02 a ARQ-04.","",
"## 3. Estrutura (pré-dimensionamento)","",
f"- Concreto armado, fck 35 MPa, classe de agressividade III; pilares 40 × 70 cm; laje nervurada de 35 cm.",
f"- Cargas: permanente {f(s['g'])} kN/m², sobrecarga {f(s['q'])} kN/m².",
f"- Pilar interno: {f(s['ai'])} m² × 4 lajes × {f(s['g']+s['q'])} kN/m² = {s['ni']:.0f} kN em serviço; Nd = {s['nid']:.0f} kN, contra 0,85·fcd·Ac = {s['nrd']:.0f} kN (aproveitamento de {s['nid']/s['nrd']*100:.0f} %, sem contar armadura nem flexão).",
f"- Pilar de fachada: {f(s['ae'])} m² × 4 lajes → {s['ne']:.0f} kN em serviço.",
"- Fundações previstas em estacas hélice contínua; diâmetro e profundidade dependem de sondagem SPT.","",
"## 4. Elétrica","",
"Tensão 380/220 V, esquema TN-S. Corrente = demanda ÷ (√3 × 380 V × 0,92). Disjuntor ≥ 1,25 × corrente. Cabo de cobre EPR em bandeja, fator de agrupamento 0,80.","",
"| Quadro | Carga | Instalada (kW) | F.D. | Demanda (kW) | I (A) | Disjuntor (A) | Alimentador (mm²) | Barra |","|---|---|---:|---:|---:|---:|---:|---|---|"]
m+=[f"| {x['q']} | {x['d']} | {f(x['kw'])} | {f(x['fd'],2)} | {f(x['dem'])} | {x['i']:.0f} | {x['dj']} | {x['cab']} | {'Normal' if x['bus']=='N' else 'Emergência'} |" for x in c]
m+=[f"| **Total** | | **{f(r['inst'],0)}** | | **{f(r['tot'],0)}** | | | | |","",
f"- Demanda total: {f(r['tot'],0)} kW = {f(r['kva'],0)} kVA.",
f"- Subestação: 2 transformadores a seco de 750 kVA (carregamento de {r['carreg']*100:.0f} %); corrente nominal de {r['i_tr']:.0f} A por transformador.",
f"- Cargas de emergência: {f(r['de'],0)} kW = {f(r['ger_kva'],0)} kVA → gerador a diesel de {r['ger']} kVA.",
"- Iluminação: 500 lux em laboratórios e salas, com 18 painéis LED de 40 W por módulo de 69 m² (10,4 W/m²).",
"- Falta verificar queda de tensão, curto-circuito e seletividade.","",
"## 5. Água fria","",
f"- População de cálculo: {a['pop']} pessoas. Consumo: {a['pop']} × 50 L + 10 m³ de processo = {f(a['cons'],0)} m³/dia.",
f"- Reserva de 1,5 dia: {f(a['res'],0)} m³ ({a['inf']} m³ no reservatório inferior e {a['sup']} m³ no superior).",
"- Vazões pelo método dos pesos, Q = 0,3·√ΣP (L/s), com velocidade máxima de 1,5 m/s.","",
"| Trecho | Soma de pesos | Vazão (L/s) | Tubo PVC (DE mm) | Velocidade (m/s) |","|---|---:|---:|---:|---:|"]
m+=[f"| {k} | {f(pp)} | {f(q,2)} | {de} | {f(v,2)} |" for k,pp,q,de,v in a["rows"]]
m+=["","## 6. Esgoto","",
f"- Sanitários: {e['san']} UHC por pavimento; tubo de queda TQ-1 com {e['tq1']} UHC → DN 100, ventilação DN 75.",
f"- Esgoto de laboratório separado, em polipropileno: EL-A com {e['elA']} UHC e EL-B com {e['elB']} UHC → DN 100, com tanque de neutralização de 2 m³ em cada bloco.",
"- Subcoletores externos DN 150 com 1 % de declividade.","",
"## 7. Águas pluviais","",
f"- Área de cobertura: {f(calc.AREA_FLOOR,0)} m². Intensidade adotada: {p['i']:.0f} mm/h (valor de referência, a conferir na NBR 10844 para Recife).",
f"- Vazão: {p['q']:.0f} L/min, em {p['n']} condutores DN 150 ({p['q1']:.0f} L/min e {f(p['a1'],0)} m² cada).","",
"## 8. Incêndio","",
f"- Chuveiros automáticos, risco ordinário grupo 2: 8,1 mm/min sobre 140 m² = {i['spk']:.0f} L/min; {i['n_spk']} bicos por pavimento.",
f"- Reserva técnica: ({i['spk']:.0f} + {i['hose']:.0f}) L/min × {i['t']} min = {f(i['vol'],0)} m³ → adotado 130 m³.",
"- Três hidrantes por pavimento, mangueira de 40 mm × 30 m.",
"- Classificação de risco, densidades e reserva precisam ser confirmadas pelo projetista conforme o COSCIP-PE e a NBR 10897.","",
"## 9. O que ainda não existe","",
"- Projetos executivos (detalhamento de armaduras, isométricos, diagramas de quadros, detalhes construtivos, caderno de especificações e orçamento).",
"- Projetos de climatização e exaustão, gases, dados e automação, SPDA e paisagismo.",
"- Levantamento topográfico, sondagens e cadastro das redes do campus.",
"- Validação do programa com os grupos de pesquisa e lista real de equipamentos."]
open(OUT+"/memorial-de-calculo.md","w").write("\n".join(m)+"\n"); print(len(m))
