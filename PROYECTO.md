# Generador eActivity para Casio fx-9750GIII

Proyecto local en Python/Flask para escribir contenido eActivity desde la computadora y exportarlo como archivo `.g2e` compatible con calculadoras Casio fx-9750GIII/fx-9860.

## Objetivo

Crear una herramienta estable para preparar apuntes, fórmulas y ejercicios en formato eActivity. La prioridad actual es mantener la generación `.g2e` segura y compatible con la calculadora. La interfaz web pública, el login y la estética final quedan como etapas posteriores.

## Estado actual

- App local con Flask.
- Generación de archivos `.g2e` desde texto plano con strips.
- Vista previa tipo pantalla de calculadora en canvas.
- Paleta de símbolos organizada en tabs.
- Soporte para texto, símbolos Casio y plantillas matemáticas básicas.
- Estructura base preparada para separar interfaz, estilos y scripts.

## Estructura del proyecto

```text
app.py
    Servidor Flask y ruta de descarga.

g2e.py
    Generador binario `.g2e`, parser de strips, codificación de caracteres y validador estructural.

templates/index.html
    Plantilla HTML principal.

static/css/app.css
    Estilos de la interfaz.

static/js/app.js
    Lógica de editor, preview, paleta de símbolos y canvas.

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
http://localhost:5000
```

4. Escribir el contenido, elegir un nombre de archivo y descargar el `.g2e`.

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

La interfaz usa una pila de fuentes con nombres habituales de fuentes Casio instaladas localmente y fallback monoespaciado:

```text
GraphicSeries, Casio Graph, Casio, ClassWiz Display, Cascadia Code, Consolas, monospace
```

No se incluye ningún archivo de fuente dentro del proyecto. Para una visualización más parecida a la calculadora, instalar localmente una fuente compatible y ajustar la pila de fuentes en `static/css/app.css` y `static/js/app.js` si fuera necesario.

## Cambios relevantes

### 2026-06-06

- Separación de la interfaz en HTML, CSS y JavaScript:
  - `templates/index.html`
  - `static/css/app.css`
  - `static/js/app.js`
- Corrección del salto de scroll al insertar símbolos desde la paleta o plantillas matemáticas.
- El foco vuelve al editor sin mover la página automáticamente.
- El nombre de archivo conserva mayúsculas y minúsculas al descargar el `.g2e`.
- La vista previa del título también conserva mayúsculas y minúsculas.
- Se agregó una pila de fuentes orientada a visualización Casio, con fallback seguro.
- Se limpió la documentación para dejarla en formato técnico y publicable.
- Se limpiaron comentarios del código para que sean normales y mantenibles.
- Se agregó límite básico de tamaño de request en Flask.

### Cambios estructurales previos preservados

- Corrección de offsets y longitudes del bloque `EACT1`.
- Títulos de strip de 21 caracteres.
- Validador estructural de archivos `.g2e`.
- Soporte de símbolos extendidos mediante tabla Casio.
- Vista previa matemática con fracciones, raíces, potencias y valor absoluto.

## Pendientes funcionales

- Revisar casos reales de uso donde la calculadora muestre un carácter distinto al esperado.
- Comparar la paleta contra capturas o archivos `.g2e` creados desde la calculadora si aparecen diferencias.
- Mejorar la vista previa para que represente más exactamente la fuente y espaciado de la calculadora.
- Agregar pruebas automatizadas para archivos generados.
- Mover archivos `.g2e` de prueba antiguos a una carpeta de referencia o legado.

## Pendientes para versión web

- Desactivar `debug=True` en producción.
- Agregar login propio con contraseñas hasheadas.
- Agregar sesiones seguras.
- Agregar límites de contenido y validación más completa del input.
- Definir despliegue en hosting o servidor compatible con Python.
- Evaluar integración futura bajo una ruta tipo `/calculadora`.

## Reglas de mantenimiento

- No modificar el formato binario sin probarlo con archivos reales.
- No agregar símbolos a la interfaz sin confirmar su codificación.
- Mantener separados HTML, CSS y JavaScript.
- Documentar cada cambio funcional importante en este archivo.
- Priorizar estabilidad sobre estética.
