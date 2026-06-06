# eActivity Generator (.g2e)

Herramienta local en Python/Flask para escribir contenido eActivity desde la computadora y exportarlo como archivo `.g2e` compatible con calculadoras Casio fx-9750GIII/fx-9860.

## Objetivo

Crear una herramienta estable para preparar apuntes, fórmulas y ejercicios en formato eActivity. La prioridad actual es mantener la generación `.g2e` segura y compatible con la calculadora. La aplicación queda preparada para funcionar bajo la ruta `/calculadora` en un sitio web, sin login por el momento. El login, la estética final y la versión ejecutable de escritorio quedan como etapas posteriores.

## Estado actual

- App Flask preparada para uso local y para ruta web `/calculadora`.
- Generación de archivos `.g2e` desde texto plano con strips.
- Importación de archivos `.g2e` para volver a editarlos desde la interfaz.
- Vista previa tipo pantalla de calculadora en canvas.
- Paleta de símbolos organizada en tabs.
- Soporte para texto, símbolos Casio y plantillas matemáticas básicas.
- HTML, CSS y JavaScript separados.
- Preparación opcional para usar fuentes oficiales Casio de la serie gráfica.
- Favicon/logo propio integrado en la interfaz y en la pestaña del navegador.

## Estructura del proyecto

```text
app.py
    Servidor Flask, rutas de interfaz, descarga e importación de archivos. La interfaz principal responde en `/calculadora/`.

g2e.py
    Generador binario `.g2e`, importador básico, parser de strips, codificación de caracteres y validador estructural.

templates/index.html
    Plantilla HTML principal.

static/css/app.css
    Estilos de la interfaz.

static/js/app.js
    Lógica de editor, importación, preview, paleta de símbolos y canvas.

static/fonts/
    Carpeta opcional para fuentes Casio locales.

static/downloads/
    Carpeta reservada para una futura versión ejecutable de escritorio.

static/icon.ico
    Icono de la página y favicon.

passenger_wsgi.py
    Punto de entrada para entornos Python basados en Passenger.

requirements.txt
    Dependencias Python.
```

## Uso local

1. Instalar dependencias:

```bash
pip install -r requirements.txt
```

2. Ejecutar la app:

```bash
python app.py
```

3. Abrir en el navegador:

```text
http://localhost:5000/calculadora/
```

La raíz local `http://localhost:5000/` redirige automáticamente a `/calculadora/`.

4. Escribir el contenido, elegir un nombre de archivo y descargar el `.g2e`.

## Preparación web `/calculadora`

La aplicación está preparada para que la interfaz principal viva en:

```text
https://frack.one/calculadora
```

Rutas principales:

```text
/calculadora/          Interfaz principal
/calculadora/generate  Generación y descarga del `.g2e`
/calculadora/import    Importación editable de `.g2e`
/calculadora/static/   Archivos estáticos: CSS, JS, favicon, fuentes opcionales y descargas futuras
```

La ruta `/calculadora` redirige a `/calculadora/` para evitar problemas con rutas relativas.

Para despliegues Python compatibles con Passenger se incluye `passenger_wsgi.py`. En otros entornos WSGI, el objeto de aplicación es `app` dentro de `app.py`.

No se agregó login en esta etapa. La aplicación queda pública en la ruta indicada hasta que se implemente autenticación.

## Versión de escritorio futura

El proyecto mantiene como pendiente una versión ejecutable para Windows, con icono propio y funcionamiento local sin navegador público ni conexión a internet.

La ruta recomendada para esa etapa es:

- empaquetar con PyInstaller o herramienta equivalente;
- reutilizar `g2e.py` como núcleo de generación/importación;
- elegir entre una interfaz nativa o una app local embebida;
- publicar el instalador o `.exe` en `static/downloads/` o en una URL pública;
- definir `DESKTOP_DOWNLOAD_URL` para mostrar automáticamente el enlace de descarga en la interfaz web.

## Importación de archivos `.g2e`

La interfaz incluye un botón `Importar .g2e` para cargar un eActivity existente y convertirlo en texto editable dentro del editor.

La importación soporta:

- archivos generados por esta herramienta;
- archivos eActivity nativos con strips de texto;
- símbolos incluidos en la tabla de codificación;
- plantillas matemáticas básicas ya soportadas por el generador, como fracciones, raíces, potencias y valor absoluto.

La importación no pretende conservar el binario original byte por byte. El archivo se decodifica a un formato editable y, al guardar, se vuelve a generar con la estructura segura del generador actual. Si se detectan líneas nativas no editables o bytes sin mapeo, la interfaz muestra un aviso y omite o reemplaza solamente esas partes.

## Formato de entrada

Los strips se separan con líneas de título:

```text
=== Titulo ===
Contenido del strip.
Otra línea.

=== Formulas ===
A = π × r²
x^{2}
\frac{a}{b}
\sqrt{x}
```

Si no se define ningún strip, el programa usa un strip único con título derivado del nombre del archivo.

## Plantillas matemáticas soportadas

```text
\frac{num}{den}
x^{n}
\sqrt{x}
\sqrt[n]{x}
\abs{x}
\int
```

Estas plantillas se convierten a estructuras Casio cuando se genera el archivo. La vista previa intenta representarlas visualmente, pero no reemplaza la validación en la calculadora real.

## Formato `.g2e`

El generador mantiene los campos estructurales principales observados en archivos reales:

- cabecera estándar Casio con inversión bit a bit;
- `@EACT` en offset `0x68`;
- setup area de 56 bytes;
- marcador de versión G2E;
- subchunk `EACT1`;
- directorio de líneas;
- líneas terminadas en `00` y alineadas a 4 bytes;
- títulos de strip con ancho fijo de 21 caracteres.

El validador interno comprueba los tamaños, offsets y marcadores principales antes de entregar el archivo.

## Codificación de caracteres

Los caracteres ASCII imprimibles se guardan directamente. Los caracteres extendidos usan códigos Casio específicos en `_CASIO_REMAP` dentro de `g2e.py`.

La paleta de símbolos de la interfaz debe mantenerse sincronizada con `_CASIO_REMAP`. Si se agrega un símbolo en `static/js/app.js`, también debe existir su codificación correspondiente en `g2e.py`, salvo que sea ASCII simple o una plantilla matemática interpretada por el generador.

## Fuente de la vista previa

La interfaz está preparada para usar el set oficial de fuentes gráficas de Casio si los archivos están disponibles localmente en:

```text
static/fonts/CFX01.ttf
static/fonts/CFX02.ttf
static/fonts/CFX04.ttf
static/fonts/CFX05.ttf
static/fonts/CFX06.ttf
```

Estos archivos no se incluyen en el proyecto. Para usarlos, descargar el paquete oficial `GraphicSeriesFontSet.zip` desde el sitio educativo de Casio, extraer los `.ttf` y copiarlos dentro de `static/fonts/`.

Si las fuentes no están presentes, la aplicación usa una pila de fuentes monoespaciadas de respaldo y sigue funcionando normalmente.

## Cambios relevantes

### 2026-06-06

- Corrección del cálculo de `length2` dentro del subchunk `EACT1`, evitando archivos frágiles que podían congelar la calculadora al reabrirse.
- Headings de strips normalizados a 21 caracteres.
- Nombres de archivo sanitizados para formato seguro de calculadora.
- Validador estructural interno para archivos `.g2e` generados.
- Soporte para valor absoluto con `\abs{x}`.
- Mejora de la vista previa para fórmulas anidadas.
- Paleta de símbolos ampliada y sincronizada con la codificación backend.
- Separación de interfaz en HTML, CSS y JavaScript.
- Corrección del salto de scroll al insertar símbolos desde la paleta o plantillas matemáticas.
- El nombre de archivo conserva mayúsculas y minúsculas al descargar el `.g2e`.
- Limpieza de documentación y comentarios técnicos.
- Se agregó límite básico de tamaño de request en Flask.

### 2026-06-06 — Ajuste de interfaz y fuente

- Título visible actualizado a `eActivity Generator (.g2e)`.
- Subtítulo de modelos conservado.
- Crédito agregado debajo del subtítulo: `Made by frack.one`, con enlace externo a `https://frack.one`.
- Placeholder del campo de contenido eliminado.
- Texto de ayuda inferior al editor eliminado.
- Sección de vista previa/listado de strips eliminada por no ser necesaria para el flujo actual.
- Vista previa en canvas y glifos de la paleta preparados para usar fuentes Casio locales (`CFX01`, `CFX02`, `CFX04`, `CFX05`, `CFX06`).
- Se agregó `static/fonts/README.md` con instrucciones para colocar las fuentes opcionales.

### 2026-06-06 — Importación editable de `.g2e`

- Se agregó endpoint `/import` para recibir un archivo `.g2e` y devolver contenido editable en JSON.
- Se incorporó un importador básico en `g2e.py` capaz de leer el bloque `EACT1`, directorio de líneas, headings, líneas de texto y líneas matemáticas `0x82`.
- Se agregó decodificación inversa para la tabla de caracteres Casio utilizada por la paleta.
- Se agregó decodificación de plantillas básicas: fracción, raíz cuadrada, raíz n-ésima, potencia y valor absoluto.
- Se agregó botón `Importar .g2e` en la interfaz, con input de archivo oculto y mensajes de estado.
- Los archivos importados se cargan en el editor, actualizan el nombre de archivo y refrescan la simulación de pantalla.
- Si el archivo contiene líneas nativas no editables o bytes no mapeados, la importación continúa con avisos en vez de fallar completamente.

### 2026-06-06 — Preparación para `/calculadora`

- La aplicación principal quedó disponible en `/calculadora/`.
- La raíz `/` redirige a `/calculadora/` para uso local cómodo.
- Las rutas de generación e importación quedaron bajo `/calculadora/generate` y `/calculadora/import`.
- Los archivos estáticos quedaron bajo `/calculadora/static/` para evitar conflictos con otros recursos del sitio principal.
- Se agregó favicon/logo mediante `static/icon.ico`.
- Se agregó `passenger_wsgi.py` como punto de entrada para entornos Python compatibles con Passenger.
- Se agregó soporte opcional para mostrar un enlace de descarga de versión de escritorio mediante `DESKTOP_DOWNLOAD_URL`.
- Se agregó `static/downloads/` como carpeta reservada para ejecutables futuros.
- Se mantiene compatibilidad con rutas antiguas `/generate` e `/import` para builds locales previos.

## Pendientes

- Revisar bugs funcionales detectados durante uso real.
- Mejorar la experiencia de edición para apuntes largos.
- Diseñar una estética final más cuidada.
- Validar el despliegue final según el tipo de hosting disponible.
- Mejorar la importación de `.g2e` nativos con caracteres o líneas todavía no mapeadas.
- Agregar login y control de acceso si vuelve a ser necesario.
- Crear versión ejecutable de escritorio para Windows.
