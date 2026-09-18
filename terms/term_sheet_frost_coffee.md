# Term Sheet Técnico — Cobertura Paramétrica de Helada para Café

**Producto #1+#2 del catálogo Solstitium/CausalQuant (modelo C: infraestructura de riesgo paramétrico)**
Diseño de índice/trigger + pricing calibrado · cafeicultores y cooperativas · Colombia (eje cafetero) / Brasil (cinturón Minas–São Paulo–Paraná)

> **v1.0 · 2026-07-02 · DR-3.3.** Documento técnico para un *design partner* (aseguradora, MGA o
> reasegurador con apetito LATAM-agro — p. ej. perfiles tipo Blue Marble, Raincoat). **No es
> marketing:** es una especificación de índice con números, honesta sobre lo que la evidencia actual
> soporta y lo que todavía no. El objetivo del piloto es co-diseñar y firmar la estructura de abajo,
> no comprar una predicción.
>
> **Qué es Solstitium en una línea:** convertimos física del clima en **probabilidades calibradas y
> auditables** para decisiones financieras. No vendemos "va a helar"; vendemos "P(helada) = 0.34, con
> este historial de calibración contra resultados reales", y la defensa causal y reproducible de ese
> número.
>
> **Alcance de esta v1.0.** Priorizamos el **cinturón brasileño** (donde tenemos hindcast verificado y
> climatología reproducible) como piloto ancla, y tratamos **Colombia** como extensión con una salvedad
> geométrica explícita (§1.5, §5). Todos los números de pricing de §3 son **indicativos** y llevan un
> factor de prudencia explícito por tamaño muestral pequeño.

---

## 0. Resumen ejecutivo (para el comité de riesgo)

| Elemento | Propuesta |
|---|---|
| **Peligro cubierto** | Helada radiativa nocturna sobre café arábica en invierno austral (jun–ago). |
| **Variable del índice** | T2M mínima diaria (temperatura del aire a 2 m), agregada como **mínimo espacial regional** sobre una caja de producción definida — **no** un punto de estación aislado (§1.5, la lección central). |
| **Fuente de settlement** | Reanálisis oficial acordado (ERA5 / ERA5-Land como candidato primario; estación oficial IDEAM/INMET o LST satelital nocturno como cross-check), con geometría **idéntica** a la del monitoreo. |
| **Umbrales (agronómicos)** | Escalonado: **< 4 °C** (daño de hoja incipiente) → **< 2 °C** (helada operativa, daño foliar cierto) → **< 0 °C** (helada letal / muerte de tejido). §1.3. |
| **Estructura de payout** | **Escalonada** (tramos), no binaria — minimiza *basis risk* y alinea el pago con la severidad física. §1.4. |
| **Ventana de cobertura** | 1 jun – 31 ago (invierno austral, hemisferio sur). §1.6. |
| **Evidencia de skill** | Hindcast Brasil-2021 verificado contra verdad ERA5: **BSS +0.64** en helada (n=12), heladas de Paraná/SP detectadas 1–4 días antes. §3, Anexo. |
| **Monitoreo en vivo** | P(helada) diaria por región de producción, 7 leads (1–10 días), ya corriendo en el modal *Calibration* del dashboard (210 probabilidades/día, verificación rolling). §4. |
| **Fee (catálogo modelo C)** | (1) diseño de índice único + (2) pricing por temporada + (3) monitoreo vivo por vigencia + (4) *settlement agent* por evento. §3.4. |

**Las tres decisiones de diseño que sostienen todo el documento:**

1. **El índice se settle sobre un agregado espacial regional, no un punto.** La lección más cara del
   sistema (hindcast India, §1.5) es que un forecast de *extremo regional* medido contra una *observación
   puntual* produce un desajuste geométrico que **castiga la calibración** (BSS −0.155). La geometría de
   settlement DEBE casar con la del forecast. Lo demostramos con nuestros propios datos, no con teoría.
2. **Payout escalonado, no binario.** El daño físico de una helada es continuo; un trigger binario
   introduce *basis risk* estructural (el agricultor pierde el 60 % y el contrato paga 0 o 100 %).
   Escalonar aproxima el pago óptimo — el **expectil condicional** de la pérdida (§2.2).
3. **Prudencia explícita por n pequeño.** Tenemos **1 evento hindcast verificado** y una climatología de
   24 inviernos; NO tenemos 20 temporadas de siniestros reales todavía. El pricing lleva un factor de
   carga por incertidumbre que se **reduce con los datos del propio piloto** (el *flywheel*, §2.3) — y lo
   decimos aquí, no en letra pequeña.

---

## 1. Diseño del índice / trigger

### 1.1 Variable y por qué

La helada que destruye café es **radiativa nocturna**: en noches despejadas y sin viento, la superficie
irradia calor al cielo, el aire cercano al suelo se enfría por debajo de 0 °C, y en terreno de valle el
aire frío drena y se acumula ("cold-air pooling"), llevando el fondo del valle varios grados por debajo
de la ladera. La variable física que captura el daño es la **temperatura mínima del aire a 2 m (T2M
min) diaria**. Es también la cantidad que nuestro motor produce nativamente y contra la que se escribe
la definición de evento (`t2m_min`, dirección `below`).

No usamos NDVI ni proxies de vegetación como *trigger* primario: son indicadores post-daño (retrasados)
y ruidosos para helada; sirven como verificación secundaria de pérdida, no como disparador (§2).

### 1.2 Fuente de datos y GEOMETRÍA de settlement — la decisión central

**El índice se define como el mínimo espacial de T2M-min sobre una caja de producción regional
declarada**, no como la lectura de una estación puntual ni del centroide de la caja.

- **Fuente primaria de settlement propuesta:** reanálisis **ERA5 / ERA5-Land** (Copernicus/ECMWF,
  licencia comercial con atribución), reducido al **mínimo espacial sobre la caja** y sobre las 24 horas
  del día — exactamente la receta `region_min_series` que usa nuestro forecast. Esto garantiza que "lo
  que el modelo predijo" y "contra qué se liquida" comparten geometría (misma caja, misma reducción
  espacial y temporal).
- **Cross-check / fuente oficial local:** estación oficial **IDEAM (Colombia) / INMET (Brasil)** dentro
  de la caja, o **LST nocturno satelital (MODIS/VIIRS)** para la discriminación municipal. Estos son
  candidatos a fuente de settlement *acordada con el partner*; la fuente final se fija en el contrato
  (§5). No usamos un proxy tipo NASA POWER puntual como settlement final (§1.5).

**Cajas de producción (registro reproducible del repo, `oracle/regions.py`):** cada caja es ~2°×2°
alrededor de un centroide, con `share` de producción global. Para café brasileño: Sul de Minas /
MG-Center (`share` 0.30), Zona da Mata (0.15), Cerrado Mineiro/Mogiana (0.08), Espírito Santo (0.10);
y las cajas de frontera fría São Paulo y Paraná. Para Colombia (extensión, §5): eje cafetero
(Caldas/Quindío/Risaralda), Huila, Nariño — con la salvedad de densidad de estaciones IDEAM en altura.

### 1.3 Umbrales y justificación agronómica

El daño por helada en café arábica es **escalonado por severidad**, y los umbrales lo reflejan
(referencias agronómicas estándar y análisis post-evento INMET del episodio 2021):

| Umbral T2M-min | Efecto físico en el cafeto | Rol en el contrato |
|---|---|---|
| **< 4 °C** | Enfriamiento de hoja; daño incipiente de tejido joven en exposición prolongada. | Tramo 1 — pago parcial menor (señal temprana de severidad). |
| **< 2 °C** | **Helada operativa:** daño foliar cierto, quema de hojas y ramas nuevas; umbral usado por el motor como *frost trigger* (`threshold_c = 2.0`). | Tramo 2 — pago intermedio. |
| **< 0 °C** | **Helada letal:** congelación de tejido, muerte de ramas/plantas, impacto plurianual (la planta tarda años en recuperar). El evento 2021 (valles a −3/−5 °C) es el caso de referencia. | Tramo 3 — pago máximo. |

El umbral operativo por defecto es **2 °C** (no 0 °C) porque el daño económico relevante empieza antes
del punto de congelación: una noche a 1 °C en el fondo de valle ya quema la cosecha del año. El
escalonamiento evita el problema binario de "0.1 °C por encima del umbral = 0 pago" (§1.4).

### 1.4 Estructura de payout: escalonada (recomendada), no binaria

**Recomendamos payout escalonado.** Un trigger binario (`Tmin < 2 °C → paga 100 %`, si no `0 %`)
introduce dos patologías de *basis risk*:

1. **Discontinuidad en el umbral:** 2.1 °C paga 0, 1.9 °C paga todo. Ni la física ni la pérdida real
   saltan así; el agricultor a 2.1 °C igual perdió cosecha.
2. **Insensibilidad a la severidad:** una helada a −4 °C (pérdida total plurianual) paga lo mismo que
   una a 1.9 °C (daño foliar recuperable).

Estructura escalonada propuesta (parametrizable con el partner):

```
payout(Tmin_index) =
   0                                    si Tmin_index >= 4 °C
   f1 · límite                          si 2 °C <= Tmin_index < 4 °C     (tramo hoja)
   f2 · límite                          si 0 °C <= Tmin_index < 2 °C     (tramo operativo)
   límite (100 %)                       si Tmin_index < 0 °C             (tramo letal)
```

con `0 < f1 < f2 < 1` calibrados contra la curva de pérdida real cuando el piloto la aporte (§2.2). La
forma escalonada es la aproximación discreta del **pago óptimo que minimiza basis risk = expectil
condicional de la pérdida dado el índice** (§2.2); mientras no haya datos de pérdida del partner, `f1`
y `f2` se fijan con priors agronómicos conservadores y se refinan con el *flywheel*.

### 1.5 *Basis risk* geométrico: la lección India (por qué el settlement es regional, no puntual)

Esta es la motivación de diseño más importante y viene de **nuestro propio sistema de verificación**, no
de la literatura.

En el *verification loop* (modal *Calibration* del dashboard, datos reales), el hindcast de la ola de calor de India
(trigo, mar-2022) obtuvo **BSS −0.155** (n=30): el modelo perdió frente a la climatología. La causa **no
fue el modelo**: el forecast produce un **máximo/mínimo espacial regional** (sobre la caja), pero se
verificó contra la **observación puntual** de NASA POWER en el centroide. En varios días el forecast
regional decía "caliente" y el punto-centroide leía justo por debajo del umbral. Eso es **basis risk
geométrico puro: forecast de extremo regional vs observación puntual** — exactamente el desajuste que un
loop auditable debe exponer. En contraste, la **helada de Brasil**, verificada contra la verdad ERA5 con
la **misma receta espacial** que el forecast, obtuvo **BSS +0.64** (n=12).

**La misma geometría reaparece en la climatología del café y la hace tangible** (cómputo reproducible,
NASA POWER punto-centroide, 24 inviernos 2001–2024 — Anexo A.3):

| Caja | P(≥1 día Tmin < 2 °C por invierno, **punto-centroide**) | Tmin estacional más frío (punto) | Verdad ERA5 **regional** del evento 2021 |
|---|---|---|---|
| **Paraná** | **54 %** (13/24) | −2.2 °C (2013) | 0.21 °C — **helada** (frost verificada) |
| **São Paulo** | **0 %** (0/24) | **2.5 °C** (2021) | **1.91 °C — helada** (frost verificada) |
| **Minas Gerais** | 0 % (0/24) | 5.8 °C (2021) | valles a −3/−5 °C (INMET), grilla ERA5 ~4 °C |

Léase la fila de **São Paulo**: el **punto-centroide nunca** baja de 2.5 °C en 24 inviernos, pero el
**mínimo espacial regional ERA5** del 2021-07-19 fue **1.91 °C = helada** (verificada en nuestro
hindcast). Si liquidáramos el contrato sobre el punto-centroide, **el agricultor pierde y el trigger no
dispara**: el peor resultado posible de un producto paramétrico. Por eso **el índice se define sobre el
agregado espacial regional**, y el settlement usa la **misma geometría** que el monitoreo.

**Regla de diseño, verbatim para el contrato:** *la geometría de la observación de settlement debe ser
idéntica a la geometría del forecast que genera la P(evento) monitoreada.*

**Refuerzo cuantitativo (jul-2026): reanálisis ERA5, una sola fuente y una sola receta espacial para
todas las geometrías** (estudio completo y reproducible: `docs/settlement_geometry_era5_2026-07.md`):

> Sobre la caja de producción de São Paulo, en la helada del 19-20 de julio de 2021, el T2M-min del
> punto-centroide de settlement fue **+2.2 °C** (no cruza el trigger operativo de 2 °C ni el letal de
> 0 °C), mientras el **mínimo espacial regional** de la misma caja **heló a −2.7 °C** (cruza ambos):
> un gap de **4.9 °C** que convierte un día de pérdida de cosecha en un trigger que no dispara. En el
> episodio completo, el punto de São Paulo no registró ningún día bajo 0 °C (el regional registró dos)
> y el punto de Minas no registró ninguno bajo 4 °C (el regional, cuatro). En las tres cajas y los once
> días analizados el punto leyó sistemáticamente más caliente que el mínimo regional (nunca al revés),
> con sesgo de 1.8 a 12.9 °C en el pico. Validez: el mínimo regional a 00Z de este cálculo reproduce la
> verdad ERA5 del hindcast (São Paulo 1.91 °C, Paraná 0.21 °C, Minas 10.68 °C) al tercer decimal. Y como
> el reanálisis a 0.25° no resuelve el drenaje de aire frío de valle (INMET midió −3/−5 °C donde la
> grilla dio ~2-4 °C), liquidar sobre un punto pierde el mínimo regional y el valle sub-grilla a la vez.

Corolario operativo del estudio: **la definición de la caja es cláusula de primer orden del contrato**
(en São Paulo el frío vive en su frontera sur). La caja se fija por anexo cartográfico y no se modifica
sin re-pricing.

### 1.6 Ventana de cobertura

**1 junio – 31 agosto** (invierno austral). Es la ventana de riesgo de helada radiativa en el hemisferio
sur; las heladas destructivas históricas del cinturón (1975, 1994, 2021) caen en jun–jul. Para Colombia,
el régimen es bimodal y de altura (no estacional-invernal clásico); la ventana colombiana se define por
altitud y temporada seca, y es parte del co-diseño del piloto (§5).

### 1.7 Rol de las partes

> **Nota de encuadre (no es consejo legal).** Esta subsección describe el rol que Solstitium propone
> ocupar en la estructura, alineado con el estándar de mercado de bonos catastróficos y seguro
> paramétrico. Es preparación interna para discusión con el partner y con counsel, no una calificación
> jurídica definitiva: ver `docs/regulatory_role_2026-07.md` para el marco regulatorio completo y su
> checklist de validación con abogado.

**Solstitium = calculation agent / index provider independiente.** No tomamos riesgo de balance, no
tenemos interés económico en el resultado del gatillo, y actuamos separados tanto del *index sponsor*
(quien define y comercializa el producto ante el asegurado) como del *risk carrier*. Concretamente:

- **Fuente de datos objetiva y reproducible:** el índice se calcula sobre reanálisis **ERA5 / ERA5-Land**
  (Copernicus/ECMWF), versionado y con la misma geometría de reducción espacial que el forecast (§1.2).
  No usamos un dato propietario no auditable: cualquier tercero puede reproducir el cálculo con la
  fecha y el `CQ_DATA_ROOT`/receta documentados en el Anexo A.
- **Protocolo de disputa:** el cálculo del índice al vencimiento se entrega con su cadena causal
  documentada (qué fuente, qué ventana, qué reducción espacial) para que el partner o un tercero lo
  audite; en caso de disputa, el mecanismo de resolución (recálculo por un tercero neutral sobre la
  misma fuente y receta) se fija en el contrato, no en este documento técnico.
- **Fallback de datos:** si la fuente primaria (ERA5/ERA5-Land) no está disponible en el momento del
  settlement, el contrato debe fijar una fuente de respaldo acordada (estación oficial IDEAM/INMET o
  LST satelital, §1.2) y el orden de prelación entre fuentes; esto se decide con el partner, no se
  asume aquí.
- **Separación de roles:** Solstitium NO es el *index sponsor* (el partner o su distribuidor define el
  producto comercial ante el agricultor) ni el *risk carrier* (la aseguradora/MGA/reasegurador retiene
  el riesgo de balance, §3.4). Esta separación es la que un comité de riesgo de reaseguro espera de un
  proveedor de índice independiente (estándar *event agent* / *calculation agent* tipo PCS (Property
  Claim Services, EE.UU./Japón) o PERILS AG (Europa/Australia) en el mercado de *insurance-linked
  securities*; ver también BIS/IAIS FSI Insights No 62, *"Uncertain waters: can parametric insurance
  help bridge NatCat protection gaps?"*, bis.org/fsi/publ/insights62.htm, consultado 2026-07-04).
- **La (re)aseguradora = risk carrier.** El partner (aseguradora, MGA o reasegurador) es quien suscribe
  la póliza, cobra la prima, retiene el riesgo de suscripción y responde ante el asegurado. Esto ya
  está en §3.4 y §5.5 de este documento; esta subsección lo formaliza como estructura de roles y lo
  ata al marco regulatorio de `docs/regulatory_role_2026-07.md` (semáforo Brasil/SUSEP: proveer índice
  + cálculo + analytics a una aseguradora/reasegurador local es el rol habilitado sin licencia
  aseguradora; tomar o distribuir riesgo no lo es).

---

## 2. *Basis risk*: cuantificado y honesto

### 2.1 Definición

**Basis risk** = la probabilidad/severidad de que el resultado del índice **diverja de la pérdida real
del asegurado**. Dos direcciones, ambas dañinas:

- **Falso negativo (el que mata al producto):** el agricultor sufre pérdida y el índice **no** dispara.
  Fuente dominante: **desajuste geométrico** (§1.5) y umbral demasiado estricto. Lo atacamos con
  settlement regional + escalonamiento + downscaler de terreno (Anexo A.2).
- **Falso positivo:** el índice dispara sin pérdida real (p. ej. helada en una parcela ya cosechada). Lo
  atacamos alineando la ventana con el calendario de cultivo y, cuando el partner lo aporte, con datos de
  fenología/cosecha.

### 2.2 Objetivo matemático: el expectil condicional

El *basis risk* no se elimina, se **minimiza con una función de pago bien elegida**. El resultado formal
que adoptamos como objetivo de diseño: **el pago que minimiza el basis risk (bajo pérdida cuadrática
asimétrica) es el expectil condicional de la pérdida real dado el disparo del índice** — una función
entrenable por regresión sobre pares (índice, pérdida) (Chen et al., *arXiv:2505.02607*, 2025).

Implicación práctica para este term sheet:

- La **curva de payout escalonada de §1.4 es la forma discreta de ese expectil condicional.** Sin datos
  de pérdida, la aproximamos con priors agronómicos (los tramos de §1.3). **Con** los datos de pérdida
  del piloto, ajustamos `f1`, `f2` y los cortes de umbral a la regresión de expectil → el contrato de la
  temporada siguiente tiene *menos* basis risk que el de esta. Ese es el producto #1 madurando.
- El expectil (no la media condicional) porque el asegurado y el asegurador tienen aversión **asimétrica**
  al error: un falso negativo grande es mucho peor que un pequeño exceso de pago.

### 2.3 Qué datos del piloto reducen el basis risk (el *flywheel* — §4.1 de la visión)

El *moat* barato de este modelo de negocio: **cada programa asegurado nos da datos de pérdidas/siniestros
reales que nadie más tiene.** El circuito:

```
piloto asegurado  →  pérdidas reales del partner (por parcela/municipio/temporada)
   →  regresión de expectil índice→pérdida  →  umbrales y tramos re-calibrados
   →  menor basis risk  →  pricing más fino  →  más programas  →  más datos …
```

Concretamente, del partner necesitamos (y esto es cláusula del piloto, no un extra): **(a)** ubicación
(municipio/vereda) de las pólizas, **(b)** pérdida declarada por evento y temporada, **(c)** idealmente,
fecha de siniestro. Con eso, la temporada 2 del piloto ya reporta *cuánto* bajó el basis risk medido
(divergencia índice−pérdida) respecto de la temporada 1.

---

## 3. Pricing indicativo

> **Advertencia de honestidad, arriba y en negrita:** los números de esta sección son **indicativos** y
> se apoyan en **1 evento hindcast verificado** + una **climatología de 24 inviernos de punto-centroide**
> (un *lower bound*, §1.5). **No** tenemos aún 20 temporadas de siniestros reales. Por eso todo pricing
> lleva un **factor de prudencia explícito** (§3.3). Un actuario NO debe firmar prima sobre estos números
> sin (a) fijar la fuente de settlement oficial y (b) correr la climatología regional-agregada sobre el
> reanálisis acordado. Esta sección muestra el **método** y el **orden de magnitud**, no una tarifa.

### 3.1 P(evento) por temporada — la evidencia disponible

**(a) Climatología reproducible (punto-centroide, 24 inviernos, NASA POWER — Anexo A.3).** Frecuencia
empírica de ≥1 día bajo umbral por invierno:

| Caja | P(< 4 °C)/inv. | P(< 2 °C)/inv. | P(< 0 °C)/inv. | Lectura |
|---|---|---|---|---|
| **Paraná** | 92 % (22/24) | **54 % (13/24)** | 21 % (5/24) | Frontera fría — helada operativa más de un año de cada dos. |
| **São Paulo** | 17 % (4/24) | 0 % (0/24)* | 0 %* | *Punto subestima: el regional-agregado sí heló en 2021 (§1.5). |
| **Minas Gerais** | 0 %* | 0 %* | 0 %* | *Idem; valles municipales sí (downscaler, A.2). |

\* **Estas tasas de punto son un LOWER BOUND del riesgo regional-agregado que el contrato realmente
precia.** La tasa de settlement se recomputa sobre el mínimo espacial ERA5 antes de fijar prima (§3.3).

**(b) Evidencia de skill del forecast (no solo climatología).** En el evento 2021 el ensemble/forecast
puso **P(helada) ≈ 0.64 a lead 1** en Paraná (verdad: heló) y detectó la rampa fría 1–4 días antes; la
calibración de helada agregada da **Brier 0.067 vs 0.188 de climatología → BSS +0.64** (n=12,
verificación loop, verdad ERA5). Es decir: el producto de **monitoreo** (§4) aporta *timing*, no solo la
tasa base — un reasegurador puede cubrir cuando P sube, antes del evento.

### 3.2 Expected loss indicativo (ilustrativo del método)

Para una caja con tasa base de settlement `p` (regional-agregada, no punto) y payout escalonado:

```
E[loss] / límite  =  P(0<=Tmin<2) · f2  +  P(Tmin<0) · 1        (tramo hoja f1 omitido si <4°C no paga capital significativo)
```

Ejemplo **ilustrativo** para Paraná con las tasas de **punto** (que subestiman; solo para mostrar el
cálculo, NO para tarifar): con `P(<2°C, no <0)=54%−21%=33%`, `P(<0°C)=21%`, y priors `f2=0.5`:
`E[loss]/límite ≈ 0.33·0.5 + 0.21·1.0 ≈ 0.38`. **Sobre el regional-agregado la tasa será mayor** → el
E[loss] real de settlement sube; por eso este número es solo demostrativo del método, y la prima se fija
tras el recómputo regional (§3.3).

### 3.3 Carga de incertidumbre — el factor de prudencia explícito

Prima indicativa = `E[loss] · (1 + carga_riesgo) · (1 + factor_prudencia) + costos`, donde:

- **`factor_prudencia`** es el add-on por **incertidumbre epistémica de muestra pequeña.** Con n≈1 evento
  verificado y 24 inviernos de punto, proponemos un factor de prudencia **inicial del orden de +30 % a
  +50 %** sobre el E[loss], **decreciente por temporada** conforme el piloto acumula settlements y
  siniestros (el flywheel, §2.3). Esto es una banda de trabajo para el co-diseño, no una tarifa.
- El factor se justifica cuantitativamente con **intervalos de Wilson** sobre las frecuencias base
  (p. ej. 13/24 tiene IC95 amplio) y se **estrecha** al crecer n — misma disciplina estadística que el
  resto del sistema aplica antes de promover cualquier señal a comercial (umbrales de promoción: IC de
  Wilson que excluya la moneda, ≥2 regímenes).
- **Recomputar la tasa base sobre el reanálisis regional-agregado acordado** (no el punto) es
  **prerrequisito** de cualquier prima firmada; sube la tasa y por tanto el E[loss] y baja parte del
  factor de prudencia (menos incertidumbre geométrica).

### 3.4 Estructura de fee (catálogo modelo C, §4.1 de la visión)

Vendemos **el número y su defensa**, en cuatro componentes sobre el mismo motor:

| # | Componente | Qué entrega | Cobro |
|---|---|---|---|
| 1 | **Diseño de índice/trigger** | Esta spec instanciada para las cajas del partner: variable, geometría de settlement, umbrales, curva escalonada, análisis de basis risk. | **Fee único por programa.** |
| 2 | **Pricing calibrado** | P(trigger) por temporada/caja + historial de calibración (Brier/BSS) + E[loss] + prima sugerida con factor de prudencia. | **Retainer por temporada** o % del GWP. |
| 3 | **Monitoreo en vivo** | P(helada) diaria por caja/municipio durante la vigencia (§4). "Subió de 12 %→34 %, reasegura YA." | **Suscripción durante la vigencia.** |
| 4 | **Settlement (calculation agent)** | Cálculo independiente y auditable del índice al vencimiento sobre la fuente oficial acordada, con cadena causal documentada. | **Fee por evento/vencimiento.** |

**No tomamos riesgo de balance:** somos el proveedor del índice y el *calculation agent*, no el
asegurador. El partner (aseguradora/MGA/reasegurador) retiene el riesgo.

---

## 4. Monitoreo en vivo (lo que el partner recibe hoy)

**Ya corre.** El pipeline diario `pevent` (DR-C1) produce, sin GPU, sobre datos abiertos de ECMWF
(licencia CC-BY-4.0, uso comercial con atribución):

- **P(helada) diaria por caja de producción, para 7 leads (1, 2, 3, 4, 5, 7, 10 días).** Hoy son ~210
  probabilidades/día (18 cajas agro + 7 ciudades EU × 7 leads); las cajas de café/OJ frost-vulnerables
  (MG-Center, Zona da Mata, Espírito Santo, Mogiana, São Paulo, Paraná) están incluidas.
- **Definición del evento viaja con cada probabilidad** (contrato `pevent.v1`): `variable=t2m_min`,
  `threshold_c=2.0`, `direction=below`. El verificador liquida el resultado con la **misma regla** que
  usó el forecast — sin deriva entre lo predicho y lo evaluado.
- **Modal *Calibration* del dashboard:** diagrama de fiabilidad, Brier vs climatología y BSS por evento,
  ventana del récord, fuente de observación y lag. Verificación **rolling**: cada probabilidad se gradúa
  sola al madurar su valid-time contra la observación independiente.

**Método versionado (el disclaimer, explícito):** cada documento diario lleva un campo `method` que
declara **exactamente** cómo se produjo la probabilidad:
- `ensemble-native-v1` — fracción nativa de los **50 miembros** del IFS-ENS que cruzan el umbral (sin
  supuesto distribucional). Camino preferido.
- `deterministic-sigma-v1` — *proxy v1* cuando solo hay campo determinista: probit de una Normal centrada
  en el T2M determinista con σ climatológica que crece con el lead. **Es un proxy explícitamente
  versionado**, no un ensemble calibrado; se supera automáticamente cuando el ensemble nativo está
  disponible.

El partner sabe siempre qué método generó cada número. Esto es la "calibración auditable" como atributo
del producto: no un dashboard más, sino el forward record aplicado a su póliza.

---

## 5. Lo que NO prometemos todavía (límites explícitos)

Un comité de riesgo confía más en un proveedor que marca sus propios límites. Estos son los nuestros, sin
adornos:

1. **Verificación con más temporadas.** El skill de helada está verificado sobre **1 evento** (Brasil
   2021, BSS +0.64) más una climatología de 24 inviernos. **No** afirmamos calibración multi-temporada
   todavía; el factor de prudencia (§3.3) lo compensa y el flywheel lo cierra. El objetivo interno es
   ≥100 verificaciones por evento con IC antes de retirar el disclaimer de muestra pequeña.
2. **Resolución municipal.** La discriminación sub-caja (finca/municipio, p. ej. valle de Varginha vs
   ladera de Três Pontas) usa un **downscaler de terreno estadístico** (lapse rate + cold-air pooling),
   validado a **±0.5 °C vs INMET en 1 evento** (2021). Es suficiente para triggers por municipio, **no**
   para un mapa de riesgo espacial <5 km (eso requiere un CorrDiff de región propio, gated por un contrato
   pagado que lo exija). No vendemos resolución de finca como validada más allá de ese ±0.5 °C / 1 evento.
3. **Settlement final requiere fuente oficial acordada.** El monitoreo corre sobre ECMWF open-data y el
   hindcast se verificó contra ERA5; el **settlement contractual final** debe fijarse sobre una fuente
   **oficial acordada con el partner** (ERA5-Land / IDEAM / INMET / LST), **no** sobre un proxy puntual
   tipo NASA POWER (que, como muestra §1.5, subestima el mínimo regional). La elección de fuente y su
   geometría es la primera decisión del contrato.
4. **Colombia es extensión, no piloto ancla en esta v1.0.** El eje cafetero colombiano tiene régimen de
   helada distinto (altura, no invierno austral) y **densidad de estaciones IDEAM escasa en altura**
   (~1 estación/2000 km² en Nariño/Huila). Antes de un settlement municipal colombiano fiable hace falta
   resolver esa densidad (fusión LST GOES-16, o acuerdo de datos con IDEAM/gremio). El piloto ancla
   propuesto es **brasileño**; Colombia entra en fase 2 con ese gate resuelto.
5. **No tomamos riesgo de suscripción.** Somos index provider + calculation agent. El riesgo de balance
   es del partner.

---

## 6. Anexo técnico — evidencia reproducible del repo

Todo lo cuantitativo de este documento es reproducible desde el repositorio (metodología completa,
hindcasts, verification loop). Rutas y comandos:

### A.1 Hindcast Brasil-2021 (skill de helada) y bake-off de modelo
- **Verdad ERA5 + forecast por caja/día:** `output_bundle/bakeoff/bakeoff_results.json`. Evento
  2021-07-18 init, valid 07-19…07-22. Mínimo espacial ERA5 (00Z): Paraná 0.21 °C, São Paulo 1.91 °C
  (ambos helada verificada); Minas 10.68 °C. Modelo Aurora (MIT): RMSE 1.34 °C, `frost_hit: true`;
  Pangu (baseline): 1.45 °C.
- **Runner del bake-off:** `scripts/a100_bakeoff.py`; sesión documentada en
  `docs/ROADMAP_DEPLOYMENT_READY.md` §5 (sesión A100 #2).

### A.2 Downscaler de terreno (discriminación municipal, ±0.5 °C)
- **Módulo:** `oracle/physics/terrain_downscale.py` (41 tests verdes). Demo Sul de Minas:
  `brazil_coffee_demo()`. Con grilla ERA5 = 4 °C y noche estable, Varginha (valle, 940 m) → **0.96 °C
  (helada)** y Guaxupé (valle, 850 m) → **1.54 °C (helada)**, mientras la ladera de Três Pontas (1100 m)
  → 3.42 °C (sin helada). Reproduce el patrón INMET 2021 (valles −1/−3 °C con grilla ~4 °C).
- **Assessment honesto de límites:** `docs/corrdiff_assessment.md` (qué captura la aproximación
  estadística vs qué exigiría un CorrDiff de región propio, y su gate).

### A.3 Climatología de helada (base rate del pricing) — CÓMPUTO REPRODUCIBLE
- **Método:** para cada caja del registro, frecuencia empírica de ≥1 día con `T2M_MIN < umbral` en la
  ventana 1-jun→31-ago, sobre 24 inviernos (2001–2024), vía el loader NASA POWER **del propio repo**
  (`causalquant.data.climate.obs_verification.get_observed_range`, `source="nasa_power"`) — el mismo que
  usa el verification loop. **Geometría: punto-centroide** (por eso es un *lower bound* del riesgo
  regional-agregado — §1.5).
- **Resultado (verificado 2026-07-02, 24/24 inviernos con datos):**
  - Paraná (−24.5, −51.5): P(<4°C)=**0.917** (22/24), P(<2°C)=**0.542** (13/24), P(<0°C)=**0.208** (5/24);
    Tmin estacional más frío −2.2 °C (2013).
  - São Paulo (−22.0, −48.0): P(<4°C)=**0.167** (4/24), P(<2°C)=**0.000**, P(<0°C)=**0.000**; Tmin más
    frío 2.5 °C (2021). **[el regional-agregado ERA5 sí heló en 2021: 1.91 °C — contraste geométrico A.1]**
  - Minas Gerais (−19.5, −45.5): P(<4°C)=**0.000**; Tmin más frío 5.8 °C (2021). **[valles municipales sí
    — A.2]**
- **Reproducción:** script efímero (no commiteado, patrón de fábrica) sobre el loader del repo con
  `CQ_DATA_ROOT` apuntando al caché; una tarde de queries NASA POWER (24 años × 3 cajas). El método está
  descrito arriba en su totalidad para que un tercero lo reejecute con el reanálisis oficial que se
  acuerde.

### A.4 Verification loop (calibración auditable)
- **Estado acumulado:** `logs/daily/verification_state.json` (n=42: helada BSS +0.64 vs ERA5; India BSS
  −0.155 vs punto — la motivación de §1.5). Contrato de datos: `causalquant/data/climate/pevent_contract.py`.
- **Documentación:** `docs/verification_loop.md` (diseño, fuentes de obs, política de lag, y la nota
  explícita: "match the settlement obs geometry to the forecast geometry").
- **Pipeline diario:** `oracle/physics/pevent_daily.py` (ECMWF open-data, ensemble nativo 50 miembros /
  proxy determinista-σ versionado). Cron: `.github/workflows/shadow-record.yml`.

### A.5 Objetivo matemático del payout
- **Expectil condicional para basis risk:** Chen et al., *arXiv:2505.02607* (2025) — el pago que minimiza
  el basis risk es el expectil condicional de la pérdida dado el disparo. Nota interna:
  `docs/research/eu_engine_strategy_2026-06.md` §4.

### A.6 Análisis de cola por teoría de valores extremos (EVT)

Sobre el índice de helada (T2M-min estacional, invierno austral, 24 inviernos 2001-2024 de la fuente
reproducible del repo, la misma de A.3, punto-centroide), se ajusta la cola inferior con dos vías
complementarias: valor extremo generalizado sobre mínimos anuales (GEV block-minima) y Pareto
generalizada sobre excedencias diarias (GPD peaks-over-threshold; umbral seleccionado con
mean-residual-life y estabilidad de parámetros, QQ de ajuste 0.997-0.999). En la caja de **Paraná**
(frontera fría, contrato ancla), el parámetro de forma es **xi = -0.28, IC95 [-0.38, -0.21]** (vía GPD):
la cola de frío está **acotada** (límite físico, no Pareto pesada). Los **niveles de retorno** de T2M-min
(punto-centroide) son -0.5 C a 5 años, -1.8 C a 25 años y **-2.5 C a 100 años (IC95 [-3.7, -1.2])**; la
probabilidad estacional de cruzar el trigger operativo (<2 C) es 0.59-0.73 y la del letal (<0 C)
0.21-0.27, consistente con la frecuencia empírica de A.3. Estas cifras usan la geometría de **punto**,
que 1.5 documenta como **cota inferior del frío regional**: el mínimo espacial regional (settlement
propuesto) es sistemáticamente más frío (gap medido de 4.9 C en 2021), por lo que **los niveles de
retorno regionales de settlement serán más severos que los de este anexo**; se reportan como cota
conservadora hasta recomputarlos sobre el reanálisis regional. Reproducible: `scripts/evt_term_sheets.py`,
módulo `causalquant/actuarial/evt.py`. Ningún proveedor comercial publica esta cola con intervalos de
confianza.

### A.7 Basis risk descompuesto (los tres componentes con número)

El basis risk de este contrato se descompone y cuantifica por componente (reproducible en
`causalquant/actuarial/basis_risk.py`): **(1) SPATIAL** = distancia settlement-exposición. Sobre la caja
de São Paulo, el punto-centroide leyó +4.9 C más caliente que el mínimo espacial regional en la helada
del 19-20 jul 2021 (+1.8 C Paraná, +12.9 C Minas), un sesgo sistemático en dirección (el punto nunca lee
más frío) que omite entre el 50 % y el 100 % de los días de pérdida según la caja. Liquidar sobre el
mínimo regional (como define este contrato) elimina este componente. **(2) TEMPORAL** = desajuste
ventana-vs-daño. La ventana 1-jun a 31-ago cubre 5 de las 6 heladas destructivas históricas del cinturón
(16.7 % fuera), y el único evento fuera (una geada de fin de mayo) está a 1 día del borde; extender el
inicio a 15-may lo cierra. **(3) DESIGN** = no-linealidad no capturada por la forma del payout. El payout
escalonado 4/2/0 C captura R2=0.83 de la severidad física del daño; el 17 % restante es la no-linealidad
fina que una curva calibrada a pérdidas del piloto (expectil condicional) cerraría. **Tasa de falso
negativo:** con settlement puntual, 62.5 % de los días de pérdida real no dispararían (IC95 Wilson
[30.6 %, 86.3 %]); con settlement regional, 0 % geométrico. **Skill index-pérdida:** R2 = 0.83 (>= regla
de mercado 0.70), hedging effectiveness 0.83, y distancia de expectil de cola 0.19, es decir el payout
sigue al daño en la cola severa. (Skill sobre proxy físico del episodio 2021; la calibración
multi-temporada es el flywheel del piloto.)

---

*Documento vivo. Los números de pricing son indicativos y sujetos a: (a) fijación de la fuente de
settlement oficial, (b) recómputo de la tasa base sobre el reanálisis regional-agregado acordado, (c)
datos de pérdida del piloto para la calibración del expectil. Contacto técnico: equipo Solstitium/
CausalQuant.*
