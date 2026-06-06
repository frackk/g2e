# Generador de eActivities para Casio fx-9750GIII

Herramienta para crear archivos `.g2e` (eActivity) en la PC y transferirlos a la calculadora via USB.

---

## Registro ChatGPT — fix crítico de crash al segundo open (2026-05-26)

> Esta sección fue agregada por ChatGPT. Objetivo: dejar documentado exactamente qué se cambió para que Claude Code pueda continuar el proyecto sin perder contexto.

### Problema reportado por Fran

En la versión recibida, los `.g2e` generados por el programa podían abrirse en la Casio fx-9750GIII, pero al cerrar el archivo e intentar abrirlo nuevamente la calculadora se congelaba, la pantalla se corrompía visualmente y el teclado dejaba de responder. La única recuperación era resetear o quitar pilas. Fran también notó que estos archivos parecían abrir más lento que los eActivities creados directamente desde la calculadora.

### Causa principal encontrada

El campo `length2` del subchunk `EACT1` estaba mal calculado.

Estructura real observada en archivos nativos y de referencia:

```text
0x78  EACT1\0\0\0
0x80  00 00 00 14
0x84  length2
0x88  D4 00 00 66
0x8C  LC + directorio + datos de líneas
```

En archivos reales (`DERIVADA.g2e`, `FUNCIONE.g2e`, `INTEGRAL.g2e`, `TEOREMAS.g2e`, `VECTORES.g2e`, `PC~EJEMP.g2e`), `length2` mide solamente desde `0x8C` hasta EOF, o sea:

```python
length2 = len(LC + line_dir + line_data)
```

La versión anterior hacía:

```python
length2 = len(D4 00 00 66 + LC + line_dir + line_data)
```

Eso dejaba `length2` exactamente **4 bytes más grande** que el formato real. Es muy probable que por eso el archivo pudiera abrir una vez, pero quedara inseguro cuando la calculadora intentaba cerrar/releer/reprocesar el eActivity.

### Fix aplicado en `g2e.py`

Se cambió:

```python
length2 = len(inner_body)
```

por:

```python
length2 = len(content)
```

donde `content` es `LC + line_dir + line_data`, sin contar el marcador `D4 00 00 66`.

También se actualizó `validate_g2e()` para verificar esto correctamente:

```python
length2 == len(data) - 0x8C
```

Antes el validador seguía la lógica incorrecta del generador, por eso no detectaba el bug.

### Segundo fix importante: headings seguros de 21 caracteres

Los archivos reales usan headings de tipo `0x07` con ancho fijo de 21 caracteres, por ejemplo:

```text
======DERIVADA=======
======FUNCIONE=======
======TEOREMAS=======
```

La versión anterior podía generar headings variables como `======TEST======` o incluso un heading vacío si el usuario no escribía `=== Título ===`. Eso no seguía el patrón nativo y podía dejar el archivo en un estado frágil.

Ahora `g2e.py` genera siempre headings seguros de 21 caracteres:

```text
======TITULO=========
```

Reglas nuevas:

- título base máximo: 8 caracteres;
- caracteres seguros: `A-Z`, `0-9`, `_`, `-`, `~`;
- si el strip no tiene título, usa el nombre del archivo como fallback;
- si tampoco hay nombre válido, usa `EACT`.

### Tercer fix: nombres de archivo seguros para calculadora

En `app.py` se agregó sanitización del nombre descargado:

- máximo 8 caracteres antes de `.g2e`;
- se convierte a mayúsculas;
- caracteres raros pasan a `_`;
- ejemplo: `mi_eactivity_largo` → `MI_EACTI.g2e`.

Esto se hizo porque la calculadora trabaja mejor con nombres estilo 8.3. El binario `.g2e` no guarda el filename en la cabecera, pero el navegador/almacenamiento de la calculadora sí puede verse afectado por nombres largos o raros.

### Cuarto fix: prefijo de líneas matemáticas `0x82`

Antes todas las líneas matemáticas se generaban con prefijo:

```text
00 80 00 HH
```

En los `.g2e` reales, el primer word no es siempre `0x0080`; suele ser un hint/cache de ancho renderizado. Se agregó `_estimate_math_width()` para calcular un ancho aproximado y evitar que todas las fórmulas parezcan artificialmente largas/scroll-heavy.

Esto no era necesariamente la causa del crash, pero sí puede explicar parte de la sensación de apertura más lenta o comportamiento menos nativo.

### Quinto fix: validador estructural

Se agregó `validate_g2e(data)` en `g2e.py`. Ahora cada archivo generado se valida antes de enviarse desde Flask.

Verifica, entre otras cosas:

- `FileSize` coincide con el tamaño real;
- `LS == 0x38`;
- `_VERSION_MARKER` correcto;
- `_SETUP_AREA` exacto de 56 bytes;
- `@EACT` en offset `0x68`;
- `EACT1` en offset `0x78`;
- `length1` correcto;
- `length2` correcto según archivos reales;
- marcador `D4 00 00 66` correcto;
- directorio de líneas monotónico;
- primer heading `0x07` de 21 caracteres.

### Sexto fix: valor absoluto

Se implementó soporte para:

```text
\abs{x}
```

Encoding usado:

```text
97 1D 1A [contenido] 1B 1E
```

Este patrón aparece en archivos reales alrededor de fórmulas de vectores/módulos. El botón de valor absoluto de la UI ahora inserta `\abs{x}` en vez de `|x|`.

### Fixes en `templates/index.html`

- Los botones matemáticos ahora tienen `type="button"` para evitar comportamientos raros dentro/fuera del formulario.
- Los tabs de símbolos también tienen `type="button"`.
- Se corrigieron posiciones de selección del cursor en:
  - fracción;
  - potencia;
  - raíz;
  - valor absoluto.
- El campo de nombre de archivo ahora tiene `maxlength="8"`.
- El preview reconoce/renderiza `\abs{x}`.

### Archivos modificados por ChatGPT

- `g2e.py`
- `app.py`
- `templates/index.html`
- `PROYECTO.md`

Se dejaron backups locales durante el trabajo:

- `g2e.py.bak_chatgpt`
- `app.py.bak_chatgpt`
- `templates/index.html.bak_chatgpt`
- `PROYECTO.md.bak_chatgpt`

No es obligatorio conservarlos en el proyecto final.

### Pruebas realizadas por ChatGPT

Se generaron archivos de prueba con:

- texto sin `=== título ===`;
- texto con título;
- fórmulas con `\frac`, `\sqrt`, potencia y `\abs`;
- muchas líneas de texto.

Todos los archivos generados pasaron `validate_g2e()`.

Además, el validador fue probado contra archivos reales incluidos en el proyecto:

- `DERIVADA.g2e` OK;
- `FUNCIONE.g2e` OK;
- `INTEGRAL.g2e` OK;
- `TEOREMAS.g2e` OK;
- `VECTORES.g2e` OK;
- `PC~EJEMP.g2e` OK.

`LIMITES.g2e` tiene al menos una entrada nativa de tipo `0x03` que el generador no usa actualmente; por eso no se lo tomó como fallo del fix.

### Estado pendiente

Lo más importante ahora es que Fran pruebe en hardware real:

1. generar un `.g2e` simple;
2. copiarlo a la calculadora;
3. abrirlo;
4. cerrarlo;
5. volver a abrirlo varias veces;
6. probar también un archivo con fórmulas.

Si todavía crashea, el siguiente sospechoso sería el formato interno de líneas `0x82` y sus hints/cache de renderizado, pero el error de `length2 +4` era el bug estructural más fuerte encontrado.



## Qué es esto

La calculadora Casio fx-9750GIII puede abrir archivos `.g2e` que contienen texto formateado, fórmulas matemáticas y secciones organizadas en "strips". Normalmente estos archivos se crean directamente en la calculadora, lo cual es lento. Este proyecto genera esos archivos binarios desde una interfaz web.

## Cómo correrlo

```
py app.py
```

Abrir http://localhost:5000

## Estructura del proyecto

```
app.py                  — servidor Flask (GET / sirve la UI; POST /generate descarga el .g2e)
g2e.py                  — toda la lógica de generación del binario .g2e
templates/index.html    — interfaz web completa (editor + preview + paleta de símbolos)

DERIVADA.g2e            ┐
FUNCIONE.g2e            │  Archivos .g2e reales escritos en la calculadora.
INTEGRAL.g2e            │  Se usan como referencia para entender el formato binario.
LIMITES.g2e             │
VECTORES.g2e            │
TEOREMAS.g2e            ┘

PC~EJEMP.g2e            — Archivo generado por Eact Maker (herramienta online de referencia).
                          Contiene un catálogo completo de 104 símbolos en la entrada [18].
                          Es la fuente principal para identificar encodings desconocidos.
```

---

## Formato binario .g2e

### Estructura del archivo

```
[0x00–0x1F]  Container Header (32 bytes, almacenados como ~NOT bit a bit)
[0x20–0x27]  FileSize (4 bytes BE) + LS=0x38 (4 bytes BE)
[0x28–0x2F]  Version marker: 00 01 02 00 03 60 32 00
[0x30–0x67]  Setup area (56 bytes fijos, idénticos en todos los archivos)
[0x68–...]   @EACT chunk → EACT1 sub-chunk → LC + directorio de líneas + datos
```

### Container Header (32 bytes, invertidos)

| Offset | Valor real (antes del NOT) | Descripción |
|--------|---------------------------|-------------|
| 0x00   | `USBPower`                | Magic string |
| 0x08   | `49 00 10 00 10 00`       | Tipo de archivo: eActivity |
| 0x0E   | `(filesize + 0x41) & FF`  | Control byte C1 |
| 0x0F   | `01`                      | Fijo |
| 0x10   | FileSize (4 bytes BE)     | Tamaño total del archivo |
| 0x14   | `(filesize + 0xB8) & FF`  | Control byte C2 |
| 0x15–0x1F | `FF FF ... FF`         | Fijos |

### Tipos de línea en el directorio

| Tipo | Descripción |
|------|-------------|
| `0x07` | Heading (strip title), almacenado como `======TITULO======` |
| `0x81` | Línea de texto plano |
| `0x82` | Línea matemática 2D (con prefijo `00 80 00 HH`) |

**Reglas obligatorias del directorio:**
- Después de cada heading (0x07) → siempre hay una entrada TEXT vacía (`00 00 00 00`)
- Todos los datos están alineados a 4 bytes (padding con `\x00`)
- Offsets en el directorio: 3 bytes big-endian, relativos al campo LC

### Prefijo de línea matemática (0x82)

```
00 80 00 HH  [contenido] 00
```

Valores de HH según contenido:
- `0x1A` (26px): fracción + raíz
- `0x16` (22px): solo fracción
- `0x0C` (12px): raíz o superíndice
- `0x08` (8px): texto plano (no debería ser 0x82)

---

## Encoding de caracteres (FONTCHARACTER)

### ASCII

Los caracteres ASCII imprimibles (0x20–0x7E) se mapean 1:1.

### Símbolos especiales confirmados en hardware

| Símbolo | Bytes | Estado |
|---------|-------|--------|
| π | `E6 40` | ✅ Confirmado |
| θ | `E6 41` | ✅ Confirmado |
| ∞ | `E6 43` | ✅ Confirmado |
| ≤ | `E6 46` | ✅ Confirmado |
| ≥ | `E6 47` | ✅ Confirmado |
| ≠ | `E6 48` | ✅ Confirmado |
| → | `E6 9C` | ✅ Confirmado |
| ← | `E6 9B` | ✅ Confirmado |
| ↑ | `E6 99` | ✅ Confirmado |
| ↓ | `E6 9A` | ✅ Confirmado |
| ∫ | `E6 BB` | ✅ del código fuente de PC~EJEMP |
| ∪ | `E6 B0` | ✅ Confirmado por el usuario |
| ∩ | `E6 B1` | ✅ Confirmado por el usuario |
| × | `00 D7` | ✅ Confirmado |
| ÷ | `00 F7` | ✅ Confirmado |
| ² | `00 B2` | ✅ Confirmado |
| ³ | `00 B3` | ✅ Confirmado |
| ° | `00 B0` | ✅ Confirmado |
| ± | `00 B1` | ✅ Confirmado |
| √ (glifo solo) | `00 BD` | ✅ Confirmado |

### Letras griegas minúsculas — ⚠️ NO CONFIRMADAS en hardware

Rango estimado E6 BD–D4 (24 letras, orden alfabético):

| Letra | Bytes estimados | | Letra | Bytes estimados |
|-------|----------------|-|-------|----------------|
| α | `E6 BD` | | ν | `E6 C9` |
| β | `E6 BE` | | ξ | `E6 CA` |
| γ | `E6 BF` | | ο | `E6 CB` |
| δ | `E6 C0` | | ρ | `E6 CD` |
| ε | `E6 C1` | | σ | `E6 CE` |
| ζ | `E6 C2` | | τ | `E6 CF` |
| η | `E6 C3` | | υ | `E6 D0` |
| ι | `E6 C5` | | φ | `E6 D1` |
| κ | `E6 C6` | | χ | `E6 D2` |
| λ | `E6 C7` | | ψ | `E6 D3` |
| μ | `E6 C8` | | ω | `E6 D4` |

> θ y π ya tienen códigos propios confirmados (E6 41 y E6 40). E6 C4 y E6 CC son posibles variantes.

### Letras griegas mayúsculas — ⚠️ NO CONFIRMADAS en hardware

Solo las que aparecen en el catálogo de Eact Maker (las que la calculadora soporta):

| Letra | Bytes estimados | | Letra | Bytes estimados |
|-------|----------------|-|-------|----------------|
| Γ | `E6 B2` | | Ξ | `E6 D7` |
| Δ | `E6 B3` | | Π | `E6 D8` |
| Θ | `E6 B4` | | Ψ | `E6 D9` |
| Λ | `E6 B5` | | Φ | `E6 DA` |
| Σ | `E6 BC` | | Υ | `E6 DB` |
| Ω | `E6 B6` | | Η | `E6 DC` |
| | | | Μ | `E6 DD` |
| | | | Ν | `E6 DE` |

### Símbolos pendientes de identificar

- **E5 C0–DF** (29 símbolos): aparecen en el catálogo de PC~EJEMP pero no se identificaron. Probablemente símbolos de conjuntos/lógica (∈, ∉, ⊂, ⊃, ∂, ∇, ∃, ∀, ∧, ∨, ¬, ⇒, ⇔...).
- **7F XX** (secuencias de 2 bytes): varias aparecen en PC~EJEMP (`7F C7`, `7F 54`, `7F 50`, `7F 53`).
- **E6 B7–BA, B8**: entre los confirmados y los griegos, rango no identificado.
- **E6 D5–D6**: entre griegos y el grupo de mayúsculas, sin identificar.

---

## Markup matemático (sintaxis del editor)

| Markup | Resultado | Encoding Casio |
|--------|-----------|----------------|
| `\frac{num}{den}` | Fracción 2D | `BB 1D 1A [num] 1B 1A [den] 1B 1E` |
| `x^{n}` o `^{expr}` | Superíndice | `A8 1A [exp] 1B` |
| `\sqrt{x}` | Raíz cuadrada con vínculum | `86 1D 1A [x] 1B 1E` |
| `\sqrt[n]{x}` | Raíz n-ésima | `B8 1D 1A [n] 1B 1A [x] 1B 1E` |
| `\int` | Símbolo ∫ | `E6 BB` |

Todos los encodings de markup confirmados desde archivos reales (INTEGRAL.g2e, LIMITES.g2e, PC~EJEMP.g2e).

---

## Estado actual (al 2026-05-26)

### ✅ Funcionando confirmado

- Generación correcta del container header (control bytes C1/C2, bytes fijos)
- Setup area: exactamente 56 bytes, idéntico a archivos reales
- Headings en formato `======TITULO======` con blank TEXT después
- Texto plano: ASCII 1:1
- Símbolos especiales básicos: flechas, ≤ ≥ ≠, π θ ∞, ×÷²³°±
- ∪ ∩ confirmados
- Markup matemático: \frac, \sqrt, \sqrt[n], ^{}, \int — encodings tomados de archivos reales

### ⚠️ Implementado pero sin confirmar en hardware

- Letras griegas minúsculas (α β γ δ ε ζ η ι κ λ μ ν ξ ο ρ σ τ υ φ χ ψ ω) — códigos E6 BD–D4 son estimados
- Letras griegas mayúsculas (Γ Δ Θ Λ Σ Ω Ξ Π Φ Ψ Υ Η Μ Ν) — códigos estimados
- Fracción, raíz, superíndice: encoding derivado de archivos reales pero sin test end-to-end completo
- ≈ (E6 49): probable por patrón, sin confirmar

### ❌ Pendiente / no implementado

- **CRÍTICO**: Confirmar que el crash al segundo open está resuelto con los fixes aplicados
- **Valor absoluto** `|x|`: debería usar `97 1D 1A [content] 1B 1E` (tomado de PC~EJEMP, no implementado)
- **E5 C0–DF**: 29 símbolos no identificados (∈ ∉ ⊂ ⊃ ∂ ∇ ∃ ∀ y otros — pendiente de análisis)
- **7F XX** sequences: varios símbolos de dos bytes no identificados
- **Integral definida con límites**: ∫ con bounds superior/inferior
- **Límites** (lim): notación lim_{x→a}
- **Sumatorias** con bounds
- **Derivadas** (notación f', dy/dx)
- Preview canvas: se desea misma fuente que Eact Maker (https://tools.planet-casio.com/EactMaker/)
- Corte de píxeles en caracteres: reportado pero no investigado

---

## Historial de bugs críticos resueltos

| Bug | Causa | Fix |
|-----|-------|-----|
| Crash al abrir el archivo | `_SETUP_AREA` era 57 bytes → `@EACT` en offset 0x69 en vez de 0x68 | Corregido a 56 bytes exactos |
| Crash al abrir | `_VERSION_MARKER` incorrecto | Corregido a `00 01 02 00 03 60 32 00` |
| Pantalla congelada al segundo open | Letras griegas mapeadas a códigos erróneos (E6 B0–BC), y entrada `00 00 00 00` antes de MATH era incorrecta | Removidos blanks antes de MATH; griegas movidas a E6 BD–D4 |
| Headings incorrectos | Almacenaba solo `TITULO` sin el padding de `======` | Corregido a `======TITULO======` |
| Falta de blank después de heading | No se emitía el TEXT vacío obligatorio post-heading | Agregado `_BLANK` después de cada heading |

---

## Herramienta de referencia

**Eact Maker**: https://tools.planet-casio.com/EactMaker/

- Genera archivos .g2e compatibles con la calculadora
- Tiene una paleta de símbolos organizada en tabs idéntica a la de la calculadora
- Usa la misma fuente bitmap que la calculadora en su preview
- El archivo `PC~EJEMP.g2e` fue generado con esta herramienta y contiene un catálogo de 104 símbolos en la entrada [18] del directorio — es la fuente principal para identificar encodings desconocidos

---

## Ideas futuras (no prioritarias)

- Convertir de Flask a app de escritorio (PyWebView, Electron, o Tkinter)
- Publicar en GitHub
- Branding: nombre y web del usuario en la UI

---

## Cambios ChatGPT — 2026-05-26 — Preview exacta y paleta ampliada

### Contexto de este paquete

- El usuario reportó que el fix anterior parece haber eliminado el crash al reabrir el eActivity en la Casio fx-9750GIII.
- Objetivo de esta tanda: mejorar funcionalidad, no estética final.
- Prioridades pedidas por el usuario:
  1. Arreglar la pantalla de visualización para que represente mejor lo que se verá en la calculadora.
  2. Agregar una paleta por tabs con más caracteres, inspirada en EactMaker / calculadora.
  3. Documentar todo para que Claude Code pueda continuar.

### Nota técnica importante sobre la base usada

En el entorno de ChatGPT, el `.rar` subido por el usuario aparece como RAR5 comprimido. El sandbox actual no tiene extractor RAR disponible, por lo que no se pudo descomprimir directamente ese `.rar`. Para no frenar el avance, estos cambios se aplicaron sobre la base del último paquete funcional generado por ChatGPT: `Calculadora_FIX_ChatGPT.zip`.

Si Claude Code había hecho una minicorrección después de ese ZIP y antes del `.rar` nuevo, conviene revisar/mergear esa diferencia manualmente. Los archivos modificados en esta tanda son:

- `g2e.py`
- `templates/index.html`
- `PROYECTO.md`

### Fix 1 — Preview matemática recursiva

Problema reportado:

- En el editor, el usuario escribe markup como `\frac{x}{\sqrt[3]{8}}` o `x^{3}`.
- En la calculadora el archivo se veía bien.
- Pero en la vista previa web aparecían cosas como `\sqrt`, `x^3`, o directamente desaparecían partes de la expresión.

Causa:

- El parser visual de `templates/index.html` solo parseaba expresiones de primer nivel.
- Dentro de una fracción, `num` y `den` se guardaban como strings crudos.
- Entonces, si el denominador era `\sqrt[3]{8}`, el renderer lo dibujaba como texto literal o lo medía mal.

Cambio realizado:

- Se reescribió el parser visual para que sea recursivo.
- Ahora `\frac`, `\sqrt`, `\sqrt[n]`, `^{}`, `\abs{}` y `\int` pueden aparecer anidados dentro de otras expresiones.
- Ejemplos que ahora deberían previsualizarse mejor:
  - `x^{3}`: muestra el 3 como exponente elevado.
  - `\frac{x}{\sqrt[3]{8}}`: muestra una fracción con raíz cúbica dentro del denominador.
  - `\frac{x^{2}}{\sqrt{x+1}}`: muestra potencia arriba y raíz abajo.
  - `\abs{x-2}`: muestra barras de valor absoluto.

Limitación:

- La preview sigue siendo una simulación canvas, no una copia perfecta del renderer interno de Casio.
- El objetivo de esta tanda fue eliminar texto crudo tipo `\sqrt` dentro de fórmulas y mejorar la representación general, sin rediseñar toda la UI.

### Fix 2 — Heading de preview más parecido a la calculadora

Antes:

- La preview mostraba el título del strip como texto simple.

Ahora:

- La preview construye un heading visual de 21 caracteres con formato tipo calculadora:
  - `======TITULO=======`

Esto acompaña el comportamiento del backend, que ya genera headings fijos de 21 caracteres.

### Fix 3 — Valor absoluto implementado también en backend

Antes:

- La UI tenía botón `\abs{x}`.
- `_line_math_type()` detectaba `\abs{}` como línea matemática.
- Pero `_encode_math_expr()` no lo encodeaba realmente, por lo que podía terminar como texto incorrecto.

Ahora:

- `g2e.py` encodea `\abs{x}` como:
  - `97 1D 1A [contenido] 1B 1E`

Estado:

- Implementado.
- Pendiente de confirmar en calculadora física real.
- No debería afectar archivos que no usen `\abs{}`.

### Fix 4 — Símbolo integral crudo `∫`

Antes:

- El botón principal de integral insertaba `\int`, que sí funcionaba.
- Pero si desde la paleta se insertaba el carácter crudo `∫`, el backend podía convertirlo en `?`.

Ahora:

- Se agregó `∫` a `_CASIO_REMAP` con encoding `E6 BB`.

### Cambio 5 — Paleta de símbolos por tabs ampliada

Se reemplazó la paleta fija por una paleta dinámica en JavaScript.

Tabs actuales:

- Básicos
- Puntuación
- Operadores
- Comparación
- Conjuntos
- α-ω
- Α-Ω
- Flechas
- Plantillas

La paleta ahora incluye:

- Letras A-Z y a-z.
- Números 0-9.
- Puntuación ASCII común.
- Operadores seguros: `+ - * / = × ÷ ± √ ∫ ² ³ ° ∞`.
- Comparadores: `< > ≤ ≥ ≠ ≈`.
- Conjuntos confirmados: `∪ ∩`.
- Letras griegas minúsculas y mayúsculas ya presentes en el proyecto.
- Flechas `→ ← ↑ ↓`.
- Plantillas de markup: `\frac{num}{den}`, `x^{n}`, `\sqrt{x}`, `\sqrt[n]{x}`, `\abs{x}`, `\int`.

### Advertencia sobre “todos los caracteres” de EactMaker

El usuario pidió replicar los tabs de EactMaker con todos los caracteres posibles.

Estado actual:

- Se amplió bastante la paleta y se organizó por tabs.
- Todavía NO es una copia perfecta de todos los caracteres internos de EactMaker.
- La razón es que varios caracteres del catálogo `PC~EJEMP.g2e` aparecen como bytes Casio (`E5 C0`, `E5 C1`, etc.) cuyo Unicode/display exacto todavía no está identificado con seguridad.
- Agregar símbolos sin conocer bien su encoding puede volver a generar archivos incorrectos o peligrosos para la calculadora.

Próximo paso recomendado para Claude/ChatGPT:

1. Extraer o conseguir la tabla completa de EactMaker.
2. Mapear cada símbolo visible a su byte FONTCHARACTER Casio.
3. Agregar solo símbolos verificados a `_CASIO_REMAP`.
4. Marcar en UI los símbolos “seguros” vs “experimentales”.
5. Probar en hardware real en tandas pequeñas.

### Tests realizados por ChatGPT

Se ejecutó un test local de backend con contenido anidado:

- `x^{3}`
- `\frac{x^{2}}{\sqrt[3]{8}}`
- `\abs{x-2}+\int x`
- símbolos especiales básicos

Resultado:

- `create_g2e()` generó archivo sin error.
- `validate_g2e()` pasó correctamente.
- Se confirmó que el byte de valor absoluto `97 1D 1A` aparece en el archivo generado.

No se pudo probar en la calculadora física desde ChatGPT.

### Pendientes después de esta tanda

- Probar en la calculadora real:
  - archivo simple con `x^{3}`
  - archivo con `\frac{x}{\sqrt[3]{8}}`
  - archivo con `\abs{x}`
  - archivo con símbolos griegos
- Confirmar si la preview visual coincide suficientemente con la pantalla real.
- Replicar con más exactitud la paleta completa de EactMaker.
- Identificar símbolos Casio `E5 C0–DF`, `7F XX`, etc.
- Más adelante, rediseñar estética general.
- Mucho más adelante, evaluar migrar/publicar como `frack.one/calculadora` o empaquetar como ejecutable.

---

## 2026-05-27 — ChatGPT — Corrección fuerte de tabla de símbolos / paleta tipo EactMaker

### Objetivo de esta tanda

Fran reportó que la preview visual ya estaba funcionando bien, pero que la paleta de símbolos seguía incompleta y, peor, que algunos botones mostraban un carácter en la web pero generaban otro carácter distinto en la calculadora.

La prioridad fue corregir la codificación real de los caracteres antes de seguir agregando símbolos, porque una paleta grande con bytes incorrectos sería peor que una paleta chica: generaría eActivities visualmente engañosos y potencialmente difíciles de depurar.

### Nota sobre el `.rar` subido por Fran

El archivo `Calculadora.rar` subido en esta tanda fue reconocido como RAR5 y se pudo listar internamente, pero el entorno de ChatGPT no tenía un extractor RAR operativo (`unrar`, `7z`, `unar`, `bsdtar`, etc.). Por eso no se pudo extraer directamente la última mini-corrección de Claude.

Para no frenar el avance, los cambios se aplicaron sobre el último ZIP funcional generado por ChatGPT, es decir, la versión donde ya estaban corregidos:

- el crash de reapertura en calculadora;
- la preview matemática recursiva;
- `\abs{}`;
- la primera paleta dinámica.

Si Claude hizo cambios pequeños después de esa versión, hay que mergearlos manualmente con estos archivos.

### Fuente usada para reconstruir la tabla

Se revisó EactMaker de Planet-Casio, pero la página pública no expone fácilmente la tabla completa de caracteres desde el HTML renderizado. Para los bytes reales se usó la tabla pública `chars/chars.toml` del proyecto Cahute, que documenta caracteres Casio para la familia fx-9860/fx-9750.

Referencia principal:

- `https://gitlab.com/cahute/cahute/-/raw/develop/chars/chars.toml`

Motivo: Cahute documenta los códigos Casio `E5xx`, `E6xx` y varios códigos de un byte usados por estas calculadoras. Es una fuente mucho más segura que inventar mappings a ojo.

### Problema encontrado

La tabla anterior `_CASIO_REMAP` tenía muchos valores estimados o directamente incorrectos. Ejemplos importantes:

- `→`, `←`, `↑`, `↓` estaban corridos a códigos de otros símbolos.
- `π`, `θ` y varias griegas estaban mezcladas con rangos que no correspondían.
- `∪` y `∩` estaban asignadas a `E6 B0` y `E6 B1`, pero esos códigos corresponden a símbolos de aproximación/relación, no a unión/intersección.
- `≤`, `≥`, `≠`, `×`, `÷`, `°`, `²`, `³` estaban usando representaciones tipo Latin-1/Unicode, no los códigos Casio correctos.

Esto explica el síntoma de Fran: en la web se veía un carácter, pero en la calculadora aparecía otro.

### Cambios en `g2e.py`

Se reconstruyó `_CASIO_REMAP` con valores verificados desde Cahute.

Se corrigieron/agregaron, entre otros:

- Comparadores:
  - `≤` → `10`
  - `≠` → `11`
  - `≥` → `12`
  - `⇒` → `13`
- Operadores:
  - `√` → `86`
  - `∛` → `96`
  - `×` → `A9`
  - `÷` → `B9`
  - `°` → `9C`
- Griegas mayúsculas:
  - rango `E5 40` a `E5 58` según tabla Casio.
- Griegas minúsculas:
  - rango `E6 40` a `E6 58` según tabla Casio.
- Acentos latinos mayúsculos/minúsculos:
  - rangos `E5 01` y `E6 01`.
- Superíndices/subíndices:
  - rango `E5 C0` a `E5 DE`.
- Cirílico:
  - mayúsculas `E5 60` a `E5 82`.
  - minúsculas `E6 60` a `E6 82`.
- Flechas:
  - `←` → `E6 90`
  - `→` → `E6 91`
  - `↑` → `E6 92`
  - `↓` → `E6 93`
  - y diagonales/bidireccionales hasta `E6 99`.
- Formas:
  - triángulos, círculos, cuadrados, diamantes, brackets especiales, etc.
- Cálculo/conjuntos/lógica:
  - `≒`, `≈`, `≡`, `≢`, `≅`, `∽`, `∝`, `∫`, `∬`, `∮`, `∂`, `∡`, `∈`, `∋`, `⊆`, `⊇`, `⊂`, `⊃`, `⋃`, `⋂`, `∉`, `∌`, `⊈`, `⊉`, `⊄`, `⊅`, `∅`, `∃`, `∨`, `∧`, `∀`, etc.

Además:

- Se agregó helper interno `_b(hexstr)` para que los valores `E5xx`/`E6xx` sean legibles.
- Se dejaron alias de comodidad:
  - `∪` usa el mismo código que `⋃`.
  - `∩` usa el mismo código que `⋂`.

Nota importante: en la calculadora el glifo puede verse como `⋃`/`⋂` porque ese es el símbolo documentado por Casio/Cahute. Por eso la UI muestra principalmente `⋃` y `⋂`, dejando `∪`/`∩` como alias.

### Cambios en `templates/index.html`

Se reemplazó la paleta anterior por 6 tabs principales, más cercana a la idea de EactMaker y basada solo en símbolos que ahora tienen encoding en backend:

1. `Texto`
2. `Acentos/Cyr`
3. `Griegas`
4. `Sup/Sub`
5. `Math`
6. `Sets/Forms`

Se agregaron muchos más caracteres visibles que antes:

- ASCII común.
- Acentos latinos.
- Puntuación/currency extendida.
- Cirílico.
- Griegas completas.
- Superíndices/subíndices.
- Operadores matemáticos.
- Relaciones.
- Integrales/símbolos de cálculo.
- Conjuntos/lógica.
- Flechas y formas geométricas.

También se corrigieron los botones de plantillas dentro de la paleta para que inserten `\\frac`, `\\sqrt`, `\\abs`, `\\int`, etc. correctamente como texto en JavaScript. Si se deja una sola barra en un string JS, secuencias como `\f` se interpretan mal.

### Símbolos retirados o no agregados todavía

Se evitaron símbolos que estaban antes pero no quedaron verificados en la tabla revisada, por ejemplo:

- `±`
- `∞`

No significa que la calculadora no pueda tenerlos en algún menú o formato, sino que en esta tanda no se encontró un mapping seguro en la tabla usada. Mejor no mostrarlos antes que volver a generar símbolos incorrectos.

### Tests realizados por ChatGPT

Se ejecutó:

- `python -m py_compile g2e.py app.py`
- pruebas de `encode_casio_text()` con símbolos corregidos;
- generación de `test_symbols_chatgpt.g2e` con:
  - flechas;
  - griegas;
  - acentos;
  - cirílico;
  - conjuntos;
  - integrales;
  - comparadores;
  - una fórmula mixta con `x^{3}`, `\frac`, `\sqrt[3]` y `\abs`.
- `validate_g2e()` pasó correctamente.
- Se verificó que todos los símbolos listados en la UI se puedan encodear sin convertirse en `?`.

No se pudo probar en la calculadora física desde ChatGPT.

### Advertencias para Fran / Claude

1. Probar en la calculadora en tandas pequeñas.
   - Primero flechas y griegas.
   - Después conjuntos/lógica.
   - Después acentos/cirílico.

2. Si algún símbolo se ve distinto, NO agregar correcciones a ojo.
   - Crear un `.g2e` desde la calculadora con ese símbolo exacto.
   - Comparar los bytes.
   - Recién ahí ajustar `_CASIO_REMAP`.

3. La paleta ahora está mucho más cerca de un catálogo completo, pero todavía no se puede afirmar que sea 100% idéntica a los 6 tabs internos de EactMaker, porque el HTML público de EactMaker no expuso la tabla completa directamente.

4. Prioridad actual: seguridad/codificación correcta antes que estética.

### Archivos modificados en esta tanda

- `g2e.py`
- `templates/index.html`
- `PROYECTO.md`
