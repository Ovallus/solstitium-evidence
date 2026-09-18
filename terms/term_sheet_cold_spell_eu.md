# Term Sheet técnico — Cobertura / señal de *cold-spell* invernal (gas TTF, UE)

> **DR-3.4 · v0.1 · 2026-07-02.** Documento **firmable como piloto de invierno 2026-27** por una
> *utility* mediana o comercializadora de gas europea **sin desk cuant propio**. Es un term sheet
> técnico, no un contrato: fija problema, producto, evidencia con sus intervalos de confianza, diseño
> del índice, *basis risk*, settlement y pricing indicativo — todo lo que un *risk manager* de energía
> necesita para decidir un piloto de una temporada. Audiencia: *risk manager* de energía europeo.
>
> **Contrato de honestidad (el mismo del resto del repo):** cada número lleva su intervalo o su límite;
> ninguna cifra se infla; lo que el modelo NO explica se dice antes de que el lector lo calcule. La
> honestidad es el argumento de venta frente a vendedores de humo — un comité de riesgo la premia.
>
> **Materia prima (verificable en el repo):** `docs/ttf_squeeze_prototype.md` v0.1 (P(squeeze) TTF, GBM
> ex-guerra BSS +0.278) · `docs/wderivs_fixes_report.md` §9 (HDD/CDD OOS n=47, Wilson [51.7%, 77.8%]) ·
> `docs/verification_loop.md` (lección de *basis risk* geométrico, caso India) ·
> `docs/energy_eu_data_sources.md` (fuentes) · `docs/VISION_AND_CAPITAL.md` §4.1 (catálogo modelo C) ·
> `docs/ROADMAP_DEPLOYMENT_READY.md` §5 (dato vivo del storage). Método y cómputos puntuales en el
> **Anexo A**.

---

## 0. Resumen ejecutivo bilingüe (1 página) · Bilingual executive summary

### Español

Una comercializadora o *utility* de gas europea sufre un **doble golpe** en una ola de frío: la demanda
de calefacción (HDD) y el precio del gas TTF disparan **a la vez**, porque el mismo frío que sube el
consumo vacía los almacenamientos y tensa el precio. En diciembre de 2021, el pico de frío del invierno
(HDD población-ponderado UE = 17.4, el día más frío) cayó el **mismo día** que el pico de precio del
TTF de ese invierno (**180 €/MWh el 2021-12-21**), con los inventarios cayendo de 77% a 54% a 37% entre
noviembre y febrero. Quien compraba gas en el mercado ese día pagaba el precio más alto justo cuando más
volumen necesitaba. **El gancho de hoy:** el almacenamiento UE está en **49.07% al 30-jun-2026**, un
**−20.1 pp** por debajo de su mediana estacional de 5 años — el invierno 2026-27 arranca con el mismo
déficit que precede a los episodios de tensión.

Ofrecemos **dos productos sobre el mismo motor** (el partner elige uno o ambos):
- **(A) Señal / monitoreo de temporada:** P(cold-spell) y P(*squeeze* TTF) semanales, con el método
  versionado del repo (P(evento) diaria + GBM v0.1), entregadas como panel/API. Suscripción de temporada.
- **(B) Índice paramétrico:** HDD población-ponderado acumulado sobre umbral en una ventana invernal, con
  *payout* escalonado. El índice se define sobre las **mismas 7 ciudades y pesos** del forecast — no otro
  set — para que no haya *basis risk* geométrico (lección del caso India, §4).

**La evidencia, con sus intervalos impresos:** la señal HDD/CDD tiene **hit 66% sobre n=47** OOS (Wilson
95% **[51.7%, 77.8%]**, p=0.020) — el borde inferior **roza la moneda (51.7%)**, y lo decimos porque el
partner lo va a calcular igual. La señal de *squeeze* TTF tiene **BSS +0.278 ex-guerra** (ECE 0.053, bate
incluso al baseline de solo-almacenamiento) — **pero con el régimen de guerra 2022 incluido NO bate a
solo-almacenamiento**: el shock geopolítico no es nuestro *edge* y el producto lo excluye por diseño.

**Lo que NO prometemos:** el precio TTF que usamos hoy es de investigación (yfinance, TOS-gris) — el
settlement financiero requiere un feed licenciado, pendiente; arrancamos con **1 solo invierno** de
*forward record* real; la *feature* de almacenamiento tiene 5 años de historia. El piloto es una prueba
de una temporada, no un producto validado a escala.

**Pricing indicativo del piloto (1 invierno):** señal/monitoreo **€8.000–15.000 / temporada**; diseño +
settlement del índice paramétrico **€10.000–20.000 fee único** + **€3.000–6.000 / temporada** de
monitoreo en vivo. Sus datos históricos de consumo y coberturas **mejoran el pricing** (afinan el índice
a su libro) — es el *flywheel* de datos.

### English

A European gas *utility* or trader suffers a **double hit** in a cold spell: heating demand (HDD) and the
TTF gas price spike **simultaneously**, because the same cold that drives consumption drains storage and
tightens the price. In December 2021, the winter's coldest day (EU population-weighted HDD = 17.4) landed
on the **same day** as that winter's TTF price peak (**€180/MWh on 2021-12-21**), with inventories
falling 77% → 54% → 37% from November to February. Whoever bought gas that day paid the highest price
exactly when they needed the most volume. **The hook today:** EU storage sits at **49.07% on 2026-06-30**,
**−20.1 pp** below its 5-year seasonal median — winter 2026-27 opens with the same deficit that precedes
stress episodes.

We offer **two products on one engine** (partner picks one or both):
- **(A) Season signal / monitoring:** weekly P(cold-spell) and P(TTF squeeze), using the repo's versioned
  method (daily P(event) + GBM v0.1), delivered as dashboard/API. Season subscription.
- **(B) Parametric index:** population-weighted HDD accumulated over a threshold within a winter window,
  with a stepped payout. The index is defined on the **same 7 cities and weights** as the forecast — not
  a different set — so there is no geometric basis risk (India-case lesson, §4).

**The evidence, with its confidence intervals printed:** the HDD/CDD signal has a **66% hit over n=47**
OOS (Wilson 95% **[51.7%, 77.8%]**, p=0.020) — the lower bound **is close to a coin flip (51.7%)**, and we
say so because the partner will compute it anyway. The TTF squeeze signal has **BSS +0.278 ex-war** (ECE
0.053, beating even the storage-only baseline) — **but with the 2022 war regime included it does NOT beat
storage-only**: the geopolitical shock is not our edge, and the product excludes it by design.

**What we do NOT promise:** the TTF price we use today is research-grade (yfinance, grey TOS) — financial
settlement needs a licensed feed, still pending; we start with **one winter** of real forward record; the
storage feature has 5 years of history. The pilot is a one-season test, not a validated-at-scale product.

**Indicative pilot pricing (1 winter):** signal/monitoring **€8,000–15,000 / season**; parametric-index
design + settlement **€10,000–20,000 one-off** + **€3,000–6,000 / season** live monitoring. Your
historical consumption and hedging data **improve the pricing** (they tune the index to your book) — the
data flywheel.

---

## 1. El problema, con números

### 1.1 El doble golpe del *cold-spell*

Una comercializadora o *utility* con clientes de calefacción tiene una exposición **doblemente
convexa** al frío invernal:

1. **La cantidad sube:** una ola de frío eleva los *heating-degree-days* (HDD), y con ellos el volumen de
   gas que debe entregar a sus clientes (contratos de suministro, obligación de servicio, o cobertura de
   su propia cartera).
2. **El precio sube al mismo tiempo:** ese mismo frío —a menudo un régimen de NAO negativo, chorro
   bloqueado, poco viento— vacía los almacenamientos europeos y tensa el precio *front-month* del TTF.

Los dos efectos **no son independientes: están causalmente ligados y ocurren juntos.** El resultado es
que la utility necesita comprar **más** volumen justo cuando ese volumen cuesta **más** — la definición
de una exposición que un producto de cobertura debe atacar. La cadena física (peer-reviewed, *Energy
Economics*; ver `docs/energy_eu_data_sources.md`):

```
NAO− → frío + poco viento → HDD↑ → demanda↑ → storage draw↑ (AGSI+) ↘
                                                                     P(squeeze) TTF
```

### 1.2 El invierno 2021-22 como ilustración (datos reales del repo)

El invierno 2021-22 es el caso de manual del doble golpe. Con los datos del prototipo TTF y del índice
HDD población-ponderado UE (verificados en el Anexo A):

| Fecha | TTF *front-month* (€/MWh) | HDD pond. UE (diario) | Storage UE (% lleno) |
|---|---:|---:|---:|
| 2021-06-01 (verano) | 25.98 | 0 | — |
| 2021-09-01 | 50.23 | ~0 | — |
| 2021-10-01 | 108.19 (06-oct) | — | **74.9%** |
| 2021-12-01 | — | — | **67.2%** |
| **2021-12-21 (pico de frío del invierno)** | **180.27** | **17.4** (día más frío) | ~60% |
| 2022-01-01 | 80.43 (03-ene) | 16.4 (06-ene) | **53.8%** |
| 2022-02-01 | 134.32 (24-feb) | 13.3 (13-feb) | **37.2%** |
| 2022-03-01 | 227.20 (07-mar) | — | **28.7%** |

**La coincidencia es exacta y no es casualidad:** el día más frío del invierno (HDD 17.4 el 2021-12-21)
fue **el mismo día** del pico de precio del TTF de ese invierno (180 €/MWh). El almacenamiento cayó
monótonamente de 77% (nov) a 29% (mar) — un *storage draw* que amplificó cada nueva ola de frío. Una
utility que hubiera comprado su faltante de volumen en el mercado *spot* en diciembre pagó el precio más
alto por el mayor volumen: el doble golpe convertido en pérdida contable.

> *Nota honesta sobre 2022:* la escalada posterior (227 €/MWh en marzo, 339 €/MWh en agosto) ya está
> dominada por el **shock geopolítico** (guerra), no por el clima. Ese régimen NO es lo que este producto
> cubre ni lo que nuestra señal pretende explicar (§3.2). La ilustración del doble golpe **clima↔precio**
> es limpia hasta diciembre-2021; a partir de ahí interviene una causa que excluimos por diseño.

### 1.3 El gancho vivo: por qué el invierno 2026-27 merece cobertura

**El almacenamiento de gas de la UE está en 49.07% al 30-jun-2026** (dato en vivo, AGSI+ verificado —
`docs/ROADMAP_DEPLOYMENT_READY.md` §5). Contra su **mediana estacional de 5 años** para esa fecha del
calendario, eso es un **déficit de −20.1 pp** (recipe canónico del repo, reproducido en Anexo A). En
lenguaje llano: **Europa entra al invierno 2026-27 con los tanques ~20 puntos más vacíos de lo normal
para esta época** — exactamente el tipo de déficit que precede a los episodios de tensión (en 2021, la
UE también entró al invierno con inventarios por debajo de lo normal, y ese fue el detonante). Este es el
gancho de por qué **este** invierno merece que una utility ponga una cobertura antes de octubre, no
después.

---

## 2. Dos productos en uno (que el partner elija)

Ambos corren sobre el **mismo motor** de CausalQuant. El partner puede contratar uno, el otro, o los dos.

### 2.1 Producto (A): Señal / monitoreo de temporada — *suscripción*

**Qué entrega:** dos probabilidades calibradas, actualizadas **semanalmente** durante la temporada
(nov–mar), con el método **versionado y auditable** del repo:

- **P(cold-spell):** probabilidad de que el HDD población-ponderado UE (o de una región del partner)
  supere un umbral de frío en una ventana de 1–6 semanas. Producida por el pipeline de **P(evento)
  diaria** (`docs/verification_loop.md`, `pevent.v1`), donde **la definición del evento viaja con la
  probabilidad** (misma variable, umbral y dirección con que se verifica).
- **P(squeeze TTF):** probabilidad de que el TTF *front-month* suba **≥ +30% en las próximas ~3 semanas
  (15 días de negociación)**, producida por el **GBM v0.1** del prototipo TTF (`docs/ttf_squeeze_prototype.md`).

**Para qué le sirve al *risk manager*:** una lectura tipo "la P(squeeze) subió de 12% a 34% esta semana —
conviene cubrir/reasegurar YA". Es una señal de *timing* de cobertura, no una recomendación de trading.

**Diferenciador honesto:** nadie más ofrece **probabilidad calibrada en vivo** con historial de
calibración público (ECE) y verificación *rolling* contra observación independiente. No es una caja negra:
cada número trae su cadena causal y su registro de aciertos.

**Cómo se cobra:** **suscripción de temporada** (catálogo §4.1, producto #3 "monitoreo en vivo").

### 2.2 Producto (B): Índice paramétrico de *cold-spell* — *diseño + settlement*

**Qué entrega:** un instrumento paramétrico con *payout* determinista sobre un índice físico observable,
sin necesidad de ajustar pérdidas (*no loss adjustment*):

> **Índice = HDD población-ponderado acumulado por encima de un umbral, sobre una ventana invernal
> definida.** Concretamente, para una ventana \[nov 1 – mar 31\] y un umbral diario `H*`:
>
> `Index = Σ_ventana max(0, HDD_pond_UE(día) − H*)`
>
> El *payout* es **escalonado** (no lineal) sobre `Index`, para que el partner cobre proporcionalmente a
> la severidad acumulada del frío, con un techo (*cap*) que acota nuestra/su exposición.

**Diseño escalonado ilustrativo** (números indicativos, se calibran al libro del partner en el piloto):

| Tramo del índice (HDD-grados acumulados sobre umbral) | *Payout* (% del nocional) |
|---|---:|
| Índice ≤ percentil 50 histórico | 0% (invierno normal/templado) |
| Percentil 50 – 75 | 25% |
| Percentil 75 – 90 | 60% |
| Índice > percentil 90 (*cold-spell* severo) | 100% (*cap*) |

**La decisión de diseño clave (lección del caso India, §4):** el índice se define sobre las **MISMAS 7
ciudades y los MISMOS pesos** que usa el forecast de la señal — París, Londres, Milán, Madrid, Frankfurt,
Varsovia, Ámsterdam (pesos en `docs/energy_eu_data_sources.md` §5). **No** se define sobre otro set de
estaciones ni sobre una media nacional distinta. Esto elimina el *basis risk* geométrico: la cosa que
pronosticamos y la cosa que paga son **la misma variable, con la misma geometría** (ver §4 para por qué
esto importa tanto — lo aprendimos por las malas en el caso India).

**Cómo se cobra:** **fee único de diseño del índice** (catálogo §4.1, producto #1) + **fee de settlement
por vencimiento** (producto #4). El monitoreo en vivo del índice durante la vigencia es el producto (A).

### 2.3 Rol de las partes

> **Nota de encuadre (no es consejo legal).** Esta subsección describe el rol que Solstitium propone
> ocupar en la estructura, alineado con el estándar de mercado de bonos catastróficos y seguro
> paramétrico. Es preparación interna para discusión con el partner y con counsel, no una calificación
> jurídica definitiva: ver `docs/regulatory_role_2026-07.md` para el marco regulatorio completo
> (incluida la frontera seguro-vs-derivado UE/España que aplica directamente al producto B de esta
> sección) y su checklist de validación con abogado.

**Solstitium = calculation agent / index provider independiente.** Sin interés económico en el
resultado del gatillo, separados del *index sponsor* y del *risk carrier*:

- **Fuente de datos objetiva y reproducible:** el índice de HDD población-ponderado se calcula sobre
  reanálisis/observación **versionada** (hoy NASA POWER en investigación; el settlement contractual
  final requiere estaciones sinópticas oficiales de las 7 ciudades, §4.2), con la misma geometría
  (mismas ciudades, mismos pesos) que el forecast de la señal: nunca una fuente distinta a la que
  genera la probabilidad monitoreada.
- **Protocolo de disputa y fallback de datos:** el cálculo del índice se entrega con su cadena causal
  documentada para auditoría por el partner o un tercero; el mecanismo de resolución de disputas y el
  orden de prelación entre fuente primaria y fuente de respaldo (§4.2) se fijan en el contrato del
  piloto, no en este documento técnico.
- **Separación de roles:** Solstitium NO es el *index sponsor* ni el *risk carrier*. Es el estándar de
  *event agent* / *calculation agent* del mercado de *insurance-linked securities* (PCS en EE.UU./Japón,
  PERILS AG en Europa/Australia) y el rol que BIS/IAIS documentan como habilitado sin licencia
  aseguradora (FSI Insights No 62, bis.org/fsi/publ/insights62.htm, consultado 2026-07-04).
- **Relevancia directa para el producto (B) de esta sección:** la frontera seguro-vs-derivado (Swiss Re,
  *"10 myths about parametric insurance"*, corporatesolutions.swissre.com, consultado 2026-07-04:
  paramétrico puro sin prueba de pérdida tiende a derivado; estructura híbrida con condición
  indemnizatoria tiende a seguro) determina si el índice paramétrico de HDD (B) se estructura como
  instrumento financiero (MiFID II) o como seguro (IDD) en cada jurisdicción del partner: ver el
  semáforo completo en `docs/regulatory_role_2026-07.md`. El producto (A) señal/monitoreo no depende de
  esta calificación porque no paga un *payout*: es research/analytics.
- **La (re)aseguradora o utility-carrier = risk carrier.** El partner retiene el riesgo de suscripción o
  de balance según la estructura elegida (§5.2 de este documento ya lo dice: "no tomamos el riesgo;
  somos el *index provider* / *calculation agent*, no la aseguradora").

---

## 3. La evidencia, con sus intervalos de confianza impresos

Esta sección es deliberadamente cruda. Todos los números vienen de reportes de investigación versionados
en el repo, con TODAS las ventanas reportadas (no *cherry-picking*). Un cuant en *due diligence* los va a
auditar — nos adelantamos.

### 3.1 Señal de *cold-spell* (HDD/CDD): n=47, hit 66%, Wilson [51.7%, 77.8%]

Fuente: `docs/wderivs_fixes_report.md` §9 (expansión OOS DR-3.1). Metodología congelada, calibrador
re-entrenado por año \[1986, Y-1\] (anti-*leakage*), 5 ciudades EEUU, 7 inviernos (2019–2025):

| Métrica | Valor | Cómo leerlo |
|---|---|---|
| n (trades OOS) | **47** (subió desde n=5) | pequeño para estándar cuant, pero ya no anecdótico |
| Hit rate | **66.0%** (31/47) | dirección acertada 2 de cada 3 veces |
| **IC 95% Wilson** | **[51.7%, 77.8%]** | verificado con `statsmodels` (Anexo A) |
| Binomial p (H0: hit=50%) | **0.020** | estadísticamente distinguible de una moneda |
| P&L bootstrap (por bloque ciudad-año) | [+175, +3.369] pts | el borde inferior despeja cero |

**El *disclaimer* que el partner va a calcular igual, dicho por nosotros primero:** el borde inferior del
IC de Wilson es **51.7% — roza la moneda justa.** Con n=47 el intervalo mide **26 puntos de ancho**. Esto
es "razonablemente convincente", **no** "estadísticamente resuelto". La honestidad exacta: el *edge* de la
señal HDD **sobrevive** la expansión de n=5 a n=47 (el borde bajo despejó 50% por primera vez, la
concentración del P&L en un solo *trade* cayó de 79% a 11.7%, las 5 ciudades tienen *edge* individual
positivo), pero **no está a nivel de un producto validado a escala.** Un piloto de una temporada es
exactamente el instrumento correcto para una señal en este estado de madurez.

### 3.2 Señal de *squeeze* TTF: BSS +0.278 ex-guerra, ECE 0.053 — y el límite explícito de 2022

Fuente: `docs/ttf_squeeze_prototype.md` v0.1 (DR-3.2b, storage en vivo). Evento primario = **+30% en 15
días de negociación** (base rate ex-guerra ≈ 11%). Walk-forward bloqueado, 5 folds, 6 features causales:

| Modelo · Régimen | BSS vs climatología | BSS vs solo-almacenamiento | ECE |
|---|---:|---:|---:|
| **GBM · ex-guerra** | **+0.278** ✅ | **+0.197** ✅ | **0.053**\* |
| GBM · full (incl. 2022) | +0.132 | **−0.020** ⚠️ | 0.037 |

\* *ECE 0.053 es la cifra citada en el registro del roadmap (`ROADMAP_DEPLOYMENT_READY.md` §5) para el
prototipo TTF; el reporte v0.1 desglosa ECE por celda régimen×evento entre 0.037 y 0.044. Ambos indican
un modelo bien calibrado. Se usa 0.053 como la cifra conservadora de referencia del producto.*

**Lo que esto significa, sin adornos:**
- **Ex-guerra (régimen normal), el GBM añade *skill* calibrado real:** bate a "¿qué época del año es?"
  (climatología) por BSS +0.278, y —lo nuevo y más fuerte— **bate al propio nivel de almacenamiento**
  (BSS +0.197). Es decir, el modelo no se limita a repetir lo que un trader ya ve mirando AGSI+; combina
  almacenamiento con clima y momentum en algo mejor que cualquiera de los dos por separado.
- **Con el régimen de guerra 2022 incluido, el modelo NO bate a solo-almacenamiento** (BSS −0.020). Esto
  se dice explícitamente porque es la verdad: en 2022 el *shock* geopolítico se transmitió en gran parte
  *a través* del propio nivel de almacenamiento (los tanques se vaciaron por la crisis), así que un solo
  número de storage ya captura casi todo. **El régimen geopolítico no es nuestro *edge*, y el producto lo
  excluye por diseño** (la señal se entrega y se evalúa sobre el régimen impulsado por fundamentales, no
  sobre el *tail* de guerra).
- **Dónde confiar y dónde no:** la P(squeeze) es fiable en el rango 0–0.4 (bien calibrada, donde cae la
  mayoría de la masa OOS); por encima de 0.4 sigue siendo ruidosa, y el *bin* de alarma alto (0.6–0.8)
  todavía es fino y sobre-confiado. Se comunica como probabilidad calibrada del **estado común**, no como
  un oráculo de la cola extrema.

### 3.3 Calibración auditable en vivo (el diferenciador)

El *verification loop* (`docs/verification_loop.md`) puntúa cada P(evento) contra observación
independiente (NASA POWER, lag 3d) con **la propia definición del evento**, acumula Brier/reliability, y
lo publica en el modal "Calibration" del dashboard. El modal ya corre sobre datos reales (n=42
verificaciones: helada Brasil BSS +0.64 vs ERA5; ola de calor India BSS −0.155 vs obs puntual; este
último negativo es, precisamente, la lección de *basis risk* que estructura el §4). Para el partner:
**el historial de calibración es *rolling* y auditable en el repo, no una promesa** (la publicación web
formal del récord está diferida hasta congelar el universo v1; se enseña en vivo en cualquier demo).

---

## 4. *Basis risk* y settlement

El *basis risk* —que el partner sufra el frío pero el índice no dispare, o al revés— es el riesgo #1 de
todo producto paramétrico. Lo atacamos con una decisión de diseño y una fuente de settlement explícita.

### 4.1 La lección del caso India: la geometría del settlement debe casar con la del forecast

En el *verification loop* del repo (`docs/verification_loop.md`), la ola de calor de India (mar-2022)
salió con **BSS negativo (−0.155)** — no porque el forecast fallara, sino por un **desajuste geométrico**:
el forecast era un **máximo regional** ("hace calor en la región"), pero la observación de settlement era
un **punto** (el centroide), que leyó justo por debajo del umbral de 38°C en varios días donde el máximo
regional decía "caliente". Textbook *basis risk* entre una obs puntual y un forecast de extremo regional.

**La consecuencia de diseño para este term sheet, adoptada explícitamente:** el índice de *cold-spell* se
define sobre **exactamente la misma variable y geometría que el forecast** — el HDD población-ponderado
sobre **las mismas 7 ciudades y los mismos pesos** (§2.2). No pronosticamos una cosa y liquidamos sobre
otra. Esto no elimina el *basis risk* frente al consumo real del partner (§4.3), pero **elimina el
*basis risk* geométrico interno** entre señal e índice — el error que nos costó BSS negativo en India.

### 4.2 Fuente de settlement propuesta y su *mismatch* cuantificado

| Componente | Fuente en el prototipo (research) | Fuente propuesta para settlement (piloto) | *Mismatch* a cuantificar |
|---|---|---|---|
| **Temperatura → HDD** | NASA POWER T2M (satélite, grilla ~50 km) | **Estaciones sinópticas oficiales** de las 7 ciudades (p.ej. red nacional/WMO por ciudad) | NASA/ERA5 vs estación sinóptica: sesgo por ciudad, a medir como en el caso India |
| **Precio TTF** (solo producto A) | yfinance `TTF=F` (TOS-gris) | **Feed licenciado / settlement oficial ICE/EEX** (pendiente, §6) | roll de continuo vs *settlement* oficial |

**El *mismatch* se cuantifica, no se esconde:** antes de firmar el settlement final, se mide el sesgo
NASA-POWER-vs-estación-sinóptica por cada una de las 7 ciudades sobre el histórico disponible (mismo
método diagnóstico que expuso el caso India), y se documenta en el anexo del piloto. La calibración del
repo ya muestra que NASA POWER reconstruye HDD oficial dentro de **~2.7–2.9% de MAPE en meses de
contrato** para ciudades bien cubiertas (`docs/wderivs_fixes_report.md` §4) — buena señal, pero se
re-verifica sobre las estaciones sinópticas europeas concretas del piloto.

### 4.3 Expectil como objetivo de diseño del índice

El objetivo de estructuración **no es el valor esperado (media)** del *payout*, sino un **expectil** de la
distribución de pérdidas del partner — el mismo objetivo que en el term sheet de helada de café. Un
expectil pondera asimétricamente la cola adversa (el *cold-spell* severo que de verdad duele), de modo que
el índice y su *payout* se ajusten a **reducir el *basis risk* donde el partner más lo siente** (los años
malos), no a minimizar el error promedio en años normales. En el piloto, el expectil objetivo se fija con
los datos históricos de consumo/pérdidas del partner (§5.3).

---

## 5. Pricing indicativo del piloto

Según el catálogo del modelo C (`docs/VISION_AND_CAPITAL.md` §4.1) y la matemática de *burn* del piloto
(§5.2 del mismo doc: un *design partner* pagando $3–10k/mes cubre el *burn lean*). Cifras **para un piloto
de 1 invierno**, en un rango defendible — no precios de lista de un producto maduro.

### 5.1 Números concretos

| Componente | Catálogo §4.1 | Fee indicativo (piloto, 1 invierno) |
|---|---|---|
| **(A) Señal / monitoreo de temporada** | #3 monitoreo en vivo (suscripción) | **€8.000 – €15.000 / temporada** |
| **(B1) Diseño del índice paramétrico** | #1 diseño de índice/trigger (fee único) | **€10.000 – €20.000** (fee único) |
| **(B2) Settlement (*calculation agent*)** | #4 settlement (fee por vencimiento) | **€2.000 – €4.000 / vencimiento** |
| **(B3) Monitoreo en vivo del índice** | #3 (suscripción durante vigencia) | **€3.000 – €6.000 / temporada** |
| **Paquete completo (A + B), piloto 1 invierno** | — | **≈ €20.000 – €40.000** |

Referencia de rango: el paquete completo se sitúa dentro del **$3–10k/mes** que la tesis de capital fija
como el *design partner* que cubre el *burn* (≈ €20–40k por una temporada de ~5 meses). El extremo bajo es
un piloto de solo-señal; el alto, señal + índice paramétrico diseñado y liquidado.

### 5.2 Qué NO incluye el fee del piloto

El fee del piloto **no** incluye la prima del instrumento paramétrico en sí (el nocional que el partner
decida cubrir es aparte y depende de su exposición), ni el coste de un feed de precio licenciado si el
partner exige settlement financiero sobre TTF en el producto (A) (§6). El piloto cobra **el número y su
defensa** —diseño, calibración, monitoreo, settlement del índice físico— no el riesgo de balance (no
tomamos el riesgo; somos el *index provider* / *calculation agent*, no la aseguradora).

### 5.3 El *flywheel*: qué datos del partner mejoran el pricing

Si el partner comparte, bajo NDA, sus **datos históricos de consumo por zona** y sus **coberturas
pasadas** (o pérdidas atribuibles a *cold-spells*), podemos:
1. **Afinar el índice a su libro real:** re-pesar las 7 ciudades hacia su huella de demanda concreta (en
   vez de los pesos poblacionales genéricos), reduciendo el *basis risk* frente a **su** consumo (§4.3).
2. **Fijar el expectil objetivo con su distribución de pérdidas real**, no con un supuesto genérico.
3. **Estrechar el pricing:** con la distribución de pérdidas del partner, la prima sugerida y los tramos
   del *payout* se calibran a datos, no a percentiles genéricos.

Este intercambio —datos por mejor pricing— es el *flywheel* del modelo C: cada piloto nos da datos de
pérdidas/consumo que nadie más tiene, lo que mejora el *basis risk* y el pricing del siguiente. Es un moat
que sale del modelo de negocio, sin capex.

---

## 6. Lo que NO prometemos (límites, dichos en voz alta)

La honestidad ES el argumento de venta. Estos son los límites reales del producto en su estado de v0.1:

1. **Feed de precio licenciado pendiente (para settlement financiero).** El precio TTF que usamos hoy es
   **yfinance `TTF=F`, de TOS-gris** — válido para *research* y para la **señal** (P(squeeze)), pero **no**
   para liquidar dinero sobre TTF. Un settlement financiero referenciado a TTF requiere un **feed
   licenciado / settlement oficial ICE/EEX**, que aún no tenemos (roadmap DR-0.2). *Mitigación de diseño:*
   el **índice paramétrico (B) liquida sobre HDD** (temperatura de estaciones oficiales), que **no**
   depende de un feed de precio licenciado — el producto que puede firmarse y liquidarse hoy es el índice
   de temperatura, no un derivado financiero sobre el precio del gas.
2. **1 solo invierno de *forward record* al arrancar.** El *shadow record* en GitHub Actions corre a
   diario con *timestamp* de tercero (prueba de no-*look-ahead*), pero al iniciar el piloto tenemos **un
   invierno** de registro *forward* real, no diez. La evidencia dura de largo plazo es el walk-forward OOS
   (§3), no un track *forward* multi-anual — ese se construye **con** el piloto.
3. **La *feature* de almacenamiento tiene 5 años de historia.** `storage_deficit` (AGSI+) cubre
   2019–2026 (~7.5 años de dato, pero el régimen útil ex-guerra es más corto). Es la *feature* más fuerte
   de la señal TTF (§3.2), pero su historia es de años, no de décadas — los intervalos de la señal TTF lo
   reflejan.
4. **n=47 en la señal HDD, borde inferior 51.7%** (§3.1) — repetido aquí porque es el límite estadístico
   central: "razonablemente convincente", no "resuelto".
5. **El régimen geopolítico está fuera de alcance por diseño** (§3.2). Si el invierno 2026-27 trae un
   *shock* de oferta tipo 2022, la señal de *squeeze* **no** lo pretende pronosticar — cubre el canal
   clima↔almacenamiento↔precio en régimen normal, no el *tail* geopolítico.

---

## Anexo A — Método y cómputos puntuales

Todos los cómputos de este anexo son **puntuales, ejecutados fuera del repo** (en `/tmp`), reutilizando el
dato ya cacheado del repo y el código versionado existente — **sin código nuevo** en el árbol. Se listan
para que un tercero los reproduzca.

### A.1 Dato vivo del almacenamiento y `storage_deficit` (−20.1 pp)

- **Fuente:** caché AGSI+ EU `data/energy_eu/agsi/eu_2019-01-01_2026-07-02.json` (2738 lecturas diarias,
  2019-01-01 → 2026-06-30, cero *gaps*). Campo `full` = % lleno; `gasDayStart` = fecha del día de gas.
- **Verificado:** `full = 49.07%` en `gasDayStart = 2026-06-30` (coincide con el dato vivo del founder).
- **`storage_deficit` — recipe canónico** (reproducido de `causalquant/verticals/energy/ttf_squeeze.py`
  `load_storage_deficit`): mediana estacional por día-del-año (*leap-safe*, todos los años), suavizada 15
  días; `deficit = fill − seasonal`. Resultado: **`storage_deficit(2026-06-30) = −20.13 pp`**; serie
  completa: media −0.81 pp, mediana +0.06 pp, n=2738 — **idéntico** a `docs/ttf_squeeze_prototype.md` §1.

### A.2 Ilustración del invierno 2021-22 (§1.2)

- **TTF:** caché `data/energy_eu/ttf/TTF_F_2019-01-01_2026-07-02.csv` (columnas `date`, `ttf_close`).
  Valores citados verificados: 25.98 (2021-06-01), 50.23 (2021-09-01), 108.19 (2021-10-06), **180.27
  (2021-12-21)**, 80.43 (2022-01-03), 134.32 (2022-02-24), 227.20 (2022-03-07), 339.20 (2022-08-26, pico
  de la crisis, coincide con el registro público).
- **HDD población-ponderado UE:** caché
  `data/energy_eu/hdd_eu/eu_hdd_population_weighted_20190101_20260702.csv` (columna `HDD_eu_weighted`).
  Invierno 2021-22: **máximo diario 17.4 el 2021-12-21** (el día más frío), media 13.0. La coincidencia
  del pico de HDD (2021-12-21) con el pico de TTF de ese invierno (2021-12-21, 180.27 €/MWh) es exacta.
- **Storage 2021-22:** de la misma caché AGSI+: 74.9% (oct-1) → 67.2% (dic-1) → 53.8% (ene-1) → 37.2%
  (feb-1) → 28.7% (mar-1) — *draw* monótono verificado.
- **Episodios +30%/15td en el invierno 2021-22:** 66 de 132 días de negociación de la ventana
  \[sep-2021, mar-2022\] tenían un *run-up* forward de +30% en 15 días (base rate altísima del régimen de
  crisis) — coherente con que 2022 es el *outlier* que el producto excluye por diseño.

### A.3 Evidencia de las señales (§3) — citas verificadas al repo

- **HDD/CDD:** n=47, hit 66% (31/47), Wilson95 [51.7%, 77.8%] (verificado con
  `statsmodels.stats.proportion.proportion_confint(method='wilson')`), p=0.020 (verificado con
  `scipy.stats.binomtest`), P&L bootstrap [+175, +3.369] pts — todo de `docs/wderivs_fixes_report.md` §9,
  reproducible con `scripts/wderivs_expanded_oos.py`.
- **TTF *squeeze*:** GBM ex-guerra BSS +0.278 vs climatología, +0.197 vs solo-almacenamiento; full-sample
  BSS −0.020 vs solo-almacenamiento (NO bate); ECE 0.053 (cifra de referencia del roadmap) — de
  `docs/ttf_squeeze_prototype.md` §5, reproducible con `scripts/ttf_squeeze_replay.py`.
- **Calibración en vivo:** n=42 verificaciones, Brasil BSS +0.64, India BSS −0.155 (*basis risk*
  geométrico) — de `docs/verification_loop.md`, reproducible con `scripts/verify_pevent.py`.

### A.4 Las 3 decisiones de diseño clave (resumen para el registro)

1. **El índice se define sobre las MISMAS 7 ciudades/pesos que el forecast** (§2.2, §4.1) — para eliminar
   el *basis risk* geométrico que hundió el BSS de India.
2. **El régimen de guerra 2022 se excluye por diseño** (§3.2) — la señal cubre el canal clima↔precio en
   régimen normal (donde bate incluso a solo-almacenamiento), no el *tail* geopolítico (donde no lo bate,
   y lo decimos).
3. **El producto firmable/liquidable hoy es el índice paramétrico de HDD (temperatura), no un derivado
   financiero sobre TTF** (§6) — porque el settlement de temperatura no depende del feed de precio
   licenciado que aún está pendiente; la señal de precio se vende como monitoreo, no como base de
   liquidación.

### A.5 Análisis de cola por teoría de valores extremos (EVT)

Sobre el índice de HDD población-ponderado UE (mismas 7 ciudades y pesos del forecast, 7 inviernos
2019-2026 de la caché del repo) se ajusta la cola superior con GEV sobre picos diarios anuales y GPD
sobre excedencias diarias (umbral por mean-residual-life + estabilidad, QQ de ajuste 0.994). El parámetro
de forma es **xi = -0.30, IC95 [-0.49, -0.20]** (vía GPD): la cola del HDD diario está **acotada** (techo
físico). Los **niveles de retorno** del HDD diario ponderado son 20.3 a 5 años, 20.8 a 25 años y **21.1 a
100 años (IC95 GPD [20.0, 22.0])**. **Nota metodológica honesta, coherente con el límite de "1 solo
invierno de forward record" del cuerpo del documento:** con n=7 inviernos la vía de máximos anuales (GEV)
es apenas identificable (su intervalo de 100 años es inutilizablemente ancho, [19.2, 91.2]) mientras la
vía de excedencias diarias (159 excedencias, GPD) mantiene el intervalo ajustado; por eso la GPD-POT es
la lectura de cola que este anexo reporta como fiable. Para el payout escalonado, el índice acumulado
`Sum max(0, HDD_dia - 12)` por invierno tiene percentiles históricos p50 = 222, p75 = 234, p90 = 265
HDD-grados (los tramos de payout se anclan a estos percentiles; indicativos con n=7, se estrechan con el
flywheel). Reproducible: `scripts/evt_term_sheets.py`.

### A.6 Basis risk descompuesto (los tres componentes con número)

Reproducible en `causalquant/actuarial/basis_risk.py`: **(1) SPATIAL** = distancia settlement-exposición.
Como el índice se define sobre las mismas 7 ciudades y pesos que el forecast, el basis geométrico interno
es ~0 por construcción (no se pronostica una cosa y se liquida otra); el residual espacial es el mismatch
reanálisis-vs-estación sinóptica al liquidar sobre estaciones oficiales, con MAPE del HDD ~2.8 % (peor
ciudad 2.9 %). **(2) TEMPORAL** = desajuste ventana-vs-daño. La ventana 1-nov a 31-mar cubre el pico de
HDD de los 7 inviernos 2019-2026 (todos en dic/ene/feb): 0 % de eventos fuera de ventana. **(3) DESIGN** =
no-linealidad no capturada. El payout escalonado por percentiles 50/75/90 captura R2=0.60 del
HDD-acumulado (el driver de volumen); el 40 % restante viene de discretizar un índice continuo en solo 3
tramos, y se reduce añadiendo cortes o pasando a un payout lineal por tramos. **Diagnóstico honesto:** con
la discretización actual y n=7, el R2 del cuerpo (0.60) no cruza la regla de mercado de 0.70, pero la cola
sí se ajusta (distancia 0.08) y subir el número de tramos cruza el umbral. Decimos dónde falla y cómo
subirlo, que es lo que distingue a un index quality vendor de una caja negra.

---

*Este term sheet es un documento técnico de piloto, confidencial para el *design partner*, preparado por
Solstitium (motor CausalQuant). Fundador: Juan Esteban Ovalle. Los resultados de backtest son
out-of-sample walk-forward y no garantizan resultados futuros; las capas nuevas (señal TTF, expansión
HDD) son investigación en curso reportada con TODAS sus ventanas e intervalos. No tomamos riesgo de
balance: actuamos como *index provider* / *calculation agent*, no como aseguradora.*
