# Memorial descritivo e de cálculo — anteprojeto

Reconstrução do bloco de laboratórios da UFPE (Campus Recife). Revisão R00, 22/11/2026.

> **Alcance.** Este caderno é um anteprojeto gerado sem visita, levantamento topográfico, sondagem ou cadastro de redes. Os cálculos são pré-dimensionamentos por índices e métodos simplificados. Não substitui os projetos legais e executivos, que precisam de responsáveis técnicos habilitados (RRT/ART) e de aprovação no Corpo de Bombeiros (COSCIP-PE), na Prefeitura e na concessionária.

## 1. Lista de pranchas

| Prancha | Conteúdo | Escala |
|---|---|---|
| ARQ-01 | Arquitetura - implantacao esquematica | 1:500 |
| ARQ-02 | Arquitetura - planta do terreo | 1:200 |
| ARQ-03 | Arquitetura - planta do 1o pavimento | 1:200 |
| ARQ-04 | Arquitetura - planta do 2o pavimento | 1:200 |
| ARQ-05 | Arquitetura - planta de cobertura | 1:200 |
| ARQ-06 | Arquitetura - cortes AA e BB | 1:200 |
| ARQ-07 | Arquitetura - fachadas norte e sul | 1:200 |
| DET-01 | Detalhe - modulo-tipo de laboratorio | 1:50 |
| EST-01 | Estrutura - pilares e forma do pavimento-tipo | 1:200 |
| HID-01 | Hidraulica - agua fria e esquema vertical | 1:200 |
| HID-02 | Hidraulica - esgoto - terreo e rede externa | 1:200 |
| HID-03 | Hidraulica - aguas pluviais e barrilete | 1:200 |
| INC-01 | Incendio - sprinklers, hidrantes e saidas - pav. tipo | 1:200 |
| ELE-01 | Eletrica - diagrama unifilar geral e quadro de cargas | 1:200 |
| ELE-02 | Eletrica - iluminacao e quadros - pavimento-tipo | 1:200 |

Cada prancha existe em PDF (`pdf/`) e em DXF (`dxf/`, em metros, para AutoCAD, BricsCAD, QCAD ou LibreCAD). O arquivo `caderno-de-projetos.pdf` reúne todas.

## 2. Arquitetura

- Barra de 108,00 × 21,60 m entre eixos, térreo mais dois pavimentos e cobertura técnica; área construída de 3 × 2.358,8 = 7.076 m² pelas faces externas (6.998 m² pelos eixos).
- Malha de 15 vãos de 7,20 m; faixas de 9,60 m (sul, laboratórios), 2,40 m (corredor) e 9,60 m (norte, permanência).
- Níveis: térreo +1,20; 1º pavimento +5,70; 2º pavimento +10,20; cobertura +14,70. Piso a piso 4,50 m, pé-direito livre 3,20 m.
- Dois blocos de 50,40 m e núcleo central de 7,20 m, separados por juntas de dilatação que coincidem com as barreiras corta-fogo.
- Três escadas enclausuradas (E1, E2, E3), dois elevadores, sanitários e shafts em todos os pavimentos.
- Quadros de áreas e de acabamentos por ambiente nas pranchas ARQ-02 a ARQ-04.

## 3. Estrutura (pré-dimensionamento)

- Concreto armado, fck 35 MPa, classe de agressividade III; pilares 40 × 70 cm; laje nervurada de 35 cm.
- Cargas: permanente 7,5 kN/m², sobrecarga 5,0 kN/m².
- Pilar interno: 43,2 m² × 4 lajes × 12,5 kN/m² = 2160 kN em serviço; Nd = 3024 kN, contra 0,85·fcd·Ac = 5950 kN (aproveitamento de 51 %, sem contar armadura nem flexão).
- Pilar de fachada: 34,6 m² × 4 lajes → 1728 kN em serviço.
- Fundações previstas em estacas hélice contínua; diâmetro e profundidade dependem de sondagem SPT.

## 4. Elétrica

Tensão 380/220 V, esquema TN-S. Corrente = demanda ÷ (√3 × 380 V × 0,92). Disjuntor ≥ 1,25 × corrente. Cabo de cobre EPR em bandeja, fator de agrupamento 0,80.

| Quadro | Carga | Instalada (kW) | F.D. | Demanda (kW) | I (A) | Disjuntor (A) | Alimentador (mm²) | Barra |
|---|---|---:|---:|---:|---:|---:|---|---|
| QDL-TA | Equipamentos de laboratorio (3 modulos x 300 W/m2) | 62,2 | 0,40 | 24,9 | 41 | 63 | 3#16+N+T | Normal |
| QDL-TB | Equipamentos de laboratorio (2 modulos x 300 W/m2) | 41,5 | 0,40 | 16,6 | 27 | 40 | 3#16+N+T | Normal |
| QDL-1A | Equipamentos de laboratorio (7 modulos x 300 W/m2) | 145,2 | 0,40 | 58,1 | 96 | 125 | 3#35+N+T | Normal |
| QDL-1B | Equipamentos de laboratorio (4 modulos x 300 W/m2) | 82,9 | 0,40 | 33,2 | 55 | 80 | 3#16+N+T | Normal |
| QDL-2A | Equipamentos de laboratorio (7 modulos x 300 W/m2) | 145,2 | 0,40 | 58,1 | 96 | 125 | 3#35+N+T | Normal |
| QDL-2B | Equipamentos de laboratorio (4 modulos x 300 W/m2) | 82,9 | 0,40 | 33,2 | 55 | 80 | 3#16+N+T | Normal |
| QDI-TA | Iluminacao (7 W/m2 normal) + tomadas de uso geral (25 W/m2) | 37,3 | 0,61 | 22,7 | 38 | 50 | 3#16+N+T | Normal |
| QDI-TB | Iluminacao (7 W/m2 normal) + tomadas de uso geral (25 W/m2) | 37,3 | 0,61 | 22,7 | 38 | 50 | 3#16+N+T | Normal |
| QDI-1A | Iluminacao (7 W/m2 normal) + tomadas de uso geral (25 W/m2) | 37,3 | 0,61 | 22,7 | 38 | 50 | 3#16+N+T | Normal |
| QDI-1B | Iluminacao (7 W/m2 normal) + tomadas de uso geral (25 W/m2) | 37,3 | 0,61 | 22,7 | 38 | 50 | 3#16+N+T | Normal |
| QDI-2A | Iluminacao (7 W/m2 normal) + tomadas de uso geral (25 W/m2) | 37,3 | 0,61 | 22,7 | 38 | 50 | 3#16+N+T | Normal |
| QDI-2B | Iluminacao (7 W/m2 normal) + tomadas de uso geral (25 W/m2) | 37,3 | 0,61 | 22,7 | 38 | 50 | 3#16+N+T | Normal |
| QF-AC | Central de agua gelada / climatizacao (aprox. 360 TR) | 395,0 | 0,90 | 355,5 | 587 | 800 | 2x3#240+N+T | Normal |
| QF-VENT | Ventiladores de insuflamento | 40,0 | 0,90 | 36,0 | 59 | 80 | 3#16+N+T | Normal |
| QF-ELEV1 | Elevador social | 15,0 | 0,50 | 7,5 | 12 | 32 | 3#16+N+T | Normal |
| QDE-ILUM | Iluminacao de emergencia e seguranca (2 W/m2) | 14,0 | 1,00 | 14,0 | 23 | 32 | 3#16+N+T | Emergência |
| QDE-EXA | Exaustao das capelas e salas NB-2 | 50,0 | 0,90 | 45,0 | 74 | 100 | 3#25+N+T | Emergência |
| QDE-ACC | Climatizacao de precisao (data center e biorrepositorios) | 44,0 | 0,90 | 39,6 | 65 | 100 | 3#25+N+T | Emergência |
| QDE-FRZ | Ultrafreezers e camaras frias (40 un. x 1,2 kW) | 48,0 | 1,00 | 48,0 | 79 | 100 | 3#25+N+T | Emergência |
| QDE-DC | Data center via no-break de 80 kVA | 60,0 | 1,00 | 60,0 | 99 | 125 | 3#35+N+T | Emergência |
| QDE-ELEV2 | Elevador de emergencia / macas | 15,0 | 1,00 | 15,0 | 25 | 32 | 3#16+N+T | Emergência |
| QDE-BOMB | Bombas de agua fria e de drenagem | 20,0 | 0,50 | 10,0 | 17 | 32 | 3#16+N+T | Emergência |
| **Total** | | **1485** | | **991** | | | | |

- Demanda total: 991 kW = 1077 kVA.
- Subestação: 2 transformadores a seco de 750 kVA (carregamento de 72 %); corrente nominal de 1140 A por transformador.
- Cargas de emergência: 232 kW = 290 kVA → gerador a diesel de 450 kVA.
- Iluminação: 500 lux em laboratórios e salas, com 18 painéis LED de 40 W por módulo de 69 m² (10,4 W/m²).
- Falta verificar queda de tensão, curto-circuito e seletividade.

## 5. Água fria

- População de cálculo: 600 pessoas. Consumo: 600 × 50 L + 10 m³ de processo = 40 m³/dia.
- Reserva de 1,5 dia: 60 m³ (36 m³ no reservatório inferior e 24 m³ no superior).
- Vazões pelo método dos pesos, Q = 0,3·√ΣP (L/s), com velocidade máxima de 1,5 m/s.

| Trecho | Soma de pesos | Vazão (L/s) | Tubo PVC (DE mm) | Velocidade (m/s) |
|---|---:|---:|---:|---:|
| AF-1 (sanitarios) | 16,5 | 1,22 | 40 | 1,25 |
| AF-2 (laboratorios bloco A) | 26,6 | 1,55 | 50 | 1,02 |
| AF-3 (laboratorios bloco B) | 15,4 | 1,18 | 40 | 1,21 |
| Barrilete / saida do reservatorio | 58,5 | 2,29 | 60 | 1,02 |

## 6. Esgoto

- Sanitários: 61 UHC por pavimento; tubo de queda TQ-1 com 122 UHC → DN 100, ventilação DN 75.
- Esgoto de laboratório separado, em polipropileno: EL-A com 84 UHC e EL-B com 60 UHC → DN 100, com tanque de neutralização de 2 m³ em cada bloco.
- Subcoletores externos DN 150 com 1 % de declividade.

## 7. Águas pluviais

- Área de cobertura: 2333 m². Intensidade adotada: 150 mm/h (valor de referência, a conferir na NBR 10844 para Recife).
- Vazão: 5832 L/min, em 14 condutores DN 150 (417 L/min e 167 m² cada).

## 8. Incêndio

- Chuveiros automáticos, risco ordinário grupo 2: 8,1 mm/min sobre 140 m² = 1134 L/min; 210 bicos por pavimento.
- Reserva técnica: (1134 + 950) L/min × 60 min = 125 m³ → adotado 130 m³.
- Três hidrantes por pavimento, mangueira de 40 mm × 30 m.
- Classificação de risco, densidades e reserva precisam ser confirmadas pelo projetista conforme o COSCIP-PE e a NBR 10897.

## 9. O que ainda não existe

- Projetos executivos (detalhamento de armaduras, isométricos, diagramas de quadros, detalhes construtivos, caderno de especificações e orçamento).
- Projetos de climatização e exaustão, gases, dados e automação, SPDA e paisagismo.
- Levantamento topográfico, sondagens e cadastro das redes do campus.
- Validação do programa com os grupos de pesquisa e lista real de equipamentos.
